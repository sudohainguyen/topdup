import os
from copy import deepcopy

from fastapi import FastAPI, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from scipy.optimize import linear_sum_assignment
from sklearn.metrics.pairwise import cosine_similarity
from starlette.exceptions import HTTPException as StarletteHTTPException

from modules.ml.document_store.faiss import FAISSDocumentStore
from modules.ml.preprocessor.vi_preprocessor import ViPreProcessor
from modules.ml.retriever.retriever import Retriever
from modules.ml.vectorizer.tf_idf import TfidfDocVectorizer
from modules.ml_api.models import CompareEntry, QueryResult

# Environment variables
POSTGRES_URI = os.getenv(
    "POSTGRES_URI", "postgresql+psycopg2://user:pwd@host/topdup_articles"
)
CAND_DIM = 768
RTRV_DIM = 1024
CAND_PATH = os.getenv("CAND_PATH", "cand.bin")

# Default methods
preprocessor = ViPreProcessor(split_by="sentence")

document_store = FAISSDocumentStore(
    sql_url=POSTGRES_URI, vector_dim=CAND_DIM, index_buffer_size=5000
)

retriever = Retriever(
    document_store=document_store,
    candidate_vectorizer=TfidfDocVectorizer(CAND_DIM),
    retriever_vectorizer=TfidfDocVectorizer(RTRV_DIM),
)
retriever.train_candidate_vectorizer(retrain=False, save_path=CAND_PATH)

tags_metadata = [
    {"name": "get", "description": "Properly do nothing now"},
    {
        "name": "compare",
        "description": "Compare and show the similar sentences between two documents",
    },
]
app = FastAPI(
    title="TopDup-ML",
    description="Allow other services to connect with ML engines",
    version="0.0.1",
    openapi_tags=tags_metadata,
)


@app.get("/", tags=["get"])
def get_query():
    return Response()


@app.post(
    "/compare",
    response_model=QueryResult,
    status_code=status.HTTP_200_OK,
    tags=["compare"],
)
def compare(entry: CompareEntry, response: Response):
    # Split texts before cleaning
    s_text_A = preprocessor.split({"text": entry.pairs[0]})
    s_text_B = preprocessor.split({"text": entry.pairs[1]})

    # Clean texts
    sc_text_A = deepcopy(s_text_A)
    sc_text_B = deepcopy(s_text_B)
    sc_text_A = [preprocessor.clean(s_text) for s_text in sc_text_A]
    sc_text_B = [preprocessor.clean(s_text) for s_text in sc_text_B]

    # Calculate embedding vectors
    embedding_vectors_A = retriever.candidate_vectorizer.transform(
        [t["text"] for t in sc_text_A]
    )
    embedding_vectors_B = retriever.candidate_vectorizer.transform(
        [t["text"] for t in sc_text_B]
    )

    # Maximize the sum of similiraties
    row_idx, col_idx = linear_sum_assignment(
        cosine_similarity(embedding_vectors_A, embedding_vectors_B), maximize=True
    )

    results = list()
    for a, b in zip(row_idx, col_idx):
        results.append(
            {
                "text_A": s_text_A[a]["text"],
                "sentence_id_A": s_text_A[a]["meta"]["_split_id"],
                "text_B": s_text_B[b]["text"],
                "sentence_id_B": s_text_B[b]["meta"]["_split_id"],
            }
        )

    return {"message": "Successfully requested TopDup-ML [compare]", "result": results}


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request, exc):
    msg = ", ".join([f'{err["loc"]}: {err["msg"]}' for err in exc.errors()])
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"message": msg}
    )


@app.exception_handler(StarletteHTTPException)
def http_exception_handler(request, exc):
    code = status.HTTP_400_BAD_REQUEST
    msg = str(exc)
    if exc.status_code == 404:
        code = status.HTTP_404_NOT_FOUND
        msg = exc.detail

    return JSONResponse(status_code=code, content={"message": msg})


if __name__ == "__main__":
    # For debugging only
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
