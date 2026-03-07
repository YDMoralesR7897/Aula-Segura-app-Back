from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.auth import LoginRequest
from app.utils.security import verify_password
import random
import string
from fastapi_mail import FastMail, MessageSchema
from app.config.mail import conf
from app.utils.security import hash_password
from app.models.persona import Persona

router = APIRouter(prefix="/auth", tags=["Autenticacion"])

def generar_password_temporal():
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for i in range(8))


@router.post("/login")
def login(login_data: LoginRequest, db: Session = Depends(get_db)):

    usuario = db.query(Usuario).filter(Usuario.username == login_data.username).first()

    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")

    if not verify_password(login_data.password, usuario.password):
        raise HTTPException(status_code=400, detail="Contrasena incorrecta")

    if not usuario.estado:
        raise HTTPException(status_code=403, detail="Usuario inhabilitado")

    return {
        "mensaje": "Login exitoso",
        "usuario": usuario.username,
        "id_usuario": usuario.id_usuario
    }

@router.post("/recuperar-password")
async def recuperar_password(correo: str, db: Session = Depends(get_db)):

    usuario = db.query(Usuario).join(Persona).filter(
        Persona.correo == correo
    ).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    nueva_password = generar_password_temporal()

    usuario.password = hash_password(nueva_password)

    db.commit()

    mensaje = MessageSchema(
        subject="Recuperación de contraseña",
        recipients=[correo],
        body=f"Tu nueva contraseña temporal es: {nueva_password}",
        subtype="plain"
    )

    fm = FastMail(conf)
    await fm.send_message(mensaje)

    return {"mensaje": "Se envió una nueva contraseña al correo"}