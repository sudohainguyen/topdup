import logging
from typing import List

import numpy as np
from sqlalchemy.sql.sqltypes import Boolean
from tqdm import tqdm

from modules.ml.document_store.faiss import FAISSDocumentStore
from modules.ml.preprocessor.vi_preprocessor import ViPreProcessor
from modules.ml.vectorizer.base import DocVectorizerBase

logger = logging.getLogger(__name__)


class Retriever:
    def __init__(
        self,
        document_store: FAISSDocumentStore = None,
        candidate_vectorizer: DocVectorizerBase = None,
        retriever_vectorizer: DocVectorizerBase = None,
    ):
        """ Init an instance of a Retriever

        Args:
            document_store (FAISSDocumentStore): An instance of DocumentStore (FAISSDocumentStore)
                                                 to where data is indexed and stored. Defaults to None.
            candidate_vectorizer (DocVectorizerBase): An instance of vectorizer to convert
                                                 QUERY documents (in database) to embedding. Defaults to None.
            retriever_vectorizer (DocVectorizerBase): An instance of vectorizer to convert
                                                 CANDIDATE documents to embeddings. Defaults to None.
        """

        self.document_store = document_store
        self.candidate_vectorizer = candidate_vectorizer
        self.retriever_vectorizer = retriever_vectorizer

    def train_candidate_vectorizer(
        self,
        retrain: Boolean = True,
        training_documents: List[str] = None,
        save_path: str = None,
    ):
        """Train vectorizer for getting candidates phase

        Args:
            retrain (Boolean): Retrain or load saved vectorizer. Defaults to True.
            training_documents (List[str]): Training documents for vectorizer. Defaults to None.
            save_path (str): Path to save paramenters of vectorizer model. Defaults to None.
        """

        if not retrain:
            self.candidate_vectorizer = self.candidate_vectorizer.load(save_path)
            return

        if not training_documents or len(training_documents):
            self.training_documents = [
                document.text for document in self.document_store.get_all_documents()
            ]

            if not self.training_documents or len(self.training_documents) == 0:
                logger.warning("Fit method called with empty DocumentStore")
                return
        else:
            self.training_documents = training_documents

        self.spare_documnet_embedding = self.candidate_vectorizer.fit_transform(
            self.training_documents
        )

        if save_path:
            self.candidate_vectorizer.save(save_path)

    def train_retriever_vectorizer(
        self,
        retrain: Boolean = True,
        training_documents: List[str] = None,
        save_path: str = None,
    ):
        """Train vectorizer for final retrieve phase

        Args:
            retrain (Boolean): Retrain or load saved vectorizer. Defaults to True.
            training_documents (List[str]): Training documents for vectorizer. Defaults to None.
            save_path (str): Path to save paramenters of vectorizer model. Defaults to None.
        """

        if not retrain:
            self.retriever_vectorizer = self.retriever_vectorizer.load(save_path)
            return

        if not training_documents or len(training_documents):
            self.training_documents = [
                document.text for document in self.document_store.get_all_documents()
            ]

            if not self.training_documents or len(self.training_documents) == 0:
                logger.warning("Fit method called with empty DocumentStore")
                return
        else:
            self.training_documents = training_documents

        self.spare_documnet_embedding = self.retriever_vectorizer.fit_transform(
            self.training_documents
        )

        if save_path:
            self.retriever_vectorizer.save(save_path)

    def update_embeddings(
        self, retrain: Boolean = True, save_path: str = None, sql_url: str = None
    ):
        """Update embeddings of documents with candidate vectorizer to `document_store`."""

        if retrain:
            self.document_store.update_embeddings(self.candidate_vectorizer)
            self.document_store.save(file_path=save_path)
        else:
            self.document_store = self.document_store.load(
                faiss_file_path=save_path, sql_url=sql_url
            )

    def get_candidates(
        self, query_docs: List[str], top_k: int = 10, index: str = None, filters=None
    ):
        """First phase of retriever to get top_k candidates

        Args:
            query_docs (List[str]): The documents to query. Defaults to None.
            top_k (int, optional): How many document to return for each query_doc. Defaults to 10.

        Returns:
            tuple: Return a tuple of score_matrix and vector_id_matrix (top_k)
                             that are most relevant to each query_doc
        """
        query_embs = self.candidate_vectorizer.transform(query_docs)
        score_matrix, vector_id_matrix = self.document_store.query_ids_by_embedding(
            query_emb=query_embs, filters=filters, top_k=top_k, index=index
        )

        return query_embs, score_matrix, vector_id_matrix

    def _calc_scores_for_candidates(self, query_doc, candidate_ids):
        """Caculate scores for each candidate in 2nd phase

        Args:
            query_doc (str, optional): The document to query. Defaults to None.
            candidate_ids (List[int]): List of candidate_ids of query. Defaults to None.

        Returns:
            [type]: [description]
        """
        query_emb = self.retriever_vectorizer.transform([query_doc])
        candidate_ids = list(map(str, candidate_ids))

        candidate_docs = self.document_store.get_documents_by_vector_ids(candidate_ids)
        candidate_docs_text = [candidate_doc.text for candidate_doc in candidate_docs]
        candidate_docs_id = [candidate_doc.id for candidate_doc in candidate_docs]
        candidate_embs = self.retriever_vectorizer.transform(candidate_docs_text)

        scores = candidate_embs.dot(query_emb.T)
        idx_scores = [(idx, score) for idx, score in enumerate(scores)]

        highest_score = sorted(idx_scores, key=(lambda tup: tup[1]), reverse=True)[
            1
        ]  # 0 location is the query_doc itself

        return candidate_docs_id[highest_score[0]], highest_score[1]

    def batch_retrieve(
        self,
        query_docs,
        top_k_candidates=10,
        processe_query_docs=False,
        index=None,
        filters=None,
    ):
        """[summary]

        Args:
            query_docs ([type]): [description]
            top_k_candidates (int, optional): [description]. Defaults to 10.
            processe_query_docs (bool, optional): [description]. Defaults to False.
            index ([type], optional): [description]. Defaults to None.
            filters ([type], optional): [description]. Defaults to None.

        Returns:
            [type]: [description]
        """
        processor = ViPreProcessor()
        if processe_query_docs:
            query_docs = [
                processor.clean({"text": query_doc})["text"] for query_doc in query_docs
            ]

        _, _, candidate_id_matrix = self.get_candidates(
            query_docs=query_docs, top_k=top_k_candidates, index=index, filters=filters
        )

        retrieve_results = []

        for idx, query_doc in enumerate(tqdm(query_docs, desc="Retrieving.....  ")):
            candidate_ids = [
                candidate_id
                for candidate_id in candidate_id_matrix[idx]
                if candidate_id >= 0
            ]

            retrieve_result, score = self._calc_scores_for_candidates(
                query_doc=query_doc, candidate_ids=candidate_ids
            )

            retrieve_results.append(
                {
                    "query_doc": query_doc,
                    "retrieve_result": retrieve_result,
                    "similarity_score": round(score[0], 5),
                }
            )

        return retrieve_results

    def sequential_retrive(
        self,
        query_docs,
        meta_docs,
        top_k_candidates=10,
        processe_query_docs=True,
        index=None,
        filters=None,
    ):
        """[summary]

        Args:
            query_docs ([type]): [description]
            meta_docs ([type]): [description]
            top_k_candidates (int, optional): [description]. Defaults to 10.
            processe_query_docs (bool, optional): [description]. Defaults to True.
            index ([type], optional): [description]. Defaults to None.
            filters ([type], optional): [description]. Defaults to None.

        Returns:
            [type]: [description]
        """
        processor = ViPreProcessor()
        retrieve_results = []
        for idx, query_doc in enumerate(
            tqdm(query_docs, desc="Sequential retrieving.....  ")
        ):

            if processe_query_docs:
                doc = processor.clean({"text": query_doc})
            else:
                doc = {"text": query_doc}

            query_emb, _, candidate_id_matrix = self.get_candidates(
                query_docs=[doc["text"]],
                top_k=top_k_candidates,
                index=index,
                filters=filters,
            )
            candidate_ids = [
                candidate_id
                for candidate_id in candidate_id_matrix[0]
                if candidate_id >= 0
            ]

            retrieve_result, score = self._calc_scores_for_candidates(
                query_doc=query_doc, candidate_ids=candidate_ids
            )
            retrieve_results.append(
                {
                    "query_doc": query_doc,
                    "retrieve_result": retrieve_result,
                    "similarity_score": round(score[0], 5),
                }
            )

            doc["embedding"] = query_emb[0]
            meta = meta_docs[idx]
            for m in meta.keys():
                if isinstance(meta[m], list):
                    meta[m] = "|".join(meta[m])

            doc["meta"] = meta

            self.document_store.write_documents([doc])

        return retrieve_results
