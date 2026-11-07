from app.models.models import Categoria, Livro, SituacaoExemplar, Exemplar
from app.schemas.entidades import Estatistica
from sqlalchemy.orm import Session
from sqlalchemy import func


async def gerar_estatisticas(session: Session) -> Estatistica:

    estatisticas = Estatistica(
        qtd_registro_livro_categoria=gerar_qtd_registro_livro_categoria(session),
        qtd_exemplar_situacao= gerar_qtd_exemplar_situacao(session),
        tempo_medio_emprestimo= ,
        data_primeiro_emprestimo= ,
        data_ultimo_emprestimo= ,

        qtd_emprestimo_livro=
    )

    return estatisticas

def gerar_qtd_registro_livro_categoria(session: Session): # count + group by

    registros = session.query(
        Categoria.nome,
        func.count(Livro.id)
    ).join(Livro.id_categoria).group_by(Categoria.nome).all()

    return {categoria: total for categoria, total in registros}


def gerar_qtd_exemplar_situacao(session: Session): # count + group by

    registros = session.query(
        Exemplar.situacao,
        func.count(Exemplar.id)
    ).group_by(str(SituacaoExemplar)).all

    return {str(situacao): total for situacao, total in registros}

def gerar_tempo_medio_emprestimo(session: Session):
    return


def gerar_data_primeiro_emprestimo(session: Session):
    return

def gerar_data_ultimo_emprestimo(session: Session):
    return

# Especifica do tema

def gerar_qtd_emprestimo_categoria_livro(session: Session):
    return
