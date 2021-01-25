from abc import abstractmethod, ABC


class IndexerBase(ABC):

    @abstractmethod
    def index(self, document_embeddings):
        pass

    @abstractmethod
    def add(self, list_vector):
        pass

    @abstractmethod
    def query_by_embeddings(self, query_embs, top_k):
        pass

    @abstractmethod
    def get_size(self):
        pass
