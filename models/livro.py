from database.databanco import db
from datetime import date

class Livro(db.Model):
    __tablename__ = "livros"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(70), unique=True, nullable=False)
    autor = db.Column(db.String(50), nullable=False)
    quantidade_total = db.Column(db.Integer, nullable=False)
    quantidade_disponivel = db.Column(db.Integer, nullable=False)
    data_criado = db.Column(db.Date, default=date.today)