from sqlalchemy import select, func
from database.databanco import db
from models import Livro, Usuario, Emprestimo, StatusEmprestimo

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