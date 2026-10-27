from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.autor import (
    listar_autores,
    obter_autor,
    atualizar_autor,
    AutorEntrada,
    apagar_autor,
)

from app.database import get_session
from app.models.models import AutorSaida

router = APIRouter(prefix="/autores", tags=["Autores"])


@router.get("/", response_model=list[dict[str, str]])
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
