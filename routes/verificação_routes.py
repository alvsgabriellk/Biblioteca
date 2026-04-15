from flask import redirect, session, request, url_for
from sqlalchemy import select
from database.databanco import db
from models import Espectador

def existe_usuario():
    return db.session.execute(
        select(Espectador.id)
    ).first() is not None