from app.models.perfil import Perfil
from app.models.persona import Persona
from app.models.usuario import Usuario
from app.utils.security import hash_password, verify_password


def _seed_user(db):
    admin_profile = Perfil(nombre="Administrador", descripcion="Admin")
    persona = Persona(nombre="Ana", apellido="Admin", correo="ana@example.com")
    db.add_all([admin_profile, persona])
    db.commit()
    db.refresh(admin_profile)
    db.refresh(persona)

    usuario = Usuario(
        username="adminuser",
        password=hash_password("password123"),
        id_persona=persona.id_persona,
        id_perfil=admin_profile.id_perfil,
        estado=True,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def test_login_returns_token(client, db):
    _seed_user(db)

    response = client.post(
        "/auth/login",
        json={"username": "adminuser", "password": "password123"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["token_type"] == "bearer"
    assert payload["access_token"]
    assert payload["id_perfil"] == 1


def test_password_reset_flow(client, db):
    user = _seed_user(db)

    reset_response = client.post("/auth/recuperar-password", json={"correo": "ana@example.com"})
    assert reset_response.status_code == 200
    token = reset_response.json()["mensaje"].split(": ")[-1]

    update_response = client.post(
        "/auth/restablecer-password",
        json={"token": token, "nueva_password": "nuevaPass123"},
    )
    assert update_response.status_code == 200

    db.refresh(user)
    assert verify_password("nuevaPass123", user.password)
