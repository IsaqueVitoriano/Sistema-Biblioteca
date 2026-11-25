from typing import TypeVar

from fastapi import HTTPException
from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import Base
from app.models.models import Categoria, Usuario
from app.schemas.entidades import (
    CategoriaEntrada,
    UsuarioEntrada,
)

ModelType = TypeVar("ModelType", bound=Base)


def get_usuario(
    session: Session,
    data: UsuarioEntrada,
    exclude_id: str | None = None,
) -> None:
    query = select(Usuario.id).where(
        or_(
            Usuario.email == data.email,
            Usuario.matricula == data.matricula,
            Usuario.telefone == data.telefone,
        )
    )

    if exclude_id is not None:
        query = query.where(Usuario.id != exclude_id)

    if session.scalar(query.limit(1)) is not None:
        raise HTTPException(
            status_code=409,
            detail="Já existe um usuário com esse e-mail, matrícula ou telefone",
        )


def get_categoria(
    session: Session,
    data: CategoriaEntrada,
    exclude_id: str | None = None,
) -> None:
    query = (select(Categoria.id)
             .where(Categoria.nome == data.nome))

    if exclude_id is not None:
        query = query.where(Categoria.id != exclude_id)

    if session.scalar(query.limit(1)) is not None:
        raise HTTPException(
            status_code=409,
            detail="Já existe uma categoria com esse nome"
        )


def get_or_404(session: Session, model: type[ModelType], id: str) -> ModelType:
    if not id:
        raise HTTPException(status_code=400, detail="id inválido")

    instance = session.get(model, id)
    if instance is None:
        raise HTTPException(status_code=404, detail=f"{model.__name__} não encontrado")
    return instance


def commit_or_conflict(session: Session) -> None:
    try:
        session.commit()
    except IntegrityError as error:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="A operação viola a restrição de integridade do banco de dados",
        ) from error
