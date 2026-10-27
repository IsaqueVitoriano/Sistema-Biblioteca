from datetime import datetime, date
from enum import Enum as PythonEnum
from uuid import uuid4

from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy import String, Enum as SQLAlchemyEnum, ForeignKey, Table, Column


class Base(DeclarativeBase):
    pass


livro_autor = Table(
    "livro_autor",
    Base.metadata,
    Column("livro_id", ForeignKey("livro.id"), primary_key=True),
    Column("autor_id", ForeignKey("autor.id"), primary_key=True),
)


class SituacaoEmprestimo(str, PythonEnum):
    DEVOLVIDO = "DEVOLVIDO"
    PENDENTE = "PENDENTE"
    ATRASADO = "ATRASADO"


class TipoUsuario(str, PythonEnum):
    SERVIDOR = "SERVIDOR"
    PROFESSOR = "PROFESSOR"
    ALUNO = "ALUNO"
    ADMINISTRADOR = "ADMINISTRADOR"


class SituacaoExemplar(str, PythonEnum):
    DISPONIVEL = "DISPONIVEL"
    DANIFICADO = "DANIFICADO"
    EM_EMPRESTIMO = "EM_EMPRESTIMO"
    RETIRADO_DE_CIRCULACAO = "RETIRADO_DE_CIRCULACAO"


class Emprestimo(Base):
    __tablename__ = "emprestimo"

    id: Mapped[str] = mapped_column(
        primary_key=True, default=lambda: str(uuid4()), comment="Id da emprestimo"
    )

    situacao_emprestimo: Mapped[SituacaoEmprestimo] = mapped_column(
        SQLAlchemyEnum(SituacaoEmprestimo, native_enum=False),
        default=SituacaoEmprestimo.PENDENTE,
        comment="status do emprestimo",
    )

    data_emprestimo: Mapped[datetime] = mapped_column(comment="Data da emprestimo")

    data_devolucao_efetiva: Mapped[datetime | None] = mapped_column(
        comment="Data efetiva do emprestimo"
    )

    data_prazo_devolucao_efetiva: Mapped[datetime | None] = mapped_column(
        comment="Data prazo do emprestimo"
    )

    id_usuario: Mapped[str] = mapped_column(
        ForeignKey("usuario.id"), comment="Id do usuario do emprestimo"
    )

    id_exemplar: Mapped[str] = mapped_column(
        ForeignKey("exemplar.id"), comment="Id do exemplar do emprestimo"
    )

    exemplar: Mapped["Exemplar"] = relationship(back_populates="emprestimos")


class Exemplar(Base):
    __tablename__ = "exemplar"

    id: Mapped[str] = mapped_column(
        primary_key=True, default=lambda: str(uuid4()), comment="Id da exemplar"
    )

    situacao: Mapped[SituacaoExemplar] = mapped_column(
        SQLAlchemyEnum(SituacaoExemplar, native_enum=False),
        default=SituacaoExemplar.DISPONIVEL,
        comment="Situacao do exemplar",
    )

    id_livro: Mapped[str] = mapped_column(ForeignKey("livro.id"), comment="Id do livro")

    emprestimos: Mapped[list["Emprestimo"]] = relationship(back_populates="exemplar")


class Usuario(Base):
    __tablename__ = "usuario"

    id: Mapped[str] = mapped_column(
        primary_key=True, default=lambda: str(uuid4()), comment="Id do usuario"
    )

    nome: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="Nome do usuario"
    )

    data_criacao: Mapped[datetime] = mapped_column(comment="data de criacao do usuario")

    email: Mapped[str] = mapped_column(
        String(150), unique=True, nullable=False, comment="Email do usuario"
    )

    matricula: Mapped[str] = mapped_column(
        unique=True, nullable=False, comment="Matricula do usuario"
    )

    tipo_usuario: Mapped[TipoUsuario | None] = mapped_column(
        SQLAlchemyEnum(TipoUsuario, native_enum=False),
        comment="Tipo do usuario",
    )


class Editora(Base):
    __tablename__ = "editora"

    id: Mapped[str] = mapped_column(
        primary_key=True, default=lambda: str(uuid4()), comment="Id do editora"
    )

    nome: Mapped[str] = mapped_column(String(100), comment="Nome do editora")


class Autor(Base):
    __tablename__ = "autor"

    id: Mapped[str] = mapped_column(
        primary_key=True, default=lambda: str(uuid4()), comment="Id do autor"
    )

    nome: Mapped[str] = mapped_column(String(100), comment="Nome do autor")

    livros: Mapped[list["Livro"]] = relationship(
        secondary=livro_autor, back_populates="autores"
    )


class Categoria(Base):
    __tablename__ = "categoria"

    id: Mapped[str] = mapped_column(
        primary_key=True, default=lambda: str(uuid4()), comment="Id do categoria"
    )

    nome: Mapped[str] = mapped_column(String(50), comment="Nome do categoria")


class Livro(Base):
    __tablename__ = "livro"

    id: Mapped[str] = mapped_column(
        primary_key=True, default=lambda: str(uuid4()), comment="Id do livro"
    )

    titulo: Mapped[str] = mapped_column(String(60), comment="Titulo do livro")

    ano_publicacao: Mapped[date] = mapped_column(comment="Ano de publicacao do livro")

    id_editora: Mapped[str] = mapped_column(
        ForeignKey("editora.id"), comment="Id do editora do livro"
    )

    id_categoria: Mapped[str] = mapped_column(
        ForeignKey("categoria.id"), comment="Id do editora do livro"
    )

    autores: Mapped[list["Autor"]] = relationship(
        secondary=livro_autor, back_populates="livros"
    )
