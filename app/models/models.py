from datetime import datetime, date
from enum import Enum as PythonEnum
from uuid import uuid4

from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy import String, Enum as SQLAlchemyEnum, ForeignKey, Table, Column
from pydantic import BaseModel as SchemaBase, ConfigDict, Field


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
        default=SituacaoEmprestimo.EM_EMPRESTIMO,
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

    situacao: Mapped[str] = mapped_column(
        SQLAlchemyEnum(SituacaoExemplar, native_enum=False),
        default=SituacaoExemplar.EM_EMPRESTIMO,
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


#  ------------- DTO's ------------


class AutorEntrada(SchemaBase):
    nome: str = Field(max_length=100)


class AutorSaida(SchemaBase):
    model_config = ConfigDict(from_attributes=True)
    id: str
    nome: str


class ExemplarEntrada(SchemaBase):
    situacao: str
    id_livro: str


class ExemplarSaida(SchemaBase):
    model_config = ConfigDict(from_attributes=True)
    id: str
    situacao: str
    id_livro: str


class EmprestimoEntrada(SchemaBase):
    situacao_emprestimo: SituacaoEmprestimo
    data_emprestimo: datetime
    data_devolucao_efetiva: datetime | None = None
    data_prazo_devolucao_efetiva: datetime | None = None
    id_usuario: str
    id_exemplar: str


class EmprestimoSaida(SchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    situacao_emprestimo: SituacaoEmprestimo
    data_emprestimo: datetime
    data_devolucao_efetiva: datetime | None
    data_prazo_devolucao_efetiva: datetime | None
    id_usuario: str
    id_exemplar: str


class UsuarioEntrada(SchemaBase):
    nome: str = Field(max_length=100)
    data_criacao: datetime
    email: str = Field(max_length=150)
    matricula: str
    tipo_usuario: TipoUsuario | None = None


class UsuarioSaida(SchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    nome: str
    data_criacao: datetime
    email: str
    matricula: str
    tipo_usuario: TipoUsuario | None


class EditoraEntrada(SchemaBase):
    nome: str = Field(max_length=100)


class EditoraSaida(SchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    nome: str


class CategoriaEntrada(SchemaBase):
    nome: str = Field(max_length=50)


class CategoriaSaida(SchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    nome: str


class LivroEntrada(SchemaBase):
    titulo: str = Field(max_length=60)
    ano_publicacao: date
    id_editora: str
    id_categoria: str
    id_autores: list[str] = Field(default_factory=list)


class LivroSaida(SchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    titulo: str
    ano_publicacao: date
    id_editora: str
    id_categoria: str
    autores: list[AutorSaida]
