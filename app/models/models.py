from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

class SituacaoEmprestimo(Enum, str):
        DANIFICADO = 'DANIFICADO'
        DISPONIVEL = 'DISPONIVEL'
        EM_EMPRESTIMO = 'EM_EMPRESTIMO'


class Emprestimo(BaseModel):
    id: str = Field(
                    description='Id da emprestimo'
                    )

    situacao_emprestimo: SituacaoEmprestimo = Field(
                                                gt=SituacaoEmprestimo.DISPONIVEL,
                                                description= 'status do emprestimo'
                                                )

    data_emprestimo: datetime = Field(
                                    gt=datetime.now(),
                                    description='Data da emprestimo'
                                     )

    data_devolucao_efetiva: datetime | None = Field(
                                                    gt=None,
                                                    description='Data efetiva do emprestimo'
                                                    )

    data_prazo_devolucao_efetiva: datetime | None = Field(
                                                        gt=None,
                                                        description='Data prazo do emprestimo'
                                                        )

    id_usuario: str = Field(
                    description='Id do usuario do emprestimo'
                    )

    id_exemplar: str = Field(
                    description='Id do exemplar do emprestimo'
                    )


