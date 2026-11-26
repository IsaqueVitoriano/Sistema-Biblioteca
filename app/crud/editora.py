from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.utils.util import commit_or_conflict, get_or_404
from app.models.models import Editora
from app.schemas.entidades import EditoraEntrada, EditoraSaida, RemocaoSaida


def criar_editoras(dados: EditoraEntrada, session: Session):
    nome_limpo = dados.nome.strip()
    editora_existente = session.scalars(
        select(Editora.id).where(func.lower(Editora.nome) == nome_limpo.lower())
    ).first()

    if editora_existente:
        raise HTTPException(
            status_code=409, detail="Já existe uma editora com esse nome"
        )

    editora = Editora(nome=nome_limpo)
    session.add(editora)

    commit_or_conflict(session)
    session.refresh(editora)
    return editora


def listar_editoras(session: Session):
    return session.scalars(select(Editora)).all()


def obter_editora(editora_id: str, session: Session):
    return get_or_404(session, Editora, editora_id)


def atualizar_editora(editora_id: str, dados: EditoraEntrada, session: Session):
    editora = get_or_404(session, Editora, editora_id)
    nome_limpo = dados.nome.strip()

    editora_existente = session.scalars(
        select(Editora.id).where(
            func.lower(Editora.nome) == nome_limpo.lower(),
            Editora.id != editora_id,
        )
    ).first()

    if editora_existente:
        raise HTTPException(
            status_code=409, detail="Já existe outra editora com esse nome"
        )

    editora.nome = nome_limpo

    commit_or_conflict(session)
    session.refresh(editora)
    return editora


def apagar_editora(editora_id: str, session: Session):
    editora = get_or_404(session, Editora, editora_id)

    dados_editora = EditoraSaida.model_validate(editora)
    session.delete(editora)
    commit_or_conflict(session)

    return RemocaoSaida(mensagem="Editora apagada com sucesso!", dados=dados_editora)
