from fastapi import APIRouter, Depends
from app.crud.editora import *
from app.database import get_session
from app.schemas.entidades import EditoraSaida

router = APIRouter(prefix="/editoras", tags=["Editoras"])


@router.get("/", response_model=list[EditoraSaida])
def listar(session: Session = Depends(get_session)):
    return listar_editoras(session)


@router.get("/{id}", response_model=EditoraSaida)
def obter_editora_id(editora_id: str, session: Session = Depends(get_session)):
    return obter_editora(editora_id, session)


@router.put("/{id}", response_model=EditoraSaida)
def atualizar_editora_id(
    id: str, editora_atualizada: EditoraEntrada, session: Session = Depends(get_session)
):
    return atualizar_editora(id, editora_atualizada, session)


@router.post("/", response_model=EditoraSaida)
def criar_editora(
    editora_atualizada: EditoraEntrada, session: Session = Depends(get_session)
):
    return criar_editoras(editora_atualizada, session)


@router.delete("/{id}", response_model=dict[str, str])
def deletar_editora_id(id: str, session: Session = Depends(get_session)):
    return apagar_editora(id, session)
