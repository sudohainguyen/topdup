import schedule

from modules.ml.document_store.faiss import FAISSDocumentStore


def update_local_db():
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

    pass


def update_remote_db():
    """
    Write a proper docstring later
    This method runs in serial as follow:
    1. Update embeddings on large FAISS index
    2. Update vector ids on remote db
    3. Update meta data of documents on local db to remote db
    4. Clear local db
    """

    pass


if __name__ == "__main__":
    schedule.every(1).minutes.do(update_local_db)
    schedule.every().day.at("00:30").do(update_remote_db)
