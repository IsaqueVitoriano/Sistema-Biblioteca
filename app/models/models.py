from datetime import datetime, date
from enum import Enum

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from pydantic import BaseModel, Field

class SituacaoEmprestimo(Enum, str):
        DANIFICADO = 'DANIFICADO'
        DISPONIVEL = 'DISPONIVEL'
        EM_EMPRESTIMO = 'EM_EMPRESTIMO'

class TipoUsuario(Enum, str):
    BIBLIOTECARIO='BIBLIOTECARIO'
    ALUNO='ALUNO'
    ADMINISTRADOR='ADMINISTRADOR'

class Emprestimo(BaseModel):
    id: Mapped[str] = mapped_column(primary_key=True, description='Id da emprestimo')

    situacao_emprestimo: Mapped[SituacaoEmprestimo] = mapped_column(
        gt=SituacaoEmprestimo.DISPONIVEL,
        description= 'status do emprestimo'
    )

    data_emprestimo: Mapped[datetime] = mapped_column(
        gt=datetime.now(),
        description='Data da emprestimo'
    )

    data_devolucao_efetiva: Mapped[datetime] | Mapped[None] = mapped_column(
        gt=None,
        description='Data efetiva do emprestimo'
    )

    data_prazo_devolucao_efetiva: Mapped[datetime] | Mapped[None] = mapped_column(
        gt=None,
        description='Data prazo do emprestimo'
    )

    id_usuario: Mapped[str] = mapped_column(
        description='Id do usuario do emprestimo'
    )

    id_exemplar: Mapped[str] = mapped_column(
        description='Id do exemplar do emprestimo'
    )

class Usuario(BaseModel):
    id: Mapped[str] = mapped_column(description='Id do usuario')

    nome: Mapped[str] = mapped_column(String(100), nullable=False, description='Nome do usuario')

    data_criacao: Mapped[datetime] = mapped_column(gt=datetime.now(), description="data de criacao do usuario")

    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False, description='Email do usuario')

    matricula: Mapped[str] = mapped_column(nullable=False, description='Matricula do usuario')

    tipo_usuario: Mapped[TipoUsuario] | Mapped[None] = mapped_column(description='Tipo do usuario')

class Editora(BaseModel):
    id: Mapped[str] = mapped_column(description='Id do editora')

    nome: Mapped[str] = mapped_column(String(100), description='Nome do editora')

class Autor(BaseModel):
    id: Mapped[str] = mapped_column(description='Id do autor')

    nome: Mapped[str] = mapped_column(String(100), description='Nome do autor')

class Categoria(BaseModel):
    id: Mapped[str] = mapped_column(description='Id do categoria')

    nome: Mapped[str] = mapped_column(String(50), description='Nome do categoria')

class Livro(BaseModel):
    id: Mapped[str] = mapped_column(description='Id do livro')

    titulo: Mapped[str] = mapped_column(String(60), description='Titulo do livro')

    ano_publicacao: Mapped[date] = mapped_column(description='Ano de publicacao do livro')

    id_editora: Mapped[str] = mapped_column(description='Id do editora do livro')

    id_categoria: Mapped[str] = mapped_column(description='Id do editora do livro')

    autores: Mapped[list] = mapped_column(description='Autores do livro')