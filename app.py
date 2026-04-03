from flask import Flask
from database.databanco import db
import os
from dotenv import load_dotenv
from models import Usuario, Livro, Emprestimo, StatusEmprestimo

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

db.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)