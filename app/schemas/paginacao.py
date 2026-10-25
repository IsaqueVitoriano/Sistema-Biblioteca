from pydantic import BaseModel
from app.models.models import LivroSaida, EmprestimoSaida


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
