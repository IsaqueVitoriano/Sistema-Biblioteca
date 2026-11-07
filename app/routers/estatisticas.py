from app.schemas.entidades import Estatistica
from fastapi import APIRouter

router = APIRouter(prefix="/estatisticas", tags=["Estatisticas"])

@router.get("/estatisticas", response_model=Estatistica)
def get_estatisticas():
    return