from flask import Blueprint, request, render_template, flash
from models import Emprestimo, Livro, Usuario
from database.databanco import db
from sqlalchemy.exc import IntegrityError

emprestimo_bp = Blueprint("/emprestimos", __name__)

@emprestimo_bp.route("/novo", methods=["POST"])
def realizar_emprestimo():
    usuario_id = request.form.get("usuario_id", "").strip()
    livro_id = request.form.get("livro_id", "").strip()

    if not usuario_id or not livro_id:
        flash("Todos os dados são obrigatórios", "error")
        return render_template("index.html"), 400
    
    if not usuario_id.isdigit() or not livro_id.isdigit():
        flash("ID deve ser um número!", "error")
        return render_template("index.html"), 400
    
    if usuario_id <= 0 or livro_id <= 0:
        flash("ID inválido", "error")
        return render_template("index.html"), 400
    
    usuario = db.session.get(Usuario, usuario_id)

    if not usuario:
        flash("Usuário não encontrado no sistema", "error")
        return render_template("index.html"), 404
    
    livro = db.session.get(Livro, livro_id)

    if not livro:
        flash("Livro não encontrado no sistema", "error")
        return render_template("index.html"), 404