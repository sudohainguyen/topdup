import faiss
import numpy as np

from modules.ml.retriever.indexer.base import IndexerBase


class FaissIndexer(IndexerBase):

    def __init__(self, document_embeddings,
                 vector_dim=128, similarity='cosin',
                 is_training=True, **kwargs):

        # check type of similarity score
        if similarity == "cosin":
            self.similarity = similarity
        else:
            raise ValueError("The FaissIndexer can currently only support"
                             "cosin similarity."
                             "Please set similarity=\"cosin\"")

        self.vector_dim = vector_dim

        # init indexer
        self.indexer = faiss.IndexFlatIP(self.vector_dim,
                                         **kwargs)

        if is_training:
            self.index(document_embeddings)

    def index(self, document_embeddings):
        self.add(document_embeddings)

    def add(self, new_embeddings):
        new_embeddings = new_embeddings.astype('float32')
        self.indexer.add(new_embeddings)

    def query_by_embeddings(self, query_embs, top_k=10):
        query_embs = np.array(query_embs).astype('float32')
        return self.indexer.search(x=query_embs, k=top_k)

    def get_size(self):
        return self.indexer.ntotal
