import os
from pathlib import Path
from shutil import copyfile

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modules.ml.document_store.faiss import FAISSDocumentStore
from modules.ml.document_store.sql import DocumentORM, ORMBase
from modules.ml.retriever.retriever import Retriever
from modules.ml.vectorizer.tf_idf import TfidfDocVectorizer
from modules.ml.vectorizer.base import DocVectorizerBase

parent_cwd = Path(__file__).parent
test_db_path = os.path.join(parent_cwd, "topdup.test_db")
temp_test_db_path = os.path.join(parent_cwd, "temp_topdup.test_db")

def test_construction():
    with pytest.raises(ValueError):
        retriever = Retriever()
        print(type(retriever))

    # Copy new temp test database
    copyfile(test_db_path, temp_test_db_path)
    document_store = FAISSDocumentStore(sql_url=f"sqlite:///{temp_test_db_path}")
    cand_vectorizer = TfidfDocVectorizer(100)
    rtrv_vectorizer = TfidfDocVectorizer(256)

    with pytest.raises(ValueError):
        retriever = Retriever(
                    document_store=document_store,
                    candidate_vectorizer=cand_vectorizer,
                    retriever_vectorizer=rtrv_vectorizer,
                    )
        assert isinstance(retriever, Retriever)

    document_store = FAISSDocumentStore(sql_url=f"sqlite:///{temp_test_db_path}")
    cand_vectorizer = TfidfDocVectorizer(128)
    rtrv_vectorizer = TfidfDocVectorizer(256)
    retriever = Retriever(
                    document_store=document_store,
                    candidate_vectorizer=cand_vectorizer,
                    retriever_vectorizer=rtrv_vectorizer,
                    )
    assert isinstance(retriever, Retriever)

    # Remove temp test database
    os.remove(temp_test_db_path)

def test_train_candidate_vectorizer(mocker):
    # Copy new temp test database
    copyfile(test_db_path, temp_test_db_path)
    save_path = os.path.join(parent_cwd, "cand_vector.test_pkl")

    document_store = FAISSDocumentStore(sql_url=f"sqlite:///{temp_test_db_path}")
    cand_vectorizer = TfidfDocVectorizer(128)
    rtrv_vectorizer = TfidfDocVectorizer(256)
    retriever = Retriever(
                    document_store=document_store,
                    candidate_vectorizer=cand_vectorizer,
                    retriever_vectorizer=rtrv_vectorizer,
                    )

    if os.path.exists(save_path):
        os.remove(save_path)
    retriever.train_candidate_vectorizer(
                        save_path=save_path
                        )
    assert isinstance(retriever.candidate_vectorizer, DocVectorizerBase)
    assert retriever.candidate_vectorizer.is_trained == True
    os.path.exists(save_path)

    document_store = FAISSDocumentStore(sql_url=f"sqlite:///{temp_test_db_path}",
                                        vector_dim=100)
    retriever = Retriever(document_store=document_store)
    with pytest.raises(ValueError):
        retriever.train_candidate_vectorizer(
                        save_path=save_path,
                        retrain=False
                        )

    document_store = FAISSDocumentStore(sql_url=f"sqlite:///{temp_test_db_path}",
                                        vector_dim=128)
    retriever = Retriever(document_store=document_store)
    retriever.train_candidate_vectorizer(
                    save_path=save_path,
                    retrain=False
                    )
    assert isinstance(retriever.candidate_vectorizer, DocVectorizerBase)
    assert retriever.candidate_vectorizer.is_trained == True

    document_store = FAISSDocumentStore(sql_url=f"sqlite:///{temp_test_db_path}")
    retriever = Retriever(document_store=document_store)
    with pytest.raises(ValueError):
        retriever.train_candidate_vectorizer(
                        save_path=save_path
                        )

    document_store = FAISSDocumentStore(sql_url=f"sqlite:///{temp_test_db_path}")
    cand_vectorizer = TfidfDocVectorizer(128)
    rtrv_vectorizer = TfidfDocVectorizer(256)
    retriever = Retriever(
                    document_store=document_store,
                    candidate_vectorizer=cand_vectorizer,
                    retriever_vectorizer=rtrv_vectorizer,
                    )
    mocker.patch('modules.ml.document_store.faiss.FAISSDocumentStore.get_all_documents',
                    return_value=[])

    with pytest.raises(ValueError):
        retriever.train_candidate_vectorizer()

    url = f"sqlite:///{temp_test_db_path}"
    engine = create_engine(url)
    ORMBase.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(DocumentORM).filter_by().limit(20)
    training_documents = [query_result.text for query_result in query.all()]

    document_store = FAISSDocumentStore(sql_url=f"sqlite:///{temp_test_db_path}")
    cand_vectorizer = TfidfDocVectorizer(128)
    rtrv_vectorizer = TfidfDocVectorizer(256)
    retriever = Retriever(
                    document_store=document_store,
                    candidate_vectorizer=cand_vectorizer,
                    retriever_vectorizer=rtrv_vectorizer,
                    )
    retriever.train_candidate_vectorizer(
                        training_documents=training_documents
                        )
    assert isinstance(retriever.candidate_vectorizer, DocVectorizerBase)
    assert retriever.candidate_vectorizer.is_trained == True

    # Remove temp test database
    os.remove(temp_test_db_path)


def test_train_retriever_vectorizer(mocker):
    # Copy new temp test database
    copyfile(test_db_path, temp_test_db_path)
    save_path = os.path.join(parent_cwd, "retriever_vector.test_pkl")

    document_store = FAISSDocumentStore(sql_url=f"sqlite:///{temp_test_db_path}")
    cand_vectorizer = TfidfDocVectorizer(128)
    rtrv_vectorizer = TfidfDocVectorizer(256)
    retriever = Retriever(
                    document_store=document_store,
                    candidate_vectorizer=cand_vectorizer,
                    retriever_vectorizer=rtrv_vectorizer,
                    )

    if os.path.exists(save_path):
        os.remove(save_path)
    retriever.train_retriever_vectorizer(
                        save_path=save_path
                        )
    assert isinstance(retriever.retriever_vectorizer, DocVectorizerBase)
    assert retriever.retriever_vectorizer.is_trained == True
    os.path.exists(save_path)

    document_store = FAISSDocumentStore(sql_url=f"sqlite:///{temp_test_db_path}",
                                        vector_dim=128)
    retriever = Retriever(document_store=document_store)
    retriever.train_retriever_vectorizer(
                    save_path=save_path,
                    retrain=False
                    )
    assert isinstance(retriever.retriever_vectorizer, DocVectorizerBase)
    assert retriever.retriever_vectorizer.is_trained == True

    document_store = FAISSDocumentStore(sql_url=f"sqlite:///{temp_test_db_path}")
    retriever = Retriever(document_store=document_store)
    with pytest.raises(ValueError):
        retriever.train_retriever_vectorizer(
                        save_path=save_path
                        )

    document_store = FAISSDocumentStore(sql_url=f"sqlite:///{temp_test_db_path}")
    cand_vectorizer = TfidfDocVectorizer(128)
    rtrv_vectorizer = TfidfDocVectorizer(256)
    retriever = Retriever(
                    document_store=document_store,
                    candidate_vectorizer=cand_vectorizer,
                    retriever_vectorizer=rtrv_vectorizer,
                    )
    mocker.patch('modules.ml.document_store.faiss.FAISSDocumentStore.get_all_documents',
                    return_value=[])

    with pytest.raises(ValueError):
        retriever.train_retriever_vectorizer()

    print("Query sample input from database")
    url = f"sqlite:///{temp_test_db_path}"
    engine = create_engine(url)
    ORMBase.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(DocumentORM).filter_by().limit(20)
    training_documents = [query_result.text for query_result in query.all()]

    document_store = FAISSDocumentStore(sql_url=f"sqlite:///{temp_test_db_path}")
    cand_vectorizer = TfidfDocVectorizer(128)
    rtrv_vectorizer = TfidfDocVectorizer(256)
    retriever = Retriever(
                    document_store=document_store,
                    candidate_vectorizer=cand_vectorizer,
                    retriever_vectorizer=rtrv_vectorizer,
                    )
    retriever.train_retriever_vectorizer(
                        training_documents=training_documents
                        )
    assert isinstance(retriever.retriever_vectorizer, DocVectorizerBase)
    assert retriever.retriever_vectorizer.is_trained == True

    # Remove temp test database
    os.remove(temp_test_db_path)

def test_update_embeddings():
    # Copy new temp test database
    copyfile(test_db_path, temp_test_db_path)
    document_store = FAISSDocumentStore(sql_url=f"sqlite:///{temp_test_db_path}")
    cand_vectorizer = TfidfDocVectorizer(128)
    rtrv_vectorizer = TfidfDocVectorizer(256)
    retriever = Retriever(
        document_store=document_store,
        candidate_vectorizer=cand_vectorizer,
        retriever_vectorizer=rtrv_vectorizer,
    )
    with pytest.raises(ValueError):
        retriever.update_embeddings()

    cand_vectorizer = TfidfDocVectorizer(128)
    rtrv_vectorizer = TfidfDocVectorizer(256)
    retriever = Retriever(
        document_store=document_store,
        candidate_vectorizer=cand_vectorizer,
        retriever_vectorizer=rtrv_vectorizer,
    )
    retriever.train_candidate_vectorizer()
    save_path = os.path.join(parent_cwd, "document_store.test_pkl")
    retriever.update_embeddings(save_path=save_path)
    # Remove temp test database
    os.remove(temp_test_db_path)

def test_get_candidates():
    # Copy new temp test database
    copyfile(test_db_path, temp_test_db_path)
    document_store = FAISSDocumentStore(sql_url=f"sqlite:///{temp_test_db_path}")
    cand_vectorizer = TfidfDocVectorizer(128)
    rtrv_vectorizer = TfidfDocVectorizer(256)
    retriever = Retriever(
        document_store=document_store,
        candidate_vectorizer=cand_vectorizer,
        retriever_vectorizer=rtrv_vectorizer,
    )
    with pytest.raises(ValueError):
        retriever.get_candidates(query_docs = ["Test candidate"])

    # Remove temp test database
    os.remove(temp_test_db_path)

def test_calc_scores_for_candidates():
    # Copy new temp test database
    copyfile(test_db_path, temp_test_db_path)
    document_store = FAISSDocumentStore(sql_url=f"sqlite:///{temp_test_db_path}")
    cand_vectorizer = TfidfDocVectorizer(128)
    rtrv_vectorizer = TfidfDocVectorizer(256)
    retriever = Retriever(
        document_store=document_store,
        candidate_vectorizer=cand_vectorizer,
        retriever_vectorizer=rtrv_vectorizer,
    )
    with pytest.raises(ValueError):
        retriever._calc_scores_for_candidates(
                            query_doc = "Test candidate",
                            candidate_ids=[1, 2, 0])

    # Remove temp test database
    os.remove(temp_test_db_path)

def test_batch_retriever():
    # Copy new temp test database
    copyfile(test_db_path, temp_test_db_path)

    # Get a document from the database as input for retriever
    print("Query sample input from database")
    url = f"sqlite:///{temp_test_db_path}"
    engine = create_engine(url)
    ORMBase.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(DocumentORM).filter_by().limit(5)

    # Get text from query to input
    input_doc = query.all()[0].text
    print(" ".join(input_doc.split(" ")[:50]))  # print the query doc

    # Init expected result
    expected_text_result = input_doc
    expected_score_result = 1

    print("Init vectorizers")
    cand_vectorizer = TfidfDocVectorizer(128)
    rtrv_vectorizer = TfidfDocVectorizer(256)

    print("Init DocumentStore")
    document_store = FAISSDocumentStore(sql_url=f"sqlite:///{temp_test_db_path}")

    print("Init retriever")
    retriever = Retriever(
        document_store=document_store,
        candidate_vectorizer=cand_vectorizer,
        retriever_vectorizer=rtrv_vectorizer,
    )

    # Train vectorizers for two phases of searching
    print("Training vectorizers")
    retriever.train_candidate_vectorizer()
    retriever.train_retriever_vectorizer()

    # Subtets 1 check raise ERROR synchronize
    with pytest.raises(ValueError):
        result = retriever.batch_retrieve([input_doc], top_k_candidates=10)

    # Update trained embeddings to DocumentStore
    print("Updating embeddings to DocumentStore")
    retriever.update_embeddings()

    print("Retrieving")

    # Test without process input data
    result = retriever.batch_retrieve([input_doc], top_k_candidates=10)
    # print the retrieved doc
    print(
        " ".join(result[0]["retrieve_result"].split(" ")[:50])
    )

    assert result[0]["query_doc"] == input_doc
    assert result[0]["retrieve_result"] == expected_text_result
    assert result[0]["similarity_score"] == expected_score_result

    # Test with processing input data
    result = retriever.batch_retrieve(
                            [input_doc],
                            top_k_candidates=10,
                            processe_query_docs=True
                            )
    # print the retrieved doc
    print(
        " ".join(result[0]["retrieve_result"].split(" ")[:50])
    )

    assert result[0]["query_doc"] == input_doc
    assert result[0]["retrieve_result"] == expected_text_result
    assert result[0]["similarity_score"] == expected_score_result

    # Remove temp test database
    os.remove(temp_test_db_path)

def test_sequential_retrieve():
    number_input_doc = 3

    # Copy new temp test database
    copyfile(test_db_path, temp_test_db_path)

    # Get a document from the database as input for retriever
    print("Query sample input from database")
    url = f"sqlite:///{temp_test_db_path}"
    engine = create_engine(url)
    ORMBase.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(DocumentORM).filter_by().limit(number_input_doc)

    # Get text from query to input
    input_docs = [query.all()[i].text for i in range(number_input_doc)]
    # print(" ".join(input_doc.split(" ")[:50]))  # print the query doc

    # Init expected result
    expected_text_results = []
    expected_score_results = []

    for i in range(number_input_doc):
        expected_text_results.append(input_docs[i])
        expected_score_results.append(1)

    print("Init vectorizers")
    cand_vectorizer = TfidfDocVectorizer(128)
    rtrv_vectorizer = TfidfDocVectorizer(256)

    print("Init DocumentStore")
    document_store = FAISSDocumentStore(sql_url=f"sqlite:///{temp_test_db_path}")

    print("Init retriever")
    retriever = Retriever(
        document_store=document_store,
        candidate_vectorizer=cand_vectorizer,
        retriever_vectorizer=rtrv_vectorizer,
    )

    # Train vectorizers for two phases of searching
    print("Training vectorizers")
    retriever.train_candidate_vectorizer()
    retriever.train_retriever_vectorizer()

    # Subtets 1 check raise ERROR synchronize
    with pytest.raises(ValueError):
        results = retriever.sequential_retrieve(input_docs, top_k_candidates=10)

    # Update trained embeddings to DocumentStore
    print("Updating embeddings to DocumentStore")
    retriever.update_embeddings()

    print("Retrieving")

    # Test without process input data
    num_doc_before = retriever.document_store.get_document_count()
    results = retriever.sequential_retrieve(
                            input_docs,
                            top_k_candidates=10,
                            processe_query_docs=False
                            )

    for i in range(number_input_doc):
        assert results[i]["query_doc"] == input_docs[i]
        assert results[i]["retrieve_result"] == expected_text_results[i]
        assert results[i]["similarity_score"] == expected_score_results[i]

    num_doc_after = retriever.document_store.get_document_count()
    assert num_doc_after == num_doc_before + number_input_doc

    # Test with processing input data
    num_doc_before = retriever.document_store.get_document_count()
    results = retriever.sequential_retrieve(
                            input_docs,
                            top_k_candidates=10,
                            processe_query_docs=True
                            )
    for i in range(number_input_doc):
        assert results[i]["query_doc"] == input_docs[i]
        assert results[i]["retrieve_result"] == expected_text_results[i]
        assert results[i]["similarity_score"] == expected_score_results[i]

    num_doc_after = retriever.document_store.get_document_count()
    assert num_doc_after == num_doc_before + number_input_doc

    # Test with meta_docs
    num_doc_before = retriever.document_store.get_document_count()
    results = retriever.sequential_retrieve(
                            input_docs,
                            top_k_candidates=10,
                            processe_query_docs=True,
                            meta_docs = [{"author": "duclt", "task":["test", "retrieve", "query"],
                                        "author": "duclt"}]
                            )
    for i in range(number_input_doc):
        assert results[i]["query_doc"] == input_docs[i]
        assert results[i]["retrieve_result"] == expected_text_results[i]
        assert results[i]["similarity_score"] == expected_score_results[i]

    num_doc_after = retriever.document_store.get_document_count()
    assert num_doc_after == num_doc_before + number_input_doc
    # Remove temp test database
    os.remove(temp_test_db_path)


if __name__ == "__main__":
    # test_batch_retriever()
    test_train_candidate_vectorizer()
    # test_train_retriever_vectorizer()
