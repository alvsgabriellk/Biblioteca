from flask import request, redirect, url_for, flash, Blueprint, session
from models import Espectador
from database.databanco import db
from sqlalchemy import select
from werkzeug.security import check_password_hash

login_bp = Blueprint("login", __name__)

@login_bp.route("/entrar", methods=["POST"])
def entrar():
    email = request.form.get("email", "").strip()
    senha = request.form.get("senha", "").strip()

    if not email or not senha:
        flash("Todos os dados são obrigatórios", "error")
        return redirect(url_for("login"), code=303)
    
    if "@" not in email:
        flash("Email inválido", "error")
        return redirect(url_for("login"), code=303)
    
    espectador = db.session.execute(
        select(Espectador).filter_by(email=email)
        ).scalar_one_or_none()
    
    
    if not espectador or not check_password_hash(espectador.senha, senha):
        flash("Email ou senha inválidos", "error")
        return redirect(url_for("login"), code=303)
    
    session["espectador_id"] = espectador.id
    session["is_admin"] = espectador.is_admin
    
    return redirect(url_for("index"), code=303)
