import numpy as np


from modules.ml.retriever.indexer.faiss import FaissIndexer
from modules.ml.retriever.vectorizer.tf_idf import TfidfDocVectorizer


class Retriever:

    def __init__(self, documents, vectorizer_type="tfidf",
                 indexer_type="faiss", vector_dim=128, is_training=True):

        self.documents = documents
        self.embeddings = None

        # check valid embedding methods
        if vectorizer_type == "tfidf":
            self.vectorizer = TfidfDocVectorizer(documents=self.documents,
                                                 vector_dim=vector_dim,
                                                 is_training=is_training)

            # if training while init retriever, set value of embedding attribute
            if is_training:
                self.embeddings = self.vectorizer.embeddings
        else:
            raise ValueError("The Retriever can currently only support "
                             "Tf-idf vectorizer."
                             "Please set vectorizer_type=\"tfidf\"")

        # check valid indexer
        if indexer_type == "faiss":
            self.indexer = FaissIndexer(document_embeddings=self.embeddings,
                                        vector_dim=vector_dim,
                                        is_training=is_training)
        else:
            raise ValueError("The Retriever can currently only support "
                             "faiss indexer_type."
                             "Please set indexer_type=\"faiss\"")

        self.is_trained = is_training

    def train_index(self):
        self.embeddings = self.vectorizer.fit_transform(self.documents)
        self.indexer.index(self.embeddings)
        self.is_trained = True

    def _query_vector(self, query_embs, top_k):
        return self.indexer.query_by_embeddings(query_embs, top_k=top_k)

    def retrieve(self, query_docs, top_k, add_to_index=False):

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
