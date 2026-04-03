from database.databanco import db
from datetime import date, timedelta

class Emprestimo(db.Model):
    __tablename__ = "emprestimos"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), unique=True)
    livro_id = db.Column(db.Integer, db.ForeignKey("livro.id"), unique=True)
    data_emprestimo = db.Column(db.Date, default=date.today)
    data_devolucao = db.Column(db.Date, default=lambda: date.today() + timedelta(days=7))
    