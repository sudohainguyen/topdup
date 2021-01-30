import numpy as np
import logging


from modules.ml.vectorizer.tf_idf import TfidfDocVectorizer
from modules.ml.document_store.faiss import FAISSDocumentStore


logger = logging.getLogger(__name__)

class Retriever:

    def __init__(self, 
                 document_store: FAISSDocumentStore = None, 
                 vectorizer: TfidfDocVectorizer = None,
                 vector_dim:int = 128):
        """
        :param documents: an instance of a DocumentStore (FAISSDocumentStore) to retrieve document from.
        :param vectorizer_type: Type of modules use for embedding and compute matrix (TFIDF AS DEFAULT).
        :param indexer_type: Name of the index in the DocumentStore from which to retrieve documents.
        :param vector_dim: Dimension for the vector that uses in First Layer.

        Init document_store and vectorizer

        """

        self.document_store = document_store
        self.vectorizer = vectorizer


    def train_vectorizer(self, training_documents=None, save_path=None):
        """
        Vectorize the document and transform into dense 

        Add the vector into the index

        Not sure the output for this one because it does not link or return anything
        """

        if not training_documents or len(training_documents):
            self.training_documents = [document.text for document in self.document_store.get_all_documents()]

            if not self.training_documents or len(self.training_documents) == 0:
                logger.warning("Fit method called with empty document store")
                return
        self.spare_documnet_embedding = self.vectorizer.fit_transform(self.training_documents)

        if save_path:
            self.vectorizer.save(save_path)

    def update_embeddings(self):
        self.document_store.update_embeddings(self.vectorizer)


    def retrieve(self, query_docs: str, top_k: int = 10, index: str = None, filters = None):
        """
        :param query_docs: The document query
        :param top_k: How many document to return 
        :param add_to_index: Add query document into DocumentStore and add embedding query into ...

        Scan through query_docs and convert it into embedding vector for comparison

        Return a small a number of document (top_k) that are most relevant to each query_doc
        """
        query_emb = self.vectorizer.transform(query_docs)
        score_matrix, vector_id_matrix = self.document_store.query_ids_by_embedding(query_emb=query_emb, filters=filters,
                                                           top_k=top_k, index=index)
        return score_matrix, vector_id_matrix

