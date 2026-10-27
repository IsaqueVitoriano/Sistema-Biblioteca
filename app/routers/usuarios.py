from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_session
from app.models.models import UsuarioEntrada, UsuarioSaida

from app.crud.usuario import listar_usuarios, criar_usuarios, atualizar_usuario, apagar_usuario

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("/", response_model=list[dict[str, str]])
def listar(session :Session = Depends(get_session)):
    return listar_usuarios(session)

@router.get("/{id}", response_model=UsuarioSaida)
def obter_usuario_id(id :str, session :Session = Depends(get_session)):
    return obter_usuario_id(id, session)

@router.put("/{id}", response_model=UsuarioSaida)
def atualizar_usuario_id(id :str,usuario_atualizado : UsuarioEntrada, session :Session = Depends(get_session)):
    return atualizar_usuario(id, usuario_atualizado, session)

@router.post("/", response_model=UsuarioSaida)
def criar_usuario(novo_usuario :UsuarioEntrada, session :Session = Depends(get_session)):
    return criar_usuarios(novo_usuario, session)

@router.delete("/{id}", response_model=UsuarioSaida)
def remover_usuario(id :str, session :Session = Depends(get_session)):
    return apagar_usuario(id, session)