from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.utils.util import commit_or_conflict, get_or_404
from app.models.models import Usuario
from app.models.models import Emprestimo, Exemplar, Livro
from app.schemas.entidades import UsuarioEntrada, UsuarioSaida, RemocaoSaida


def criar_usuarios(dados: UsuarioEntrada, session: Session):
    email_existente = session.scalars(
        select(Usuario.id).where(Usuario.email == dados.email)
    ).first()

    if email_existente:
        raise HTTPException(
            status_code=409, detail="Já existe um usuário com esse e-mail"
        )

    matricula_existente = session.scalars(
        select(Usuario.matricula).where(Usuario.matricula == dados.matricula)
    ).first()

    telefone_existente = session.scalars(
        select(Usuario.telefone).where(Usuario.telefone == dados.telefone)
    ).first()

    if telefone_existente:
        raise HTTPException(
            status_code=409, detail="Já existe um usuário com esse telefone"
        )

    if matricula_existente:
        raise HTTPException(
            status_code=409, detail="Já existe um usuário com essa matricula"
        )

    usuario = Usuario(**dados.model_dump())

    session.add(usuario)
    commit_or_conflict(session)
    session.refresh(usuario)

    return usuario


def listar_usuarios(session: Session):
    return session.scalars(select(Usuario)).all()


def obter_usuario(usuario_id: str, session: Session):
    return get_or_404(session, Usuario, usuario_id)


def atualizar_usuario(usuario_id: str, dados: UsuarioEntrada, session: Session):
    usuario = get_or_404(session, Usuario, usuario_id)

    for campo, valor in dados.model_dump().items():
        setattr(usuario, campo, valor)

    commit_or_conflict(session)
    session.refresh(usuario)
    return usuario


def apagar_usuario(usuario_id: str, session: Session):
    usuario = get_or_404(session, Usuario, usuario_id)

    dados_usuario = UsuarioSaida.model_validate(usuario)
    session.delete(usuario)
    commit_or_conflict(session)

    return RemocaoSaida(mensagem="Usuario apagado com sucesso!", dados=dados_usuario)


def listar_historico_emprestimos_usuario(session: Session, usuario_id: str):
    consulta = (
        select(Emprestimo, Exemplar, Livro)
        .join(Exemplar, Emprestimo.id_exemplar == Exemplar.id)
        .join(Livro, Exemplar.id_livro == Livro.id)
        .where(Emprestimo.id_usuario == usuario_id)
    )

    resultados = session.execute(consulta).all()

    historico = []
    for emp, exemp, liv in resultados:
        historico.append(
            {
                "id_emprestimo": emp.id,
                "situacao_emprestimo": emp.situacao_emprestimo,
                "data_emprestimo": emp.data_emprestimo,
                "data_devolucao_efetiva": emp.data_devolucao_efetiva,
                "data_prazo_devolucao": emp.data_prazo_devolucao,
                "id_exemplar": exemp.id,
                "situacao_exemplar": exemp.situacao,
                "id_livro": liv.id,
                "titulo_livro": liv.titulo,
            }
        )

    return historico
