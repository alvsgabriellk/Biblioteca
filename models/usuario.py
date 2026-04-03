from database.databanco import db
from datetime import date

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(70), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    data_criado = db.Column(db.Date, default=date.today)