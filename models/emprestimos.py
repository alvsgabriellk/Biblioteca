from database.databanco import db
from datetime import date, timedelta
import enum
from sqlalchemy import Enum

class StatusEmprestimo(enum.Enum):
    NAO_DEVOLVIDO = "NAO_DEVOLVIDO"
    EM_ANDAMENTO = "EM_ANDAMENTO"
    DEVOLVIDO = "DEVOLVIDO"


class Emprestimo(db.Model):
    __tablename__ = "emprestimos"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    livro_id = db.Column(db.Integer, db.ForeignKey("livros.id"))
    data_emprestimo = db.Column(db.Date, default=date.today)
    data_devolucao = db.Column(db.Date, default=lambda: date.today() + timedelta(days=7))
    status = db.Column(
        Enum(StatusEmprestimo),
        default=StatusEmprestimo.EM_ANDAMENTO,
        nullable=False
    )

    livro = db.relationship("Livro")
    usuario = db.relationship("Usuario")
    