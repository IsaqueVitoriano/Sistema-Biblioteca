from sqlalchemy.orm import Session

from app.database import get_session
from app.schemas.entidades import Estatistica
from fastapi import APIRouter, Depends
from app.crud.estatistica import gerar_estatisticas

router = APIRouter(prefix="/estatisticas", tags=["Estatisticas"])

@router.get("/estatisticas", response_model=Estatistica)
def get_estatisticas(session: Session = Depends(get_session)):
    return gerar_estatisticas(session)