from flask import Blueprint, request, redirect, url_for, render_template, flash
from models import Usuario
from database.databanco import db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

usuario_bp = Blueprint("usuarios", __name__)

@usuario_bp.route("/cadastrar", methods=["POST"])
def cadastrar_usuario():

    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")

    if not nome or not email or not senha:
        flash("Todos os dados são obrigatórios", "error")
        return redirect(url_for("index"))

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
        flash("Esse e-mail já foi cadastrado.", "error")
        return redirect(url_for("index"))

    flash("Usúario criado com sucesso!", "success")
    return redirect(url_for("index"))     

@usuario_bp.route("/deletar", methods=["POST"])
def deletar_usuario():
    id = request.form.get("usuario_id")

    if not id:
        flash("ID do Usúario é obrigatório", "error")
        return redirect(url_for("index"))

    usuario = Usuario.query.get(id)

    db.session.delete(usuario)
    db.session.commit()

    flash("Usúario deletado com sucesso!", "success")
    return redirect(url_for("index"))

@usuario_bp.route("/listar", methods=["GET"])
def listar_usuarios():
    usuarios = Usuario.query.all()

    return render_template("index.html", usuarios=usuarios)
