from flask import Blueprint, request, render_template, redirect, url_for, flash
from models import Livro
from database.databanco import db
from sqlalchemy.exc import IntegrityError

livro_bp = Blueprint("livros", __name__)

@livro_bp.route("/novo", methods=["POST"])
def novo_livro():

    titulo = request.form.get("titulo", "").strip()
    autor = request.form.get("autor", "").strip()
    quantidade_total = request.form.get("quantidade_total", "").strip()

    if not titulo or not autor or not quantidade_total:
        flash("Todos os dados são obrigatórios", "error")
        return redirect(url_for("index"), code=303)
    
    if not quantidade_total.isdigit():
        flash("Quantidade deve conter apenas números", "error")
        return redirect(url_for("index"), code=303)
    
    try:
        quantidade_total = int(quantidade_total)
    except (TypeError, ValueError):
        flash("Quantidade deve ser um número!", "error")
        return redirect(url_for("index"), code=303)
    
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
        return redirect(url_for("index"), code=303)
    
    flash("Livro criado com sucesso!", "success")
    return redirect(url_for("index"), code=303)

@livro_bp.route("/deletar", methods=["POST"])
def deletar_livro():
    id = request.form.get("livro_id")

    if not id:
        flash("ID do Livro é obrigatório", "error")
        return redirect(url_for("index"), code=303)
    
    try:
        id = int(id)
    except (TypeError, ValueError):
        flash("ID deve ser um número!", "error")
        return redirect(url_for("index"), code=303)
    
    if not id.isdigit():
        flash("ID tem que ser um número!", "error")
        return redirect(url_for("index"), code=303)

    if id <= 0:
        flash("ID inválido", "error")
        return redirect(url_for("index"), code=303)
    
    # antes
    #livro = Livro.query.get(id)

    #depois
    livro = db.session.get(Livro, id)

    if not livro:
        flash("Livro não encontrado no sistema", "error")
        redirect(url_for("index"), code=303)
    
    db.session.delete(livro)
    db.session.commit()

    flash("Livro deletado com sucesso!", "success")
    redirect(url_for("index"), code=303)

@livro_bp.route("/listar", methods=["GET"])
def listar_livros():
    #antes
    #livros = Livro.query.all()

    #depois
    livros = db.session.execute(db.select(Livro)).scalars().all()

    if not livros:
        flash("Nenhum livro encontrado", "error")
        return render_template("index.html"), 404

    return render_template("index.html", livros=livros), 200




