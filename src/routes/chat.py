
from fastapi import APIRouter
from data.index_storage import index_storage

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)


@router.post("/")
async def chat(question: str):
    query_engine = index_storage.index().as_query_engine()
    response = query_engine.query(question)
    return {"answer": response}





