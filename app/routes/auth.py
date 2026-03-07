from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.auth import LoginRequest
from app.utils.security import verify_password

router = APIRouter(prefix="/auth", tags=["Autenticacion"])


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
