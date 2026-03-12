from app.models.perfil import Perfil
from app.models.persona import Persona
from app.models.usuario import Usuario
from app.utils.security import hash_password, verify_password


def _seed_admin_and_target(db):
    admin_profile = Perfil(nombre="Administrador", descripcion="Admin")
    teacher_profile = Perfil(nombre="Docente", descripcion="Doc")

    admin_person = Persona(nombre="Ana", apellido="Admin", correo="ana2@example.com")
    target_person = Persona(nombre="Luis", apellido="Doc", correo="luis@example.com")

    db.add_all([admin_profile, teacher_profile, admin_person, target_person])
    db.commit()
    db.refresh(admin_profile)
    db.refresh(teacher_profile)
    db.refresh(admin_person)
    db.refresh(target_person)

    admin_user = Usuario(
        username="admin2",
        password=hash_password("password123"),
        id_persona=admin_person.id_persona,
        id_perfil=admin_profile.id_perfil,
        estado=True,
    )
    target_user = Usuario(
        username="targetuser",
        password=hash_password("password123"),
        id_persona=target_person.id_persona,
        id_perfil=teacher_profile.id_perfil,
        estado=True,
    )
    db.add_all([admin_user, target_user])
    db.commit()
    db.refresh(target_user)

    return target_user.id_usuario


def test_update_user_password_is_hashed(client, db):
    target_user_id = _seed_admin_and_target(db)

    login = client.post("/auth/login", json={"username": "admin2", "password": "password123"})
    token = login.json()["access_token"]

    response = client.put(
        f"/usuario/{target_user_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"username": "targetuser", "password": "newStrong123", "id_perfil": 2},
    )

    assert response.status_code == 200

    updated_user = db.query(Usuario).filter(Usuario.id_usuario == target_user_id).first()
    assert updated_user is not None
    assert updated_user.password != "newStrong123"
    assert verify_password("newStrong123", updated_user.password)
