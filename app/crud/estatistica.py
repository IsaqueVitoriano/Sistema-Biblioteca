from app.models.models import Categoria, Livro, SituacaoExemplar, Exemplar, Emprestimo
from app.schemas.entidades import Estatistica
from sqlalchemy.orm import Session
from sqlalchemy import func


def gerar_estatisticas(session: Session) -> Estatistica:

    estatisticas = Estatistica(
        qtd_livro_categoria= gerar_qtd_livro_categoria(session),
        qtd_exemplar_situacao= gerar_qtd_exemplar_situacao(session),
        tempo_medio_emprestimo= gerar_tempo_medio_emprestimo(session),
        data_primeiro_emprestimo= gerar_data_primeiro_emprestimo(session),
        data_ultimo_emprestimo= gerar_data_ultimo_emprestimo(session),
        tot_paginas_categoria= gerar_total_paginas_categoria(session),
    )

    return estatisticas

def gerar_qtd_livro_categoria(session: Session): # count + group by
    registros = session.query(
        Categoria.nome,
        func.count(Livro.id)
    ).join(Livro.id_categoria).group_by(Categoria.nome).all()

    return {categoria: total for categoria, total in registros}


def gerar_qtd_exemplar_situacao(session: Session): # count + group by
    registros = session.query(
        Exemplar.situacao,
        func.count(Exemplar.id)
    ).group_by(str(SituacaoExemplar)).all()

    return {str(situacao): total for situacao, total in registros}

def gerar_tempo_medio_emprestimo(session: Session): # avg
    tempo_medio_dias = session.query(
        func.avg(Emprestimo.data_devolucao_efetiva - Emprestimo.data_emprestimo),
    ).scalar()

    if not tempo_medio_dias:
        return 0

    return float(tempo_medio_dias)

def gerar_data_primeiro_emprestimo(session: Session): # min
    return session.query(
            func.min(Emprestimo.data_emprestimo),
        ).scalar()

def gerar_data_ultimo_emprestimo(session: Session): # max
    return session.query(
            func.max(Emprestimo.data_emprestimo),
        ).scalar()

def gerar_total_paginas_categoria(session: Session): #sum
    registros = session.query(
        Categoria.nome,
        func.sum(Livro.paginas)
    ).join(Livro.id_categoria).group_by(Categoria.nome).all()

    return {categoria: tot for categoria, tot in registros}

# Especifica do tema
