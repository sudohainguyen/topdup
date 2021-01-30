from numpy.core.fromnumeric import transpose
from numpy.lib.function_base import vectorize
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

from modules.ml.vectorizer.base import DocVectorizerBase


class TfidfDocVectorizer(DocVectorizerBase):

    def __init__(self, vector_dim: int = 128, **kwargs):
        """
        Vectorize the documents and return a vector that has been embedding for indexer or comparison.

        :param documents: A list of document for vectorize.
        :param vector_dim: Dimension for the vector that uses in First Layer.
        :param is_training: Whether you want to fit_transform embedding or not.
        """
        self.vectorizer = TfidfVectorizer(max_features = vector_dim, **kwargs)
        self.is_trained = False



    def fit(self, train_documents: list):
        """
        Fit `train_documents` into the tf-idf and return a list of vector.
        """
        vectorizer = self.vectorizer.fit(train_documents)
        self.is_trained = True
        return vectorizer


    def fit_transform(self, train_documents: list):
        """
        Fit and transform `train_documents` into the tf-idf vectorizer and return a list of vector and convert to dense.
        """
        transform_vector = np.array(
            self.vectorizer.fit_transform(train_documents).todense())
        self.is_trained = True
        return transform_vector


    def transform(self, documents: list):
        """
        Transform `documents` into the tf-idf vectorizer and return a list of vector and convert to dense.
        """
        transform_vectors = np.array(self.vectorizer.transform(documents).todense())
        return transform_vectors

    def transform_document_objects(self, documents):
        document_text = [document.text for document in documents]
        return self.transform(document_text)

    @classmethod
    def save(cls, model_path):
        """ Save tf_idf model to the pickle file

        Args:
            model_path ([str]): [description]
        """

    @classmethod
    def load(cls, model_path):
        """
        Load tf_idf model from the pickle file
        """
        pass
