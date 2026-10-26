from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.models.models import LivroSaida, LivroEntrada
from app.schemas.paginacao import LivroPaginadoSaida
from app.crud.livro import listar_livros, obter_livro, atualizar_livro, criar_livros, apagar_livro
from app.database import get_session

router = APIRouter(prefix="/livros", tags=["Livros"])


@router.get("/", response_model=LivroPaginadoSaida)
def listar(
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamanho da página"),
    titulo: str | None = Query(None, description="Filtrar por título do livro"),
    id_categoria: str | None = Query(None, description="Filtrar por ID da Categoria"),
    id_editora: str | None = Query(None, description="Filtrar por ID da Editora"),
    ano_publicacao: int | None = Query(None, description="Filtrar por ano (ex: 1990)"),
    session: Session = Depends(get_session),
):
    return listar_livros(
        session=session,
        page=page,
        page_size=page_size,
        titulo=titulo,
        id_categoria=id_categoria,
        id_editora=id_editora,
        ano_publicacao=ano_publicacao,
    )


# @router.get("/", response_model=list[LivroSaida])
# def listar(session :Session = Depends(get_session)):
#     return listar_livros(session)

@router.get("/{id}", response_model=LivroSaida)
def obter_livro_id(livro_id: str, session :Session = Depends(get_session)):
    return obter_livro(livro_id, session)

@router.put("/{id}", response_model=LivroSaida)
def atualizar_livro_id(id :str, livro_atualizado: LivroEntrada, session :Session = Depends(get_session)):
    return atualizar_livro(id, livro_atualizado, session)

@router.post("/", response_model=LivroSaida)
def criar_livro(novo_livro: LivroEntrada, session :Session = Depends(get_session)):
    return criar_livros(novo_livro, session)

@router.delete("/{id}", response_model=dict[str, str])
def deletar_livro_id(id :str, session :Session = Depends(get_session)):
    return apagar_livro(id, session)