from fastapi import APIRouter
from app.models.schemas import AskRequest, AskResponse
router = APIRouter()

@router.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest):
    raise NotImplementedError
