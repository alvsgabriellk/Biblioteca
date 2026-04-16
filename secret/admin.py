from functools import wraps
from flask import session, redirect, url_for, flash,request ,Blueprint
from models import Espectador
from database.databanco import db
from dotenv import load_dotenv
import os

load_dotenv()

admin_bp = Blueprint("admin", __name__)

# *ARGS E **KWAGRS -> Aceitam qualquer tipo de parâmetro
# decorator para proteger rotas de admin
def admin_required(f): # f -> a função(rota) que será protegida
    @wraps(f) # wraps -> nao perde os dados da função recebida
    def wrapper(*args, **kwargs): # wrapper = função nova que envolve a original
        if not session.get("is_admin"):
            flash("Você não tem acesso de admin", "error")

            open_param = request.form.get("open") or request.args.get("open")

            return redirect(
                url_for("index", open=open_param) if open_param else url_for("index"),
                code=303
            )
        return f(*args, **kwargs) # executa função original
    return wrapper # retorna a função modificada




