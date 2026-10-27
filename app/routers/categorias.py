from fastapi import APIRouter, Depends
from app.crud.categoria import (
    listar_categorias,
    atualizar_categoria,
    obter_categoria,
    apagar_categoria,
)
from sqlalchemy.orm import Session
from app.database import get_session
from app.schemas.entidades import CategoriaSaida, CategoriaEntrada

router = APIRouter(prefix="/categorias", tags=["Categorias"])


@router.get("/", response_model=list[CategoriaSaida])
def listar(session: Session = Depends(get_session)):
    return listar_categorias(session)


@router.get("/{id}", response_model=CategoriaSaida)
def obter_categoria_id(categoria_id: str, session: Session = Depends(get_session)):
    return obter_categoria(categoria_id, session)


@router.put("/{id}", response_model=CategoriaSaida)
def atualizar_categoria_id(
    id: str,
    categoria_atualizada: CategoriaEntrada,
    session: Session = Depends(get_session),
):
    return atualizar_categoria(id, categoria_atualizada, session)


@router.post("/", response_model=CategoriaSaida)
def criar_categoria(
    nova_categoria: CategoriaEntrada, session: Session = Depends(get_session)
):
    return criar_categoria(nova_categoria, session)


@router.delete("/{id}", response_model=dict[str, str])
def deletar_categoria_id(id: str, session: Session = Depends(get_session)):
    return apagar_categoria(id, session)
