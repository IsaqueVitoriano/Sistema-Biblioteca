from fastapi import APIRouter, Depends, Query

from app.crud.emprestimo import *
from app.database import get_session
from app.models.models import EmprestimoSaida
from app.schemas.paginacao import EmprestimoPaginadoSaida

router = APIRouter(prefix="/emprestimos", tags=["Empréstimos"])


@router.get("/", response_model=EmprestimoPaginadoSaida)
def listar(
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamanho da página"),
    id_usuario: str | None = Query(None, description="ID do leitor"),
    id_exemplar: str | None = Query(None, description="ID do exemplar"),
    situacao_emprestimo: SituacaoEmprestimo | None = Query(
        None, description="Status do empréstimo"
    ),
    session: Session = Depends(get_session),
):
    return listar_emprestimos(
        session=session,
        page=page,
        page_size=page_size,
        id_usuario=id_usuario,
        id_exemplar=id_exemplar,
        situacao_emprestimo=situacao_emprestimo,
    )

#
# @router.get("/", response_model=list[EmprestimoSaida])
# def listar(session :Session = Depends(get_session)):
#     return listar_emprestimos(session)

@router.get("/{id}", response_model=EmprestimoSaida)
def obter_emprestimo_id(emprestimo_id: str, session :Session = Depends(get_session)):
    return obter_emprestimo(emprestimo_id, session)

@router.put("/{id}", response_model=EmprestimoSaida)
def atualizar_emprestimo_id(id :str, exemplar_atualizado: EmprestimoEntrada, session :Session = Depends(get_session)):
    return atualizar_emprestimo(id, exemplar_atualizado, session)

@router.post("/", response_model=EmprestimoSaida)
def criar_emprestimo(novo_emprestimo: EmprestimoEntrada, session :Session = Depends(get_session)):
    return criar_emprestimos(novo_emprestimo, session)

@router.delete("/{id}", response_model=dict[str, str])
def deletar_emprestimos_id(id :str, session :Session = Depends(get_session)):
    return apagar_emprestimo(id, session)