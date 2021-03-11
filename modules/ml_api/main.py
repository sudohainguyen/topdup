# import time
# import traceback

from fastapi import FastAPI, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from modules.ml.document_store.faiss import FAISSDocumentStore
from modules.ml_api.models import AllPairsEntry, CompareEntry, QueryResult

tags_metadata = [
    {
        "name": "get",
        "description": "Properly do nothing now",
    },
    {
        "name": "all_pairs",
        "description": "Find all similar document pairs with sim_score above threshold",
    },
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
    "/all_pairs",
    response_model=QueryResult,
    status_code=status.HTTP_200_OK,
    tags=["all_pairs"],
)
def find_all_pairs(entry: AllPairsEntry, response: Response):
    # cand_dim = 768
    # sql_url = "postgresql+psycopg2://user:pwd@host/topdup_articles"

    # print("Init DocumentStore")
    # document_store = FAISSDocumentStore(
    #     sql_url=sql_url, vector_dim=cand_dim, index_buffer_size=5000
    # )

    # document_store.get_documents_by_sim_threshold(entry.threshold)

    all_pairs = {
        "message": "Successfully requested ML-API [all_pairs]",
        "result": [
            {
                "id": "concat articleAId & articleBId",
                "articleA": "title of articleA",
                "articleAId": "id of articleA",
                "domainA": "domain of articleA",
                "authorA": "author of articleA",
                "createdDateA": "created date of articleA",
                "articleB": "title of articleB",
                "articleBId": "id of articleB",
                "domainB": "domain of articleB",
                "authorB": "author of articleB",
                "createdDateB": "created date of articleB",
                "simScore": "similarity score between articleA & articleB",
            }
        ],
    }

    return all_pairs


@app.post(
    "/compare",
    response_model=QueryResult,
    status_code=status.HTTP_200_OK,
    tags=["compare"],
)
def compare(entry: CompareEntry, response: Response):
    pass


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request, exc):
    msg = ", ".join([f'{err["loc"]}: {err["msg"]}' for err in exc.errors()])
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": msg},
    )


@app.exception_handler(StarletteHTTPException)
def http_exception_handler(request, exc):
    code = status.HTTP_400_BAD_REQUEST
    msg = str(exc)
    if exc.status_code == 404:
        code = status.HTTP_404_NOT_FOUND
        msg = exc.detail

    return JSONResponse(
        status_code=code,
        content={"message": msg},
    )


if __name__ == "__main__":
    # For debugging only
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
