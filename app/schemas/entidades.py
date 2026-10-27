from datetime import datetime, date
from pydantic import BaseModel, ConfigDict, Field
from app.models.models import TipoUsuario, SituacaoEmprestimo, SituacaoExemplar


class AutorEntrada(BaseModel):
    nome: str = Field(max_length=100)


class AutorSaida(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    nome: str


class ExemplarEntrada(BaseModel):
    situacao: SituacaoExemplar
    id_livro: str


class ExemplarSaida(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    situacao: SituacaoExemplar
    id_livro: str


class EmprestimoEntrada(BaseModel):
    situacao_emprestimo: SituacaoEmprestimo
    data_emprestimo: datetime
    data_devolucao_efetiva: datetime | None = None
    data_prazo_devolucao_efetiva: datetime | None = None
    id_usuario: str
    id_exemplar: str


class EmprestimoSaida(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    situacao_emprestimo: SituacaoEmprestimo
    data_emprestimo: datetime
    data_devolucao_efetiva: datetime | None
    data_prazo_devolucao_efetiva: datetime | None
    id_usuario: str
    id_exemplar: str


class UsuarioEntrada(BaseModel):
    nome: str = Field(max_length=100)
    data_criacao: datetime
    email: str = Field(max_length=150)
    matricula: str
    tipo_usuario: TipoUsuario | None = None


class UsuarioSaida(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    nome: str
    data_criacao: datetime
    email: str
    matricula: str
    tipo_usuario: TipoUsuario | None


class EditoraEntrada(BaseModel):
    nome: str = Field(max_length=100)


class EditoraSaida(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    nome: str


class CategoriaEntrada(BaseModel):
    nome: str = Field(max_length=50)


class CategoriaSaida(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    nome: str


class LivroEntrada(BaseModel):
    titulo: str = Field(max_length=60)
    ano_publicacao: date
    id_editora: str
    id_categoria: str
    id_autores: list[str] = Field(default_factory=list)


class LivroSaida(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    titulo: str
    ano_publicacao: date
    id_editora: str
    id_categoria: str
    autores: list[AutorSaida]


class PaginacaoInfo(BaseModel):
    registros_total: int
    paginas_total: int
    pagina_atual: int
    pagina_tamanho: int


class LivroPaginadoSaida(BaseModel):
    dados: list[LivroSaida]
    paginacao: PaginacaoInfo


class EmprestimoPaginadoSaida(BaseModel):
    dados: list[EmprestimoSaida]
    paginacao: PaginacaoInfo


class HistoricoEmprestimoSaida(BaseModel):
    id_emprestimo: str
    situacao_emprestimo: SituacaoEmprestimo
    data_emprestimo: datetime
    data_devolucao_efetiva: datetime | None
    data_prazo_devolucao_efetiva: datetime | None
    id_exemplar: str
    situacao_exemplar: SituacaoExemplar
    id_livro: str
    titulo_livro: str
