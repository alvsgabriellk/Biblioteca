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

    if not titulo or not autor or not quantidade_total:
        flash("Todos os dados são obrigatórios", "error")
        return redirect(url_for("index"))
    
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

@livro_bp.route("/deletar", methods=["POST"])
def deletar_livro():
    id = request.form.get(int("livro_id"))

    if not int(id):
        flash("ID do Livro é obrigatório", "error")
        return redirect(url_for("index"))

    if int(id) <= 0:
        flash("ID inválido", "error")
        return redirect(url_for("index"))

    livro = Livro.query.get(id)

    if not livro:
        flash("Livro não encontrado no sistema", "error")
        return redirect(url_for("index"))
    
    db.session.delete(livro)
    db.session.commit()

    flash("Livro deletado com sucesso!", "success")
    return redirect(url_for("index"))

@livro_bp.route("/listar", methods=["GET"])
def listar_livros():
    livros = Livro.query.all()

    if not livros:
        flash("Nenhum livro encontrado", "error")
        return redirect(url_for("index"))

    return render_template("index.html", livros=livros)
