from datetime import datetime, date

from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy import String, Enum, ForeignKey, Table, Column


class Base(DeclarativeBase):
    pass

livro_autor = Table(
    "livro_autor",
    Base.metadata,
    Column("livro_id", ForeignKey("livro.id"), primary_key=True),
    Column("autor_id", ForeignKey("autor.id"), primary_key=True),
)


class SituacaoEmprestimo(str, Enum):
        DANIFICADO = 'DANIFICADO'
        DISPONIVEL = 'DISPONIVEL'
        EM_EMPRESTIMO = 'EM_EMPRESTIMO'

class TipoUsuario(str, Enum):
    BIBLIOTECARIO='BIBLIOTECARIO'
    ALUNO='ALUNO'
    ADMINISTRADOR='ADMINISTRADOR'

class Emprestimo(Base):
    __tablename__ = 'emprestimo'

    id: Mapped[str] = mapped_column(primary_key=True, comment='Id da emprestimo')

    situacao_emprestimo: Mapped[SituacaoEmprestimo] = mapped_column(
        comment= 'status do emprestimo'
    )

    data_emprestimo: Mapped[datetime] = mapped_column(
        comment='Data da emprestimo'
    )

    data_devolucao_efetiva: Mapped[datetime] | Mapped[None] = mapped_column(
        comment='Data efetiva do emprestimo'
    )

    data_prazo_devolucao_efetiva: Mapped[datetime] | Mapped[None] = mapped_column(
        comment='Data prazo do emprestimo'
    )

    id_usuario: Mapped[str] = mapped_column(
        ForeignKey("usuario.id"),
        comment='Id do usuario do emprestimo'
    )

    id_exemplar: Mapped[str] = mapped_column(
        ForeignKey("exemplar.id"),
        comment='Id do exemplar do emprestimo'
    )

class Exemplar(Base):
    __tablename__ = 'exemplar'

    id: Mapped[str] = mapped_column(primary_key=True, comment='Id da exemplar')

    situacao: Mapped[str] = mapped_column(comment='Situacao do exemplar')

    id_livro: Mapped[str] = mapped_column(ForeignKey("livro.id"), comment='Id do livro')

class Usuario(Base):
    __tablename__ = 'usuario'

    id: Mapped[str] = mapped_column(primary_key=True, comment='Id do usuario')

    nome: Mapped[str] = mapped_column(String(100), nullable=False, comment='Nome do usuario')

    data_criacao: Mapped[datetime] = mapped_column(comment="data de criacao do usuario")

    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False, comment='Email do usuario')

    matricula: Mapped[str] = mapped_column(unique=True, nullable=False, comment='Matricula do usuario')

    tipo_usuario: Mapped[TipoUsuario] | Mapped[None] = mapped_column(comment='Tipo do usuario')

class Editora(Base):
    __tablename__ = 'editora'

    id: Mapped[str] = mapped_column(primary_key=True, comment='Id do editora')

    nome: Mapped[str] = mapped_column(String(100), comment='Nome do editora')

class Autor(Base):
    __tablename__ = 'autor'

    id: Mapped[str] = mapped_column(primary_key=True, comment='Id do autor')

    nome: Mapped[str] = mapped_column(String(100), comment='Nome do autor')

    livros: Mapped[list["Livro"]] = relationship(secondary=livro_autor, back_populates="autores")

class Categoria(Base):
    __tablename__ = 'categoria'

    id: Mapped[str] = mapped_column(primary_key=True ,comment='Id do categoria')

    nome: Mapped[str] = mapped_column(String(50), comment='Nome do categoria')

class Livro(Base):
    __tablename__ = 'livro'

    id: Mapped[str] = mapped_column(primary_key=True, comment='Id do livro')

    titulo: Mapped[str] = mapped_column(String(60), comment='Titulo do livro')

    ano_publicacao: Mapped[date] = mapped_column(comment='Ano de publicacao do livro')

    id_editora: Mapped[str] = mapped_column(ForeignKey("editora.id"), comment='Id do editora do livro')

    id_categoria: Mapped[str] = mapped_column(ForeignKey("categoria.id"), comment='Id do editora do livro')

    autores: Mapped[list["Autor"]] = relationship(secondary=livro_autor, back_populates="livros")

