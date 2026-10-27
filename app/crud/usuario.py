from sqlalchemy import select
from sqlalchemy.orm import Session

from app.utils.util import commit_or_conflict, get_or_404
from app.models.models import Usuario, UsuarioEntrada, UsuarioSaida


def criar_usuarios(dados: UsuarioEntrada, session: Session):
    usuario = Usuario(**dados.model_dump())

    session.add(usuario)
    commit_or_conflict(session)
    session.refresh(usuario)

    return usuario


def listar_usuarios(session: Session):
    return session.scalars(select(Usuario)).all()


def obter_usuario(usuario_id: str, session: Session):
    return get_or_404(session, Usuario, usuario_id)


def atualizar_usuario(usuario_id: str, dados: UsuarioEntrada, session: Session):
    usuario = get_or_404(session, Usuario, usuario_id)

    for campo, valor in dados.model_dump().items():
        setattr(usuario, campo, valor)

    commit_or_conflict(session)
    session.refresh(usuario)
    return usuario


def apagar_usuario(usuario_id: str, session: Session):
    usuario = get_or_404(session, Usuario, usuario_id)

    session.delete(usuario)
    commit_or_conflict(session)
    return {"mensagem": "Usuario apagado com sucesso"}
