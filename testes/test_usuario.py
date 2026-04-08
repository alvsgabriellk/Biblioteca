def test_criar_usuario(client):
    response = client.post("/usuarios/novo", data={
        "nome": "Janaina",
        "email": "janaina128@gmail.com",
        "senha": "f2u2uf32"
    })

    assert response.status_code == 302

    from models import Usuario
    usuario = Usuario.query.filter_by(nome="Janaina").first()

    assert usuario is not None
    assert usuario.email == "janaina128@gmail.com"


def test_criar_usuario_invalido(client):
    response = client.post("/usuarios/novo", data={
        "nome": "",
        "email": "",
        "senha": ""
    })

    assert response.status_code == 302

def test_listar_produtos(client):
    from database.databanco import db
    from models import Usuario

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
    from database.databanco import db
    from models import Usuario

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

    assert response.status_code == 302

    with client.application.app_context():
        usuario = db.session.get(Usuario, usuario_id)
        assert usuario is None