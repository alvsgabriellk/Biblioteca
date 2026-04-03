from flask import Flask, render_template
from database.databanco import db
import os
from dotenv import load_dotenv
from models import Usuario, Livro, Emprestimo, StatusEmprestimo
from routes import usuario_bp

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

db.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


app.register_blueprint(usuario_bp, url_prefix="/usuarios")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)