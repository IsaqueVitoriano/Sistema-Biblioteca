from sqlalchemy import select, func, extract
from sqlalchemy.orm import Session, selectinload

from app.utils.util import commit_or_conflict, get_or_404
from app.models.models import Autor, Categoria, Editora, Livro, LivroEntrada


def criar_livro(dados: LivroEntrada, session: Session):
    get_or_404(session, Editora, dados.id_editora)
    get_or_404(session, Categoria, dados.id_categoria)

    if dados.id_autores:
        autores = session.scalars(
            select(Autor).where(Autor.id.in_(dados.id_autores))
        ).all()
    else:
        autores = []

    id_autores_encontrados = {autor.id for autor in autores}

    id_autor_inexistente = next(
        (
            autor_id
            for autor_id in dados.id_autores
            if autor_id not in id_autores_encontrados
        ),
        None,
    )

    if id_autor_inexistente is not None:
        get_or_404(session, Autor, id_autor_inexistente)

    livro = Livro(
        titulo=dados.titulo,
        ano_publicacao=dados.ano_publicacao,
        id_editora=dados.id_editora,
        id_categoria=dados.id_categoria,
        autores=autores,
    )

    session.add(livro)
    commit_or_conflict(session)
    session.refresh(livro)
    return livro


def listar_livros(
    session: Session,
    page: int = 1,
    page_size: int = 10,
    titulo: str | None = None,
    id_categoria: str | None = None,
    id_editora: str | None = None,
    ano_publicacao: int | None = None,
):
    condicoes = []
    if titulo:
        condicoes.append(Livro.titulo.ilike(f"%{titulo}%"))
    if id_categoria:
        condicoes.append(Livro.id_categoria == id_categoria)
    if id_editora:
        condicoes.append(Livro.id_editora == id_editora)
    if ano_publicacao:
        condicoes.append(extract("year", Livro.ano_publicacao) == ano_publicacao)

    consulta_contador = select(func.count()).select_from(Livro)
    if condicoes:
        consulta_contador = consulta_contador.where(*condicoes)

    registros_total = session.scalar(consulta_contador) or 0
    paginas_total = (registros_total + page_size - 1) // page_size

    deslocamento = (page - 1) * page_size

    consulta = select(Livro).options(selectinload(Livro.autores))

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


def obter_livro(livro_id: str, session: Session):
    return session.scalar(
        select(Livro).where(Livro.id == livro_id).options(selectinload(Livro.autores))
    ) or get_or_404(session, Livro, livro_id)


def atualizar_livro(livro_id: str, dados: LivroEntrada, session: Session):
    livro = get_or_404(session, Livro, livro_id)

    get_or_404(session, Editora, dados.id_editora)
    get_or_404(session, Categoria, dados.id_categoria)

    if dados.id_autores:
        autores = session.scalars(
            select(Autor).where(Autor.id.in_(dados.id_autores))
        ).all()
    else:
        autores = []

    autores_encontrados = {autor.id for autor in autores}

    autor_inexistente = next(
        (
            autor_id
            for autor_id in dados.id_autores
            if autor_id not in autores_encontrados
        ),
        None,
    )

    if autor_inexistente is not None:
        get_or_404(session, Autor, autor_inexistente)

    livro.titulo = dados.titulo
    livro.ano_publicacao = dados.ano_publicacao
    livro.id_editora = dados.id_editora
    livro.id_categoria = dados.id_categoria
    livro.autores = autores

    commit_or_conflict(session)
    session.refresh(livro)
    return livro


def apagar_livro(livro_id: str, session: Session):
    livro = get_or_404(session, Livro, livro_id)

    session.delete(livro)
    commit_or_conflict(session)
    return {"mensagem": "Livro apagado com sucesso!"}
