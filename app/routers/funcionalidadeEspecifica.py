from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.models import Usuario, Emprestimo, SituacaoEmprestimo
from app.database import get_session

router = APIRouter(tags=["Funcionalidade especifica"])


@router.get("/emprestimos/vencidos/")
def identificar_emprestimos_atrasados(db: Session = Depends(get_session)):
    data_atual = datetime.now()

    emprestimos_vencidos = (
        db.query(Emprestimo)
        .filter(
            Emprestimo.situacao_emprestimo == SituacaoEmprestimo.PENDENTE,
            Emprestimo.data_devolucao_efetiva.is_(None),
            Emprestimo.data_prazo_devolucao_efetiva < data_atual,
        )
        .all()
    )

    for emp in emprestimos_vencidos:
        emp.situacao_emprestimo = SituacaoEmprestimo.ATRASADO

    if emprestimos_vencidos:
        db.commit()

    atrasados = (
        db.query(Emprestimo)
        .filter(
            Emprestimo.situacao_emprestimo == SituacaoEmprestimo.ATRASADO,
            Emprestimo.data_devolucao_efetiva.is_(None),
        )
        .all()
    )

    return {
        "total_atrasados": len(atrasados),
        "emprestimos": [
            {
                "id_emprestimo": emp.id,
                "id_usuario": emp.id_usuario,
                "id_exemplar": emp.id_exemplar,
                "data_prazo": emp.data_prazo_devolucao_efetiva.strftime("%d/%m/%Y"),
                "dias_atraso": (data_atual - emp.data_prazo_devolucao_efetiva).days,
            }
            for emp in atrasados
        ],
    }


@router.get("/usuarios/{id_usuario}/situacao")
def calcular_situacao_usuario(id_usuario: str, db: Session = Depends(get_session)):
    usuario = db.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    data_atual = datetime.now()

    atrasos_usuario = (
        db.query(Emprestimo)
        .filter(
            Emprestimo.id_usuario == id_usuario,
            Emprestimo.data_devolucao_efetiva.is_(None),
            Emprestimo.data_prazo_devolucao_efetiva < data_atual,
        )
        .all()
    )

    teve_alteracao = False
    for emp in atrasos_usuario:
        if emp.situacao_emprestimo != SituacaoEmprestimo.ATRASADO:
            emp.situacao_emprestimo = SituacaoEmprestimo.ATRASADO
            teve_alteracao = True

    if teve_alteracao:
        db.commit()

    dias_totais_pendentes = sum(
        (data_atual - emp.data_prazo_devolucao_efetiva).days for emp in atrasos_usuario
    )

    situacao_conta = "BLOQUEADO" if atrasos_usuario else "REGULAR"

    return {
        "id_usuario": usuario.id,
        "nome": usuario.nome,
        "tipo_usuario": usuario.tipo_usuario,
        "situacao_conta": situacao_conta,
        "livros_em_atraso": len(atrasos_usuario),
        "dias_totais_de_atraso_acumulados": dias_totais_pendentes,
    }
