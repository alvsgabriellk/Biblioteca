from flask import Blueprint, request, render_template, flash
from models import Emprestimo, Livro, Usuario, StatusEmprestimo
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
    
    try:
        usuario_id = int(usuario_id)
        livro_id = int(livro_id)
    except (TypeError, ValueError):
        flash("ID tem que ser um número!", "error")
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
    
    if livro.quantidade_disponivel <= 0:
        flash("Livro indisponível", "error")
        return render_template("index.html"), 404
    
    emprestimo = Emprestimo(
        usuario_id=usuario_id,
        livro_id=livro_id
    )

    livro.quantidade_disponivel -= 1

    db.session.add(emprestimo)
    db.session.commit()

    flash("Empréstimo realizado com sucesso!", "success")
    return render_template("index.html"), 201

@emprestimo_bp.route("/devolver", methods=["POST"])
def devolver_livro():
    livro_id = request.form.get("livro_id", "").strip()

    if not livro_id:
        flash("Todos os dados sõa obrigatórios", "error")
        return render_template("index.html"), 400
    
    try:
        livro_id = int(livro_id)
    except (TypeError, ValueError):
        flash("ID inválido", "error")
        return render_template("index.html"), 400
    
    if not livro_id.isdigit():
        flash("ID tem que ser um número!", "error")
        return render_template("index.html"), 400
    
    if livro_id <= 0:
        flash("ID inválido", "error")
        return render_template("index.html"), 400
    
    emprestimo = db.session.get(Emprestimo, livro_id)

    if not emprestimo:
        flash("Empréstimo não encontrado no sistema", "error")
        return render_template("index.html"), 404
    
    if emprestimo.status == StatusEmprestimo.DEVOLVIDO:
        flash("Livro já foi devolvido", "error")
        return render_template("index.html"), 409
    
    livro = db.session.get(Livro, livro_id)

    if not livro:
        flash("Livro não encontrado no sistema", "error")
        return render_template("index.html"), 404
    
    emprestimo.status = StatusEmprestimo.DEVOLVIDO
    
    livro.quantidade_disponivel += 1

    db.session.commit()

    flash("Livro devolvido com sucesso!", "success")
    return render_template("index.html"), 200