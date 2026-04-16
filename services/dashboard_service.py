from flask import session
from datetime import date
from sqlalchemy import select, func
from database.databanco import db
from models import Livro, Usuario, Emprestimo, StatusEmprestimo, Espectador

def get_totais_dashboard():
    total_livros = db.session.execute(
        select(func.count()).select_from(Livro)
    ).scalar()

    total_usuarios = db.session.execute(
        select(func.count()).select_from(Usuario)
    ).scalar()

    return {
        "total_livros": total_livros or 0,
        "total_usuarios": total_usuarios or 0
    }

def dados_usuario():
    usuarios = db.session.execute(select(Usuario)).scalars().all()

    return {
        "usuarios": usuarios
    }

def dados_livro():
    livros = db.session.execute(
        select(Livro)
    ).scalars().all()

    return {
        "livros": livros
    }

def dados_emprestimo():
    # antes
    #emprestimos = db.session.execute(
     #   select(Emprestimo)
    #).scalars().all()

    emprestimos = db.session.execute(
        select(Emprestimo).where (
            Emprestimo.status != StatusEmprestimo.DEVOLVIDO
        )
    ).scalars().all()

    hoje = date.today()

    return {
        "emprestimos": emprestimos,
        "hoje": hoje
    }

def data_primeiro_criado():
    primeiro_usuario = db.session.execute(select(Usuario).order_by(Usuario.data_criado.asc())).scalars().first()

    meses = [
    "janeiro","fevereiro","março","abril","maio","junho",
    "julho","agosto","setembro","outubro","novembro","dezembro"
    ]

    if primeiro_usuario:
        data = primeiro_usuario.data_criado
        desde = f"{meses[data.month - 1]}/{data.year}"
    else:
        desde = "-"

    return {
        "desde": desde
    }

def totais_livros_quantidade():
    # antes
    #total = db.session.execute(select(func.count()).select_from(Livro.quantidade_total)).scalar()

    # depois
    total = db.session.execute(
        select(func.sum(Livro.quantidade_total))
        ).scalar()

    return {
        "total_quantidade_livro": total
    }

def total_livros_disponiveis():
    total =db.session.execute(
        select(func.sum(Livro.quantidade_disponivel))
    ).scalar()

    return {
        "total_quantidade_disponivel": total
    }

def total_emprestimos_ativos_e_atrasados():
    total_ativo = db.session.execute(
        select(func.count()).where(
            Emprestimo.status == StatusEmprestimo.EM_ANDAMENTO
        )
    ).scalar()

    total_atrasado = db.session.execute(
        select(func.count()).where(
            Emprestimo.status == StatusEmprestimo.NAO_DEVOLVIDO
        )
    ).scalar()

    return {
        "total_ativo": total_ativo,
        "total_atrasado": total_atrasado
    }

def ultimo_emprestimo():
    emprestimo = db.session.execute(
        select(Emprestimo).order_by(
            Emprestimo.data_emprestimo.desc(),
            Emprestimo.id.desc()
            )
    ).scalars().first()

    return {
        "ultimo_emprestimo": emprestimo
    }

def atividades_recentes():
    emprestimos = db.session.execute(
        select(Emprestimo)
        .order_by(
            Emprestimo.data_emprestimo.desc(),
            Emprestimo.id.desc()
        )
        .limit(3)
    ).scalars().all()

    return {
        "atividades": emprestimos
    }

def verificar_session():
    espectador_id = session.get("espectador_id")

    if not espectador_id:
        return {"tipo_usuario": None}
    
    espectador = db.session.get(Espectador, espectador_id)

    if not espectador:
        return {"tipo_usuario": None}
    
    tipo = "Admin" if espectador.is_admin else "Usuário"


        # nao funcional
    """espectador_admin = db.session.execute(
        select(Espectador).where(
            espectador.is_admin == True
        )
    ).scalar()

    espectador = db.session.execute(
        select(Espectador).where(
            Espectador.is_admin == False
        )
    ).scalar()"""

    return {
        "tipo_usuario": tipo,
        "usuario_nome": espectador.nome
    }