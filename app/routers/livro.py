from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.schemas.paginacao import LivroPaginadoSaida
from app.crud.livro import listar_livros
from app.database import get_session

router = APIRouter(prefix="/livros", tags=["Livros"])


@router.get("/", response_model=LivroPaginadoSaida)
def listar(
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamanho da página"),
    session: Session = Depends(get_session),
):
    return listar_livros(session=session, page=page, page_size=page_size)
