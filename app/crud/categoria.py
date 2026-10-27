from sqlalchemy import select
from sqlalchemy.orm import Session

from app.utils.util import commit_or_conflict, get_or_404
from app.models.models import Categoria
from app.schemas.entidades import CategoriaEntrada

def criar_categoria(dados: CategoriaEntrada, session: Session):
    categoria = Categoria(nome=dados.nome)

    session.add(categoria)
    commit_or_conflict(session)
    session.refresh(categoria)
    return categoria


def listar_categorias(session: Session):
    return session.scalars(select(Categoria)).all()


def obter_categoria(categoria_id: str, session: Session):
    return get_or_404(session, Categoria, categoria_id)


def atualizar_categoria(categoria_id: str, dados: CategoriaEntrada, session: Session):
    categoria = get_or_404(session, Categoria, categoria_id)
    categoria.nome = dados.nome

    commit_or_conflict(session)
    session.refresh(categoria)
    return categoria


def apagar_categoria(categoria_id: str, session: Session):
    categoria = get_or_404(session, Categoria, categoria_id)

    session.delete(categoria)
    commit_or_conflict(session)
    return {"mensagem": "Categoria apagada com sucesso" }
