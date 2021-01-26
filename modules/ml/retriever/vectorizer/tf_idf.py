from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

from modules.ml.retriever.vectorizer.base import DocVectorizerBase


class TfidfDocVectorizer(DocVectorizerBase):

    def __init__(self, documents=[], vector_dim=128, is_training=True, **kwargs):
        self.vectorizer = TfidfVectorizer(max_features=vector_dim, **kwargs)

        if is_training:
            self.embeddings = self.fit_transform(documents)

    def fit(self, train_documents):
        self.vectorizer = self.vectorizer.fit(train_documents)

    def fit_transform(self, train_documents):
        transform_vector = np.array(
            self.vectorizer.fit_transform(train_documents).todense())
        return transform_vector

    def transform(self, documents):
        transform_vector = np.array(self.vectorizer.transform(documents).todense())
        return transform_vector
