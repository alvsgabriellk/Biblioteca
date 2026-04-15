from flask import Blueprint, request, render_template, flash, redirect, url_for
from models import Emprestimo, Livro, Usuario, StatusEmprestimo
from secret import admin_required
from database.databanco import db

emprestimo_bp = Blueprint("emprestimos", __name__)

@emprestimo_bp.route("/novo", methods=["POST"])
@admin_required
def realizar_emprestimo():
    usuario_id = request.form.get("usuario_id", "").strip()
    livro_id = request.form.get("livro_id", "").strip()

    if not usuario_id or not livro_id:
        flash("Todos os dados são obrigatórios", "error")
        return redirect(url_for("index"), code=303)
    
    try:
        usuario_id = int(usuario_id)
        livro_id = int(livro_id)
    except (TypeError, ValueError):
        flash("ID tem que ser um número!", "error")
        return redirect(url_for("index", open="emprestimo"), code=303)
    
    if usuario_id <= 0 or livro_id <= 0:
        flash("ID inválido", "error")
        return redirect(url_for("index", open="emprestimo"), code=303)
    
    usuario = db.session.get(Usuario, usuario_id)    
    livro = db.session.get(Livro, livro_id)

    if not usuario and not livro:
        flash("Livro e Usuário não encontrados no sistema", "error")
        return redirect(url_for("index", open="emprestimo"), code=303)

    if not usuario:
        flash("Usuário não encontrado no sistema", "error")
        return redirect(url_for("index", open="emprestimo"), code=303)

    if not livro:
        flash("Livro não encontrado no sistema", "error")
        return redirect(url_for("index", open="emprestimo"), code=303)
    
    if livro.quantidade_disponivel <= 0:
        flash("Livro indisponível", "error")
        return redirect(url_for("index", open="emprestimo"), code=303)
    
    emprestimo = Emprestimo(
        usuario_id=usuario_id,
        livro_id=livro_id
    )

    livro.quantidade_disponivel -= 1

    db.session.add(emprestimo)
    db.session.commit()

    flash("Empréstimo realizado com sucesso!", "success")
    return redirect(url_for("index", open="emprestimo"), code=303)

@emprestimo_bp.route("/devolver", methods=["POST"])
@admin_required
def devolver_livro():
    emprestimo_id = request.form.get("emprestimo_id", "").strip()

    if not emprestimo_id:
        flash("Todos os dados são obrigatórios", "error")
        return redirect(url_for("index", open="devolver"), code=303)
    
    try:
        emprestimo_id = int(emprestimo_id)
    except (TypeError, ValueError):
        flash("ID inválido", "error")
        return redirect(url_for("index", open="devolver"), code=303)
    
    if emprestimo_id <= 0:
        flash("ID inválido", "error")
        return redirect(url_for("index", open="devolver"), code=303)
    
    emprestimo = db.session.get(Emprestimo, emprestimo_id)

    if not emprestimo:
        flash("Empréstimo não encontrado no sistema", "error")
        return redirect(url_for("index", open="devolver"), code=303)
    
    if emprestimo.status == StatusEmprestimo.DEVOLVIDO:
        flash("Livro já foi devolvido", "error")
        return redirect(url_for("index", open="devolver"), code=303)
    
    emprestimo.status = StatusEmprestimo.DEVOLVIDO
    
    emprestimo.livro.quantidade_disponivel += 1

    db.session.commit()

    flash("Livro devolvido com sucesso!", "success")
    return redirect(url_for("index", open="devolver"), code=303)