from flask import Blueprint, request, redirect, url_for, render_template, flash
from models import Usuario
from database.databanco import db
from sqlalchemy.exc import IntegrityError

usuario_bp = Blueprint("usuarios", __name__)

@usuario_bp.route("/cadastrar", methods=["POST"])
def cadastrar_usuario():

    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")

    usuario = Usuario(
        nome=nome,
        email=email,
        senha=senha
    )

    try:
        db.session.add(usuario)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("Esse e-mail já foi cadastrado.")
        return redirect("/")

    flash("Usúario criado com sucesso!")
    return render_template("index.html")        