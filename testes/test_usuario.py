from models import Usuario
from database.databanco import db
import pytest

def test_criar_usuario(client):
    response = client.post("/usuarios/novo", data={
        "nome": "Janaina",
        "email": "janaina128@gmail.com",
        "senha": "f2u2uf32"
    })

    assert response.status_code == 201

    usuario = Usuario.query.filter_by(nome="Janaina").first()

    assert usuario is not None
    assert usuario.email == "janaina128@gmail.com"


"""@pytest.mark.parametrize("nome, email, senha", [
    ("",        "user@email.com", "senha123"),   # nome vazio
    ("   ",     "user@email.com", "senha123"),   # nome só com espaço
    ("João",    "",               "senha123"),   # email vazio
    ("João",    "   ",            "senha123"),   # email só com espaço
    ("João",    "user@email.com",  ""       ),   # senha vazia
    ("João",    "user@email.com", "   "     ),   # senha só com espaço
    ("",        "",               ""        ),   # tudo vazio
])

def test_criar_usuario_dados_invalido(client, nome, email, senha):

    response = client.post("/usuarios/novo", data={
        "nome": nome,
        "email": email,
        "senha": senha
    })

    with client.application.app_context():
        total = db.session.execute(db.select(Usuario)).scalars().all()
        assert len(total) == 0

    assert response.status_code == 400"""

def test_criar_usuario_senha_inválida(client):
    response = client.post("/usuarios/novo", data={
        "nome": "Gabriell",
        "email": "cauagabriell@gmail.com",
        "senha": "12345678"
    })

    assert response.status_code == 400

    with client.application.app_context():
        usuario = db.session.execute(
            db.select(Usuario).filter_by(email="cauagabriell@gmail.com")
        ).scalar_one_or_none()

        assert usuario is None

    

def test_listar_produtos(client):

    with client.application.app_context():
        db.session.add(Usuario(
            nome="Janaina", 
            email="janaina123@gmail.com", 
            senha="fnjkqnf23f2"
        ))
        db.session.commit()

    response = client.get("/usuarios/listar")

    assert response.status_code == 200
    assert b"Janaina" in response.data


def test_deletar_usuario(client):

    with client.application.app_context():
        usuario = Usuario(
            nome="Janaina",
            email="janaina124@gmail.com",
            senha="jfnu2r2fnf24"
        )
        db.session.add(usuario)
        db.session.commit()
        usuario_id = usuario.id

    response = client.post("/usuarios/deletar", data={
        "usuario_id": usuario_id
    })

    assert response.status_code == 200

    with client.application.app_context():
        usuario = db.session.get(Usuario, usuario_id)
        assert usuario is None