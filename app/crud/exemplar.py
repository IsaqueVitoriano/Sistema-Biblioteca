from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.utils.util import commit_or_conflict, get_or_404
from app.models.models import Exemplar, Livro, SituacaoExemplar
from app.schemas.entidades import ExemplarEntrada, ExemplarSaida, RemocaoSaida


def criar_exemplares(dados: ExemplarEntrada, session: Session):
    get_or_404(session, Livro, dados.id_livro)

    exemplar = Exemplar(
        situacao=dados.situacao,
        id_livro=dados.id_livro
    )

    session.add(exemplar)
    commit_or_conflict(session)
    session.refresh(exemplar)
    return exemplar

def listar_exemplares(session: Session):
    return session.scalars(select(Exemplar)).all()


def obter_exemplar(exemplar_id: str, session: Session):
    return get_or_404(session, Exemplar, exemplar_id)


def atualizar_exemplar(exemplar_id: str, dados: ExemplarEntrada, session: Session):
    exemplar = get_or_404(session, Exemplar, exemplar_id)
    get_or_404(session, Livro, dados.id_livro)

    exemplar.situacao = dados.situacao
    exemplar.id_livro = dados.id_livro

    commit_or_conflict(session)
    session.refresh(exemplar)
    return exemplar


def apagar_exemplar(exemplar_id: str, session: Session):
    exemplar = get_or_404(session, Exemplar, exemplar_id)

    dados_exemplar = ExemplarSaida.model_validate(exemplar)
    session.delete(exemplar)
    commit_or_conflict(session)

    return RemocaoSaida(
        mensagem="Exemplar apagado com sucesso!", dados=dados_exemplar
    )
