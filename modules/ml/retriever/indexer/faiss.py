import faiss
import numpy as np

from modules.ml.retriever.indexer.base import IndexerBase


class FaissIndexer(IndexerBase):

    def __init__(self, document_embeddings: list, vector_dim: int = 128, similarity: str = 'cosin', is_training: = True, **kwargs):
        """
        Using FAISS library (https://github.com/facebookresearch/faiss) to perform similarity search on vectors.

        All of the document text and meta-data are stored using PostgreSQL while the vector embeddings are indexed in FAISS Index.

        :param document_emddings: The document list or array that has been embedding.
        :param vector_dim: Dimension for the vector that uses in First Layer.
        :param similarity: Metrics that use for similarity search. `cosine` is the default.
        :param is_training: Whether you want to index the document embeddings or not.
        """


        # check type of similarity score
        if similarity == "cosin":
            self.similarity = similarity
        else:
            raise ValueError("The FaissIndexer can currently only support"
                             "cosine similarity."
                             "Please set similarity=\"cosin\"")

        self.vector_dim = vector_dim

        # init indexer
        self.indexer = faiss.IndexFlatIP(self.vector_dim,
                                         **kwargs)

        if is_training:
            self.index(document_embeddings)
        else:
            raise Exception("Please set is_training=\"True\"")


    def index(self, document_embeddings: np.array):
        """
        Calling `ADD Function` to add the document that has been embedding into the FAISS Indexer.

        param document_embeddings: An array of document that has been embedded.
        """
        self.add(document_embeddings)


    def add(self, new_embeddings: np.array):
        """
        Append documents that have been embedded into FAISS Indexer.

        param new_embedding: An array to add into indexer.
        """
        new_embeddings = new_embeddings.astype('float32')
        self.indexer.add(new_embeddings)


    def query_by_embeddings(self, query_embs: np.array, top_k: int = 10):
        """
        Find the document that is most similar to the provided `query_embs` by using a cosine similarity metric.


        param query_embs: Embedding of the query.
        param top_k: How many documents to return.
        """
        query_embs = np.array(query_embs).astype('float32')
        return self.indexer.search(x=query_embs, k=top_k)


    def get_size(self):
        """
        Get the size of the indexer.
        """
        return self.indexer.ntotal
