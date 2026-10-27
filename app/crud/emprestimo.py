from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.utils.util import commit_or_conflict, get_or_404
from app.models.models import (
    Emprestimo,
    Exemplar,
    Usuario,
    SituacaoEmprestimo,
)
from app.schemas.entidades import EmprestimoEntrada


def validar_fks(session: Session, dados: EmprestimoEntrada) -> None:
    get_or_404(session, Usuario, dados.id_usuario)
    get_or_404(session, Exemplar, dados.id_exemplar)


def criar_emprestimos(dados: EmprestimoEntrada, session: Session):
    validar_fks(session, dados)

    emprestimo = Emprestimo(**dados.model_dump())

    session.add(emprestimo)
    commit_or_conflict(session)
    session.refresh(emprestimo)
    return emprestimo


def listar_emprestimos(
    session: Session,
    page: int = 1,
    page_size: int = 10,
    id_usuario: str | None = None,
    id_exemplar: str | None = None,
    situacao_emprestimo: SituacaoEmprestimo | None = None,
):
    condicoes = []
    if id_usuario:
        condicoes.append(Emprestimo.id_usuario == id_usuario)
    if id_exemplar:
        condicoes.append(Emprestimo.id_exemplar == id_exemplar)
    if situacao_emprestimo:
        condicoes.append(Emprestimo.situacao_emprestimo == situacao_emprestimo)

    consulta_contador = select(func.count()).select_from(Emprestimo)
    if condicoes:
        consulta_contador = consulta_contador.where(*condicoes)

    registros_total = session.scalar(consulta_contador) or 0
    paginas_total = (registros_total + page_size - 1) // page_size

    deslocamento = (page - 1) * page_size

    consulta = select(Emprestimo)
    if condicoes:
        consulta = consulta.where(*condicoes)

    consulta = consulta.offset(deslocamento).limit(page_size)

    resultados = session.scalars(consulta).all()

    return {
        "dados": resultados,
        "paginacao": {
            "registros_total": registros_total,
            "paginas_total": paginas_total,
            "pagina_atual": page,
            "pagina_tamanho": page_size,
        },
    }


def obter_emprestimo(emprestimo_id: str, session: Session):
    return get_or_404(session, Emprestimo, emprestimo_id)


def atualizar_emprestimo(
    emprestimo_id: str,
    dados: EmprestimoEntrada,
    session: Session,
):
    validar_fks(session, dados)
    emprestimo = get_or_404(session, Emprestimo, emprestimo_id)

    for campo, valor in dados.model_dump().items():
        setattr(emprestimo, campo, valor)

    commit_or_conflict(session)
    session.refresh(emprestimo)
    return emprestimo


def apagar_emprestimo(emprestimo_id: str, session: Session):
    emprestimo = get_or_404(session, Emprestimo, emprestimo_id)

    session.delete(emprestimo)
    commit_or_conflict(session)
    return {"mensagem": "Emprestimo apagado com sucesso"}
