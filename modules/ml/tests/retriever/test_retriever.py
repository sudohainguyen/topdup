import os
from pathlib import Path

from modules.ml.document_store.faiss import FAISSDocumentStore
from modules.ml.retriever.retriever import Retriever
from modules.ml.vectorizer.tf_idf import TfidfDocVectorizer

parent_cwd = Path(__file__).parent.parent

vectorizer = TfidfDocVectorizer(256)

db_path = os.path.join(parent_cwd, "document_store/topdup.db")
document_store = FAISSDocumentStore(sql_url=f"sqlite:///{db_path}")
retriever = Retriever(
    document_store=document_store,
    candidate_vectorizer=vectorizer,
    retriever_vectorizer=vectorizer,
)

retriever.document_store.faiss_index

retriever.train_candidate_vectorizer()
retriever.train_retriever_vectorizer()

retriever.candidate_vectorizer.vectorizer
retriever.retriever_vectorizer.vectorizer

retriever.update_embeddings()
