from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.schemas.paginacao import EmprestimoPaginadoSaida
from app.crud.emprestimo import listar_emprestimos
from app.database import get_session

router = APIRouter(prefix="/emprestimos", tags=["Empréstimos"])


@router.get("/", response_model=EmprestimoPaginadoSaida)
def listar(
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamanho da página"),
    session: Session = Depends(get_session),
):
    return listar_emprestimos(session=session, page=page, page_size=page_size)
