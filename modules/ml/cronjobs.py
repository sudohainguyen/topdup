import logging
import os
from datetime import datetime, timedelta

import schedule
from tqdm.auto import tqdm

from modules.ml.retriever.retriever import Retriever
from modules.ml.utils import get_connection
from modules.ml.vectorizer.tf_idf import TfidfDocVectorizer

# TODO: config remote logging

LOCAL_DB_URI = os.getenv("LOCAL_DB_URI", "sqlite:///local.db")
POSTGRES_URI = os.getenv(
    "POSTGRES_URI", "postgresql+psycopg2://user:pwd@host/topdup_articles"
)
CAND_DIM = 768
RTRV_DIM = 1024
HARD_SIM_THRESHOLD = 0.8
CAND_PATH = os.getenv("CAND_PATH", "cand.bin")
RTRV_PATH = os.getenv("RTRV_PATH", "rtrv.bin")
INDEX = os.getenv("INDEX", "document")
LOCAL_IDX_PATH = os.getenv("LOCAL_IDX_PATH", "local_index.bin")
REMOTE_IDX_PATH = os.getenv("REMOTE_IDX_PATH", "remote_index.bin")

local_doc_store = get_connection(LOCAL_DB_URI, CAND_DIM)
remote_doc_store = get_connection(POSTGRES_URI, CAND_DIM)


def update_local_db(local_doc_store, remote_doc_store):
    """
    Write a proper docstring later
    This method runs in serial as follow:
    1. Get document ids from remote and local db
    2. Check if there is new document
    If Yes:
    3. Write new document to local db
    4. Update embeddings on small FAISS index
    5. Update vector ids on local db
    6. Run sequential retriever to pre-calculate the similarity scores
    and update on local db meta data
    """

    if not local_doc_store or not remote_doc_store:
        logging.warning("DB connection not initialized, trying re-connect...")
        local_doc_store = get_connection(LOCAL_DB_URI, CAND_DIM)
        remote_doc_store = get_connection(POSTGRES_URI, CAND_DIM)
        if not local_doc_store or not remote_doc_store:
            logging.error("DB initialization failed, quit local_update...")
            return

    remote_reindex = not os.path.exists(REMOTE_IDX_PATH)
    if remote_reindex:
        new_ids = remote_doc_store.get_document_ids(
            from_time=datetime.now() - timedelta(days=365), index=INDEX
        )
    else:
        new_ids = remote_doc_store.get_document_ids(
            from_time=datetime.now() - timedelta(minutes=3), index=INDEX
        )
    if not new_ids:
        logging.info(f"No new updates in local db at {datetime.now()}")
        return

    local_ids = local_doc_store.get_document_ids(index=INDEX)

    # Filter existing ids in local out of recent updated ids from remote db
    new_ids = sorted([_id for _id in new_ids if _id not in local_ids])

    docs = remote_doc_store.get_documents_by_id(new_ids, index=INDEX)
    logging.info(f"Retrieved {len(docs)} at {datetime.now()}")

    if len(docs) > 0:
        local_doc_store.write_documents(docs)
        logging.info("Stored documents to local db")

        local_retriever = Retriever(
            document_store=local_doc_store,
            candidate_vectorizer=TfidfDocVectorizer(CAND_DIM),
            retriever_vectorizer=TfidfDocVectorizer(RTRV_DIM),
        )
        remote_retriever = Retriever(
            document_store=remote_doc_store,
            candidate_vectorizer=TfidfDocVectorizer(CAND_DIM),
            retriever_vectorizer=TfidfDocVectorizer(RTRV_DIM),
        )

        if not os.path.exists(CAND_PATH) or not os.path.exists(RTRV_PATH):
            remote_retriever.train_candidate_vectorizer(
                retrain=True, save_path=CAND_PATH
            )
            remote_retriever.train_retriever_vectorizer(
                retrain=True, save_path=RTRV_PATH
            )
            logging.info("Vectorizers retrained")
        else:
            remote_retriever.train_candidate_vectorizer(
                retrain=False, save_path=CAND_PATH
            )
            remote_retriever.train_retriever_vectorizer(
                retrain=False, save_path=RTRV_PATH
            )

        local_retriever.train_candidate_vectorizer(retrain=False, save_path=CAND_PATH)
        local_retriever.train_retriever_vectorizer(retrain=False, save_path=RTRV_PATH)
        logging.info("Vectorizers loaded")

        local_retriever.update_embeddings(
            retrain=True, save_path=LOCAL_IDX_PATH, sql_url=LOCAL_DB_URI
        )
        remote_retriever.update_embeddings(
            retrain=remote_reindex, save_path=REMOTE_IDX_PATH, sql_url=POSTGRES_URI
        )
        logging.info("Embeddings updated")

        docs = [doc.text for doc in docs]
        local_results = local_retriever.batch_retrieve(docs)
        if remote_reindex:
            remote_result = local_results.copy()
        else:
            remote_result = remote_retriever.batch_retrieve(docs)
        for _id, l, r in tqdm(
            zip(new_ids, local_results, remote_result), total=len(new_ids)
        ):
            local_sim = l.get("similarity_score", 0)
            remote_sim = r.get("similarity_score", 0)
            if (local_sim > HARD_SIM_THRESHOLD) & (remote_sim > HARD_SIM_THRESHOLD):
                if local_sim >= remote_sim:
                    sim_data = {
                        "sim_score": local_sim,
                        "similar_to": l["retrieve_result"],
                    }
                else:
                    sim_data = {
                        "sim_score": remote_sim,
                        "similar_to": r["retrieve_result"],
                    }
                remote_doc_store.update_document_meta(_id, sim_data)
        logging.info("Similarity scores updated into metadata")


def update_remote_db(remote_doc_store):
    """
    Write a proper docstring later
    This method runs in serial as follow:
    1. Update embeddings on large FAISS index
    2. Update vector ids on remote db
    3. Update meta data of documents on local db to remote db
    4. Clear local db
    """

    remote_retriever = Retriever(
        document_store=remote_doc_store,
        candidate_vectorizer=TfidfDocVectorizer(CAND_DIM),
        retriever_vectorizer=TfidfDocVectorizer(RTRV_DIM),
    )
    remote_retriever.train_candidate_vectorizer(retrain=False, save_path=CAND_PATH)
    remote_retriever.update_embeddings(retrain=True)
    logging.info("Remote embeddings and vector ids updated")

    local_doc_store.delete_all_documents()


if __name__ == "__main__":
    schedule.every().minute.do(update_local_db, local_doc_store, remote_doc_store)
    schedule.every().day.at("00:00").do(update_remote_db, remote_doc_store)
    while True:
        schedule.run_pending()
