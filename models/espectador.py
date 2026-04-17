from database.databanco import db

class Espectador(db.Model):
    __tablename__ = "espectador"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)