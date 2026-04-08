from flask import Blueprint, request, redirect, url_for, render_template, flash
from models import Usuario
from database.databanco import db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

usuario_bp = Blueprint("usuarios", __name__)

@usuario_bp.route("/novo", methods=["POST"])
def novo_usuario():

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
    
    try:
        id = int(id)
    except (TypeError, ValueError):
        flash("ID deve ser um número!", "error")
        return redirect(url_for("index"))

    if id <= 0:
        flash("ID inválido", "error")
        return redirect(url_for("index"))
    
    #antes
    #usuario = Usuario.query.get(id)

    #depois
    usuario = db.session.get(Usuario, id)

    if not usuario:
        flash("Usúario não encontrado no sistema", "error")
        return redirect(url_for("index"))

    db.session.delete(usuario)
    db.session.commit()

    flash("Usúario deletado com sucesso!", "success")
    return redirect(url_for("index"))

@usuario_bp.route("/listar", methods=["GET"])
def listar_usuarios():
    #antes
    #usuarios = Usuario.query.all()

    #depois
    usuarios = db.session.execute(db.select(Usuario)).scalars().all()
    #db.select = select * from 
    #.execute(db.select(Usuario)) envia pro banco, e recebe resultado bruto
    # pega os objetos usuario de cada linha
    #.all transforma em lista

    if not usuarios:
        flash("Nenhum usúario encontrado", "error")
        return redirect(url_for("index"))

    return render_template("index.html", usuarios=usuarios)
