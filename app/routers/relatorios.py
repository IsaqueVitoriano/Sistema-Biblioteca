from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud.autor import livros_por_categoria
from app.crud.categoria import categoria_com_atrasos

from app.database import get_session
from app.schemas.entidades import RankingAutorCategoriaSaida, CategoriasComMaisAtrasos

router = APIRouter(prefix="/relatorios", tags=["Relatorios"])


@router.get(
    "/obras-autores-categorias", response_model=list[RankingAutorCategoriaSaida]
)
def ranking_autor_por_categoria(session: Session = Depends(get_session)):
    return livros_por_categoria(session)


@router.get("/atrasos-categorias", response_model=list[CategoriasComMaisAtrasos])
def ranking_atrasos_por_categoria(session: Session = Depends(get_session)):
    return categoria_com_atrasos(session)
