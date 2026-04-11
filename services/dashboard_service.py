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

