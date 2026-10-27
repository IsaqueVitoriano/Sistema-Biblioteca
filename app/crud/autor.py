from sqlalchemy import select
from sqlalchemy.orm import Session

from app.utils.util import commit_or_conflict, get_or_404
from app.models.models import Autor, Livro, livro_autor
from app.schemas.entidades import AutorEntrada


def criar_autor(dados: AutorEntrada, session: Session):
    autor = Autor(nome=dados.nome)

    session.add(autor)
    commit_or_conflict(session)
    session.refresh(autor)
    return autor


def listar_autores(session: Session):
    return session.scalars(select(Autor)).all()


def obter_autor(autor_id: str, session: Session):
    return get_or_404(session, Autor, autor_id)


def atualizar_autor(autor_id: str, dados: AutorEntrada, session: Session):
    autor = get_or_404(session, Autor, autor_id)
    autor.nome = dados.nome

    commit_or_conflict(session)
    session.refresh(autor)
    return autor


def apagar_autor(autor_id: str, session: Session):
    autor = get_or_404(session, Autor, autor_id)

    session.delete(autor)
    commit_or_conflict(session)
    return {"mensagem": "Autor apagado com sucesso" }


def listar_livros_por_autor(session: Session, autor_id: str):
    consulta = (
        select(Livro)
        .join(livro_autor, Livro.id == livro_autor.c.livro_id)
        .where(livro_autor.c.autor_id == autor_id)
    )

    return session.execute(consulta).scalars().all()