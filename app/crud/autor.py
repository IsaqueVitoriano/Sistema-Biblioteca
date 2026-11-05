from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.utils.util import commit_or_conflict, get_or_404
from app.models.models import Autor, Livro, livro_autor, Categoria
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
    return {"mensagem": "Autor apagado com sucesso"}


def listar_livros_por_autor(session: Session, autor_id: str):
    consulta = (
        select(Livro)
        .join(livro_autor, Livro.id == livro_autor.c.livro_id)
        .where(livro_autor.c.autor_id == autor_id)
    )

    return session.execute(consulta).scalars().all()


def livros_por_categoria(session: Session):
    consulta_complexa = (
        (
            select(func.count(Livro.id), Categoria.nome, Autor.nome)
            .join(Categoria, Livro.id_categoria == Categoria.id)
            .join(livro_autor, Livro.id == livro_autor.c.livro_id)
            .join(Autor, livro_autor.c.autor_id == Autor.id)
        )
        .group_by(Categoria.nome, Autor.nome)
        .order_by(func.count(Livro.id).desc(), Autor.nome)
    )

    resultados = session.execute(consulta_complexa).all()

    ranking = []
    for quantidade, categoria, autor in resultados:
        ranking.append(
            {"qtd_obras": quantidade, "nome_categoria": categoria, "nome_autor": autor}
        )

    return ranking
