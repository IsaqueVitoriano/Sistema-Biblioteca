from sqlalchemy import select
from sqlalchemy.orm import Session

from app.utils.util import commit_or_conflict, get_or_404
from app.models.models import Editora, EditoraEntrada


def criar_editoras(dados: EditoraEntrada, session: Session):
    editora = Editora(nome=dados.nome)
    session.add(editora)

    commit_or_conflict(session)
    session.refresh(editora)
    return editora


def listar_editoras(session: Session):
    return session.scalars(select(Editora)).all()


def obter_editora(editora_id: str, session: Session):
    return get_or_404(session, Editora, editora_id)


def atualizar_editora(editora_id: str, dados: EditoraEntrada, session: Session):
    editora = get_or_404(session, Editora, editora_id)
    editora.nome = dados.nome

    commit_or_conflict(session)
    session.refresh(editora)
    return editora


def apagar_editora(editora_id: str, session: Session):
    editora = get_or_404(session, Editora, editora_id)

    session.delete(editora)
    commit_or_conflict(session)
    return {"mensagem": "Editora apagada com sucesso" }
