import numpy as np


from modules.ml.retriever.indexer.faiss import FaissIndexer
from modules.ml.retriever.vectorizer.tf_idf import TfidfDocVectorizer
from modules.ml.document_store.base import BaseDocumentStore


class First_Layer_Retriever:

    def __init__(self, documents: BaseDocumentStore, vectorizer_type: str = "tfidf", indexer_type: str = "faiss", vector_dim: int = 128, is_training: Optional[bool] = True):
        """
        :param documents: an instance of a DocumentStore (HAVE NOT LINK YET) to retrieve document from.
        :param vectorizer_type: Type of modules use for embedding and compute matrix (TFIDF AS DEFAULT).
        :param indexer_type: Name of the index in the DocumentStore from which to retrieve documents.
        :param vector_dim: Dimension for the vector that uses in First Layer.
        

        Read all document from DocumentStore.

        Checking both inputs from vectorizer_type and indexer_type are valid or not
            + Vectorizer must be TFIDF
            + Indexer must be FAISS
        
        """

        self.documents = documents

        if vectorizer_type == "tfidf":
            self.vectorizer = TfidfDocVectorizer(documents=self.documents,
                                                 vector_dim=vector_dim,
                                                 is_training=True)

            self.embeddings = self.vectorizer.embeddings
        else:
            raise ValueError("The Retriever can currently only support "
                             "Tf-idf vectorizer."
                             "Please set vectorizer_type=\"tfidf\"")

        if indexer_type == "faiss":
            self.indexer = FaissIndexer(document_embeddings=self.embeddings,
                                        vector_dim=vector_dim,
                                        is_training=True)
        else:
            raise ValueError("The Retriever can currently only support "
                             "faiss indexer_type."
                             "Please set indexer_type=\"faiss\"")



    def train_index(self):
        """
        Vectorize the document and transform into dense 

        Add the vector into the index

        Not sure the output for this one because it does not link or return anything
        """
        self.embeddings = self.vectorizer.fit_transform(self.documents)
        self.indexer.index(self.embeddings)
        self.is_trained = True


    def _query_vector(self, query_embs: np.array, top_k: int):
        """
        param query_embs: Embedding of the query.
        param top_k: How many documents to return.
    
        Find the document that is most similar to the provided `query_embs` by using a vector similarity metric.

        Return top_k embedding vectors
        """
        return self.indexer.query_by_embeddings(query_embs, top_k=top_k)


    def retrieve(self, query_docs: str, top_k: int, add_to_index: Optional[bool] = False) -> dict{Results}:
        """
        :param query_docs: The document query
        :param top_k: How many document to return 
        :param add_to_index: Add query document into DocumentStore and add embedding query into ...

        Scan through query_docs and convert it into embedding vector for comparison
        
        Return a small a number of document (top_k) that are most relevant to the query
        """

        # get embedding vector for query_docs
        query_embs = self.vectorizer.transform(query_docs)
        _, query_results = self._query_vector(query_embs, top_k)


        results = {}
        for idx, query_doc in enumerate(query_docs):

            # get indices of results for each query_docs and remove indices < 0
            index_results = query_results[idx]
            valid_indices = index_results[index_results >= 0]

            # get list of results for each query_doc
            results[query_doc] = np.array(self.documents)[valid_indices]


        # update index and document if add_to_index == True
        if add_to_index:

            self.documents.extend(query_docs)
            self.indexer.add(query_embs)

        return results
