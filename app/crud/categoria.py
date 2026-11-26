from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.utils.util import commit_or_conflict, get_or_404, get_categoria
from app.models.models import Categoria, Emprestimo, Exemplar, Livro
from app.schemas.entidades import CategoriaEntrada, CategoriaSaida, RemocaoSaida


def criar_categorias(dados: CategoriaEntrada, session: Session):
    get_categoria(session, dados)

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
    get_categoria(session, dados, exclude_id=categoria_id)
    categoria.nome = dados.nome

    commit_or_conflict(session)
    session.refresh(categoria)
    return categoria


def apagar_categoria(categoria_id: str, session: Session):
    categoria = get_or_404(session, Categoria, categoria_id)

    dados_categoria = CategoriaSaida.model_validate(categoria)
    session.delete(categoria)
    commit_or_conflict(session)

    return RemocaoSaida(
        mensagem="Categoria apagada com sucesso!", dados=dados_categoria
    )


def categoria_com_atrasos(session: Session):
    consulta_complexa = (
        (
            select(Categoria.nome, func.count(Emprestimo.id))
            .join(Livro, Livro.id_categoria == Categoria.id)
            .join(Exemplar, Livro.id == Exemplar.id_livro)
            .join(Emprestimo, Emprestimo.id_exemplar == Exemplar.id)
            .where(Emprestimo.situacao_emprestimo == "ATRASADO")
        )
        .group_by(Categoria.nome)
        .order_by(func.count(Emprestimo.id).desc())
    )

    resultados = session.execute(consulta_complexa).all()

    atrasos_categoria = []
    for nome_categoria, qtd_atrasos in resultados:
        atrasos_categoria.append(
            {"nome_categoria": nome_categoria, "qtd_atrasos": qtd_atrasos}
        )

    return atrasos_categoria
