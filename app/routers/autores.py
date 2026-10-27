from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.autor import (
    listar_autores,
    obter_autor,
    atualizar_autor,
    apagar_autor,
    listar_livros_por_autor
)

from app.database import get_session
from app.schemas.entidades import AutorEntrada, AutorSaida, LivroSaida

router = APIRouter(prefix="/autores", tags=["Autores"])


@router.get("/", response_model=list[AutorSaida])
def listar(session: Session = Depends(get_session)):
    return listar_autores(session)


@router.get("/{id}", response_model=AutorSaida)
def obter_autor_id(id: str, session: Session = Depends(get_session)):
    return obter_autor(id, session)


@router.put("/{id}", response_model=AutorSaida)
def atualizar_autor_id(
    id: str, autor_atualizado: AutorEntrada, session: Session = Depends(get_session)
):
    return atualizar_autor(id, autor_atualizado, session)


@router.post("/", response_model=AutorSaida)
def criar_autor(novo_autor: AutorEntrada, session: Session = Depends(get_session)):
    return criar_autor(novo_autor, session)


@router.delete("/{id}", response_model=AutorSaida)
def remover_autor(id: str, session: Session = Depends(get_session)):
    return apagar_autor(id, session)


@router.get("/{autor_id}/livros", response_model=list[LivroSaida])
def listar_livros_autor(autor_id: str, session: Session = Depends(get_session)):
    return listar_livros_por_autor(session, autor_id)
