from typing import TypeVar

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.models import Base


ModelType = TypeVar("ModelType", bound=Base)


def get_or_404(session: Session, model: type[ModelType], id: str) -> ModelType:
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
            detail="A operação viola uma restrição de integridade do banco de dados",
        ) from error
