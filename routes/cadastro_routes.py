from flask import request, redirect, url_for, flash, Blueprint
from models import Espectador
from database.databanco import db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
import os

load_dotenv()

cadastro_bp = Blueprint("cadastros", __name__)

@cadastro_bp.route("/novo", methods=["POST"])
def novo_cadastro():
    nome = request.form.get("nome", "").strip()
    email = request.form.get("email", "").strip()
    senha = request.form.get("senha", "").strip()
    confirmar_senha = request.form.get("confirmar_senha", "").strip()
    admin_code = request.form.get("admin_code", "").strip()

    if not nome or not email or not senha or not confirmar_senha:
        flash("Todos os dados são obrigatórios", "error")
        return redirect(url_for("cadastro"), code=303)
    
    if "@" not in email:
        flash("Email inválido", "error")
        return redirect(url_for("cadastro"), code=303)
    
    if len(senha) < 8 or len(confirmar_senha) < 8:
        flash("A senha precisa ter no mínimo 8 caracteres", "error")
        return redirect(url_for("cadastro"), code=303)
    
    if len(senha) > 20 or len(confirmar_senha) > 20:
        flash("A senha pode ter no máximo 20 caracteres", "error")
        return redirect(url_for("cadastro"), code=303)
    
    if confirmar_senha != senha:
        flash("Senhas não se combinam", "error")
        return redirect(url_for("cadastro"), code=303)
    
    senha_cripto = generate_password_hash(senha)

    espectador = Espectador(
        nome=nome,
        email=email,
        senha=senha_cripto
    )

    if admin_code and admin_code == os.getenv("ADMIN_CODE"):
        espectador.is_admin = True

    try:
        db.session.add(espectador)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

        flash("Esse email já foi cadastrado", "error")
        return redirect(url_for("cadastro"), code=303)
    
    flash("Você foi cadastrado com sucesso!", "success")
    return redirect(url_for("login"), code=303)
    

