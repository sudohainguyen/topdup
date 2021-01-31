import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from modules.ml.retriever.vectorizer.base import DocVectorizerBase


class TfidfDocVectorizer(DocVectorizerBase):
    def __init__(
        self,
        documents: list = [],
        vector_dim: int = 128,
        is_training: bool = True,
        **kwargs
    ):
        """
        Vectorize the documents and return a vector that has been embedding for indexer or comparison.

        :param documents: A list of document for vectorize.
        :param vector_dim: Dimension for the vector that uses in First Layer.
        :param is_training: Whether you want to fit_transform embedding or not.
        """
        self.vectorizer = TfidfVectorizer(max_features=vector_dim, **kwargs)

        if is_training:
            self.embeddings = self.fit_transform(documents)

    def fit(self, train_documents: list) -> List[np.array(train_documents)]:
        """
        Fit `train_documents` into the tf-idf and return a list of vector.
        """
        train_documents = self.vectorizer.fit(train_documents)
        return train_documents

    def fit_transform(self, train_documents: list) -> List[np.array(Transform_Vector)]:
        """
        Fit and transform `train_documents` into the tf-idf vectorizer and return a list of vector and convert to dense.
        """
        transform_vector = np.array(
            self.vectorizer.fit_transform(train_documents).todense()
        )
        return transform_vector

    def transform(self, documents: list) -> List[np.array(Transform_Vector)]:
        """
        Transform `documents` into the tf-idf vectorizer and return a list of vector and convert to dense.
        """
        transform_vector = np.array(self.vectorizer.transform(documents).todense())
        return transform_vector

    @classmethod
    def save(self, model_path):
        """Save tf_idf model to the pickle file

        Args:
            model_path ([str]): [description]
        """

    @classmethod
    def load(cls, model_path):
        """
        Load tf_idf model from the pickle file
        """
        pass
