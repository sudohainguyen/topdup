from abc import abstractmethod, ABC


class DocVectorizerBase(ABC):

    @abstractmethod
    def fit(self, train_documents):
        pass

    @abstractmethod
    def fit_transform(self, train_documents):
        pass

    @abstractmethod
    def transform(self, documents):
        pass
