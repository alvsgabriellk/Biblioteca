import pytest
from app import app
from database.databanco import db
from dotenv import load_dotenv
import os

load_dotenv()

@pytest.fixture # SETUP
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI_MEMORY")
    # memory = Banco só na ram, nao suja banco real, apenas teste temporario

    with app.test_client() as client: # cria cliente falso para teste navegador
        with app.app_context():
            db.create_all()
        yield client # tudo antes é o setup / tudo depois é o teardown(limpeza)
                    # roda o teste aqui
        with app.app_context():
            db.drop_all() # limpa tudo dps