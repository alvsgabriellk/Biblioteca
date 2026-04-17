from flask import Flask, render_template, request, redirect, url_for, session
from database.databanco import db
import os
from dotenv import load_dotenv
import psycopg2
from models import Usuario, Livro, Emprestimo, StatusEmprestimo, Espectador
from routes import usuario_bp, livro_bp, emprestimo_bp, cadastro_bp, login_bp, existe_usuario
from secret import admin_required
from services import (
    get_totais_dashboard, 
    dados_usuario, 
    data_primeiro_criado, 
    totais_livros_quantidade, 
    dados_livro, 
    dados_emprestimo, 
    total_livros_disponiveis, 
    total_emprestimos_ativos_e_atrasados, 
    ultimo_emprestimo, 
    atividades_recentes,
    verificar_session
)

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-key")

ENV = os.getenv("ENV", "local")

if ENV == "production":
    DATABASE_URL = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "connect_args": {"sslmode": "require"}
    }
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banco.db"

db.init_app(app)

@app.route("/")
def index():
    open_section = request.args.get("open")

    dados_emprestimos = dados_emprestimo()
    dados_usuarios = dados_usuario()
    dados_livros = dados_livro()

    dados_totais = get_totais_dashboard()
    dados_primeiro_usuario = data_primeiro_criado()
    dados_totais_livros = totais_livros_quantidade()
    dados_total_disponivel = total_livros_disponiveis()
    dados_total_ativo_atrasado = total_emprestimos_ativos_e_atrasados()
    dados_ultimo_emprestimo = ultimo_emprestimo()
    dados_atividades = atividades_recentes()
    dados_session = verificar_session()

    return render_template(
        "index.html", 
        **dados_totais, **dados_usuarios, 
        **dados_primeiro_usuario, **dados_totais_livros, 
        **dados_livros, **dados_emprestimos, 
        **dados_total_disponivel, **dados_total_ativo_atrasado,
        **dados_ultimo_emprestimo,**dados_atividades,
        **dados_session, open_section=open_section
    )

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.before_request
def controle_acesso():
    rota_livre = ["login", "cadastro", "cadastros.novo_cadastro", "login.entrar"]

    if request.endpoint in rota_livre:
        return
    if not existe_usuario():
        return redirect(url_for("cadastro"))
    if not session.get("espectador_id"):
        return redirect(url_for("login"))


app.register_blueprint(usuario_bp, url_prefix="/usuarios")
app.register_blueprint(livro_bp, url_prefix="/livros")
app.register_blueprint(emprestimo_bp, url_prefix="/emprestimos")
app.register_blueprint(cadastro_bp, url_prefix="/cadastros")
app.register_blueprint(login_bp, url_prefix="/login")


with app.app_context():
    db.drop_all()
    db.create_all()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
    