from fastapi import APIRouter, Depends, Query, status

from app.crud.emprestimo import (
    listar_emprestimos,
    Session,
    SituacaoEmprestimo,
    atualizar_emprestimo,
    EmprestimoEntrada,
    criar_emprestimos,
    obter_emprestimo,
    apagar_emprestimo,
)
from app.database import get_session
from app.schemas.entidades import EmprestimoSaida, EmprestimoPaginadoSaida, RemocaoSaida

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


@router.get("/{id}", response_model=EmprestimoSaida)
def obter_emprestimo_id(id: str, session: Session = Depends(get_session)):
    return obter_emprestimo(id, session)


@router.put("/{id}", response_model=EmprestimoSaida)
def atualizar_emprestimo_id(
    id: str,
    emprestimo_atualizado: EmprestimoEntrada,
    session: Session = Depends(get_session),
):
    return atualizar_emprestimo(id, emprestimo_atualizado, session)


@router.post("/", response_model=EmprestimoSaida, status_code=status.HTTP_201_CREATED)
def criar_emprestimo(
    novo_emprestimo: EmprestimoEntrada, session: Session = Depends(get_session)
):
    return criar_emprestimos(novo_emprestimo, session)


@router.delete("/{id}", response_model=RemocaoSaida[EmprestimoSaida])
def deletar_emprestimos_id(id: str, session: Session = Depends(get_session)):
    return apagar_emprestimo(id, session)
