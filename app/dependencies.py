from dataclasses import dataclass

from fastapi import Depends, HTTPException, Query, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.jwt import TokenError, decode_token
from app.database import get_db
from app.models.usuario import Usuario

security = HTTPBearer(auto_error=False)


@dataclass
class PaginationParams:
    limit: int = 20
    offset: int = 0


def pagination_params(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> PaginationParams:
    return PaginationParams(limit=limit, offset=offset)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: Session = Depends(get_db),
) -> Usuario:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")

    try:
        payload = decode_token(credentials.credentials)
    except TokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc

    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    user = db.query(Usuario).filter(Usuario.id_usuario == user_id, Usuario.estado.is_(True)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or disabled")

    return user


def require_profiles(*allowed_profile_ids: int):
    def dependency(current_user: Usuario = Depends(get_current_user)) -> Usuario:
        if allowed_profile_ids and current_user.id_perfil not in allowed_profile_ids:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return current_user

    return dependency
