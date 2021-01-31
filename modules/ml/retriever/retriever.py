import logging

import numpy as np

from modules.ml.document_store.faiss import FAISSDocumentStore
from modules.ml.vectorizer.tf_idf import TfidfDocVectorizer

logger = logging.getLogger(__name__)


class Retriever:

    """Need help to fix"""

    def __init__(
        self,
        document_store: FAISSDocumentStore,
        vectorizer_type: str = "tfidf",
        vector_dim: int = 128,
        is_training: Optional[bool] = True,
    ):
        """
        :param documents: an instance of a DocumentStore (FAISSDocumentStore) to retrieve document from.
        :param vectorizer_type: Type of modules use for embedding and compute matrix (TFIDF AS DEFAULT).
        :param indexer_type: Name of the index in the DocumentStore from which to retrieve documents.
        :param vector_dim: Dimension for the vector that uses in First Layer.

        Init document_store and vectorizer

        """

        # self.document_store = document_store

        # if vectorizer_type == "tfidf":
        #     self.vectorizer = TfidfDocVectorizer(documents=self.documents,
        #                                          vector_dim=vector_dim,
        #                                          is_training=True)

        #     self.embeddings = self.vectorizer.embeddings
        # else:
        #     raise ValueError("The Retriever can currently only support "
        #                      "Tf-idf vectorizer."
        #                      "Please set vectorizer_type=\"tfidf\"")

    def train_index(self):
        """
        Vectorize the document and transform into dense

        Add the vector into the index

        Not sure the output for this one because it does not link or return anything
        """
        self.embeddings = self.vectorizer.fit_transform(self.documents)
        self.document_store.indexer.index(self.embeddings)

    def _query_vector(self, query_embs: np.array, top_k: int):
        """
        param query_embs: Embedding of the query.
        param top_k: How many documents to return.

        Find the document that is most similar to the provided `query_embs` via indexer of document_store.

        Return top_k vector id for each query_emb
        """

    def retrieve(
        self, query_docs: str, top_k: int, add_to_index: Optional[bool] = False
    ):
        """
        :param query_docs: The document query
        :param top_k: How many document to return
        :param add_to_index: Add query document into DocumentStore and add embedding query into ...

        Scan through query_docs and convert it into embedding vector for comparison

        Return a small a number of document (top_k) that are most relevant to each query_doc
        """
