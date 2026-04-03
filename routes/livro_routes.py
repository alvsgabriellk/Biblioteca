from flask import Blueprint, request, render_template, redirect, url_for, flash
from models import Livro
from database.databanco import db
from sqlalchemy.exc import IntegrityError

livro_bp = Blueprint("livros", __name__)

@livro_bp.route("/novo", methods=["POST"])
def novo_livro():
    titulo = request.form.get("titulo")
    autor = request.form.get("autor")
    quantidade_total = request.form.get(int("quantidade_total"))
    
    livro = Livro(
        titulo=titulo,
        autor=autor,
        quantidade_total=quantidade_total,
        quantidade_disponivel=quantidade_total
    )

    try:
        db.session.add(livro)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("Esse Livro já foi cadastrado.", "error")
        return redirect(url_for("index"))
    
    flash("Livro criado com sucesso!", "success")
    return redirect(url_for("index"))
