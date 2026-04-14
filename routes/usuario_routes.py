from flask import Blueprint, request, redirect, url_for, render_template, flash
from models import Usuario
from database.databanco import db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

usuario_bp = Blueprint("usuarios", __name__)

@usuario_bp.route("/novo", methods=["POST"])
def novo_usuario():

    nome = request.form.get("nome", "").strip()
    email = request.form.get("email", "").strip()
    senha = request.form.get("senha", "").strip()

    if not nome or not email or not senha:
        flash("Todos os dados são obrigatórios", "error")
        return redirect(url_for("index", open="novoUsuario"), code=303)
    
    if len(senha) < 8:
        flash("A senha precisa ter no mínimo 8 caracteres", "error")
        return redirect(url_for("index"), open="novoUsuario", code=303)
    if len(senha) > 20:
        flash("A senha pode ter no máximo 20 caracteres", "error")
        return redirect(url_for("index"), open="novoUsuario", code=303)
    
    if senha.isdigit():
        flash("A senha não pode conter apenas números", "error")
        return redirect(url_for("index"), open="novoUsuario", code=303)

    senha_hash = generate_password_hash(senha)

    usuario = Usuario(
        nome=nome,
        email=email,
        senha=senha_hash
    )

    try:
        db.session.add(usuario)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

        flash("Esse e-mail já foi cadastrado", "error")
        return redirect(url_for("index", open="novoUsuario"), code=303)

    flash("Usuário criado com sucesso!", "success")
    return redirect(url_for("index", open="novoUsuario"), code=303)

@usuario_bp.route("/deletar", methods=["POST"])
def deletar_usuario():
    id = request.form.get("usuario_id")

    if not id:
        flash("ID do Usuário é obrigatório", "error")
        return redirect(url_for("index", open="deletarUsuario"), code=303)
    
    try:
        id = int(id)
    except (TypeError, ValueError):
        flash("ID deve ser um número", "error")
        return redirect(url_for("index", open="deletarUsuario"), code=303)

    if id <= 0:
        flash("ID inválido", "error")
        return redirect(url_for("index", open="deletarUsuario"), code=303)
    
    #antes
    #usuario = Usuario.query.get(id)

    #depois
    usuario = db.session.get(Usuario, id)

    if not usuario:
        flash("Usuário não encontrado no sistema", "error")
        return redirect(url_for("index", open="deletarUsuario"), code=303)

    db.session.delete(usuario)
    db.session.commit()

    flash("Usuário deletado com sucesso!", "success")
    return redirect(url_for("index", open="deletarUsuario"), code=303)

