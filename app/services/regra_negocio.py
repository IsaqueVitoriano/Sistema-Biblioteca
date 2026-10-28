from fastapi import HTTPException
from app.models.models import SituacaoExemplar, SituacaoEmprestimo, Exemplar, Emprestimo
from datetime import datetime

def verificar_disponibilidade(exemplar: Exemplar):
    if not exemplar:
        raise HTTPException(
            status_code=404,
            detail="Exemplar não encontrado."
        )

    if exemplar.situacao != SituacaoExemplar.DISPONIVEL:
        raise HTTPException(
            status_code=400,
            detail="Exemplar indisponível para empréstimo."
        )


def impedir_emprestimo_duplicado(exemplar_id: str, emprestimos: list[Emprestimo]):
    emprestimo_ativo = any(
        emp.id_exemplar == exemplar_id
        and not emp.data_devolucao_efetiva
        and emp.situacao_emprestimo != SituacaoEmprestimo.DEVOLVIDO
        for emp in emprestimos
    )

    if emprestimo_ativo:
        raise HTTPException(
            status_code=400,
            detail="Este exemplar já possui um empréstimo ativo."
        )


def validar_periodo_devolucao(data_emprestimo: datetime, data_prazo_devolucao: datetime):
    if not data_emprestimo or not data_prazo_devolucao:
        raise HTTPException(
            status_code=400,
            detail="Datas de empréstimo e devolução são obrigatórias."
        )

    if data_prazo_devolucao <= data_emprestimo:
        raise HTTPException(
            status_code=400,
            detail="O prazo de devolução deve ser posterior à data do empréstimo."
        )