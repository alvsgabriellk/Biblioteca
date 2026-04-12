from flask import Flask, render_template, request
from database.databanco import db
import os
from dotenv import load_dotenv
from models import Usuario, Livro, Emprestimo, StatusEmprestimo
from routes import usuario_bp, livro_bp, emprestimo_bp
from services import get_totais_dashboard, dados_usuario, data_primeiro_criado, totais_livros_quantidade, dados_livro, dados_emprestimo, total_livros_disponiveis, total_emprestimos_ativos_e_atrasados

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")

db.init_app(app)


@app.route("/")
def index():
    open_section = request.args.get("open")

    dados_totais = get_totais_dashboard()
    dados_usuarios = dados_usuario()
    dados_primeiro_usuario = data_primeiro_criado()
    dados_totais_livros = totais_livros_quantidade()
    dados_livros = dados_livro()
    dados_emprestimos = dados_emprestimo()
    dados_total_disponivel = total_livros_disponiveis()
    dados_total_ativo_atrasado = total_emprestimos_ativos_e_atrasados()
    return render_template("index.html", **dados_totais, **dados_usuarios, **dados_primeiro_usuario, **dados_totais_livros, **dados_livros, **dados_emprestimos, **dados_total_disponivel, **dados_total_ativo_atrasado, open_section=open_section)


app.register_blueprint(usuario_bp, url_prefix="/usuarios")
app.register_blueprint(livro_bp, url_prefix="/livros")
app.register_blueprint(emprestimo_bp, url_prefix="/emprestimos")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)