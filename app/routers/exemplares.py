from fastapi import APIRouter, Depends
from app.crud.exemplar import *
from app.database import get_session
from app.schemas.entidades import ExemplarSaida

router = APIRouter(prefix="/exemplares", tags=["Exemplares"])


@router.get("/", response_model=list[ExemplarSaida])
def listar(session: Session = Depends(get_session)):
    return listar_exemplares(session)


@router.get("/{id}", response_model=ExemplarSaida)
def obter_exemplar_id(exemplar_id: str, session: Session = Depends(get_session)):
    return obter_exemplar(exemplar_id, session)


@router.put("/{id}", response_model=ExemplarSaida)
def atualizar_exemplar_id(
    id: str,
    exemplar_atualizado: ExemplarEntrada,
    session: Session = Depends(get_session),
):
    return atualizar_exemplar(id, exemplar_atualizado, session)


@router.post("/", response_model=ExemplarSaida)
def criar_exemplar(
    novo_exemplar: ExemplarEntrada, session: Session = Depends(get_session)
):
    return criar_exemplares(novo_exemplar, session)


@router.delete("/{id}", response_model=dict[str, str])
def deletar_exemplar_id(id: str, session: Session = Depends(get_session)):
    return apagar_exemplar(id, session)
