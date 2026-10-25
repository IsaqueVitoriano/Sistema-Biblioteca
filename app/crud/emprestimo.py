from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.utils.util import commit_or_conflict, get_or_404
from app.models.models import (
    Emprestimo,
    EmprestimoEntrada,
    Exemplar,
    Usuario,
)


def validar_fks(session: Session, dados: EmprestimoEntrada) -> None:
    get_or_404(session, Usuario, dados.id_usuario)
    get_or_404(session, Exemplar, dados.id_exemplar)


def criar_emprestimo(dados: EmprestimoEntrada, session: Session):
    validar_fks(session, dados)

    emprestimo = Emprestimo(**dados.model_dump())

    session.add(emprestimo)
    commit_or_conflict(session)
    session.refresh(emprestimo)
    return emprestimo


def listar_emprestimos(session: Session, page: int = 1, page_size: int = 10):
    registros_total = session.scalar(select(func.count()).select_from(Emprestimo)) or 0
    paginas_total = (registros_total + page_size - 1) // page_size

    deslocamento = (page - 1) * page_size

    consulta = select(Emprestimo).offset(deslocamento).limit(page_size)

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
