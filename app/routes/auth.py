from datetime import UTC, datetime
import secrets

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config import get_settings
from app.core.jwt import TokenError, create_token, decode_token
from app.database import get_db
from app.models.persona import Persona
from app.models.usuario import Usuario
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RecuperarPasswordRequest,
    RestablecerPasswordRequest,
)
from app.schemas.common import MessageResponse
from app.services.mail import send_password_reset_email
from app.utils.security import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Autenticacion"])
settings = get_settings()


@router.post("/login", response_model=LoginResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.username == login_data.username).first()

    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales invalidas")

    if not verify_password(login_data.password, usuario.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales invalidas")

    if not usuario.estado:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuario inhabilitado")

    expires_in = settings.jwt_expire_minutes * 60
    token = create_token(
        subject=usuario.username,
        extra={"user_id": usuario.id_usuario, "id_perfil": usuario.id_perfil},
    )

    return LoginResponse(
        access_token=token,
        expires_in=expires_in,
        id_usuario=usuario.id_usuario,
        username=usuario.username,
        id_perfil=usuario.id_perfil,
    )


@router.post("/recuperar-password", response_model=MessageResponse)
async def recuperar_password(data: RecuperarPasswordRequest, db: Session = Depends(get_db)):
    usuario = (
        db.query(Usuario)
        .join(Persona, Persona.id_persona == Usuario.id_persona)
        .filter(Persona.correo == data.correo, Usuario.estado.is_(True))
        .first()
    )

    if not usuario:
        return MessageResponse(mensaje="Si el correo existe, se enviaron instrucciones")

    reset_token = create_token(
        subject=usuario.username,
        minutes=settings.password_reset_expire_minutes,
        extra={"user_id": usuario.id_usuario, "scope": "password_reset", "nonce": secrets.token_hex(8)},
    )
    reset_url = f"{settings.frontend_reset_url}?token={reset_token}"

    sent = await send_password_reset_email(data.correo, reset_url)
    if not sent:
        # Fallback for local development when email settings are missing.
        return MessageResponse(mensaje=f"Token generado para desarrollo: {reset_token}")

    return MessageResponse(mensaje="Se enviaron instrucciones al correo")


@router.post("/restablecer-password", response_model=MessageResponse)
def restablecer_password(payload: RestablecerPasswordRequest, db: Session = Depends(get_db)):
    try:
        token_data = decode_token(payload.token)
    except TokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc

    if token_data.get("scope") != "password_reset":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalido")

    exp = token_data.get("exp")
    if exp is None or datetime.fromtimestamp(exp, tz=UTC) < datetime.now(UTC):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado")

    user_id = token_data.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalido")

    usuario = db.query(Usuario).filter(Usuario.id_usuario == user_id).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    usuario.password = hash_password(payload.nueva_password)
    db.commit()

    return MessageResponse(mensaje="Contrasena actualizada correctamente")
