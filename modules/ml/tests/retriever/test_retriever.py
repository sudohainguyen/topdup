import os
from pathlib import Path
# import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modules.ml.document_store.faiss import FAISSDocumentStore
from modules.ml.retriever.retriever import Retriever
from modules.ml.vectorizer.tf_idf import TfidfDocVectorizer
from modules.ml.document_store.sql import DocumentORM, ORMBase


parent_cwd = Path(__file__).parent.parent
test_db_path = os.path.join(parent_cwd, "document_store/topdup.db")


def test_retrieve_with_database():

    print('Init vectorizer')
    cand_vectorizer = TfidfDocVectorizer(128)
    retriver_vectorizer = TfidfDocVectorizer(256)

    print('Init document store')
    document_store = FAISSDocumentStore(sql_url=f"sqlite:///{test_db_path}")

    print('Init retriever')
    retriever = Retriever(
        document_store=document_store,
        candidate_vectorizer=cand_vectorizer,
        retriever_vectorizer=retriver_vectorizer)

    # Traing vectorizer for two phases of searching
    print('Training vectorizer')
    retriever.train_candidate_vectorizer()
    retriever.train_retriever_vectorizer()

    # update embedding after training to document store
    print('Updating embedding to document store')
    retriever.update_embeddings()

    # Get a document from data base as input for retriver
    print('Query sample input from data base')
    url = f"sqlite:///{test_db_path}"
    engine = create_engine(url)
    ORMBase.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(DocumentORM).filter_by().limit(5)

    # Get text from query to input
    input_doc = query.all()[0].text

    # Init expected result
    expected_text_result = input_doc
    expected_score_result = 1

    print('Retrieving')

    result = retriever.retrieve([input_doc], top_k_candidates=10)
    assert result[input_doc]['retrieve_result'] == expected_text_result
    assert result[input_doc]['similarity_score'] == expected_score_result







