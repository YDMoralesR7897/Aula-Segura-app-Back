from datetime import UTC, datetime, timedelta
from typing import Any

from jose import JWTError, jwt

from app.config import get_settings

settings = get_settings()


class TokenError(Exception):
    pass


def create_token(subject: str, minutes: int | None = None, extra: dict[str, Any] | None = None) -> str:
    now = datetime.now(UTC)
    payload: dict[str, Any] = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=minutes or settings.jwt_expire_minutes)).timestamp()),
    }
    if extra:
        payload.update(extra)

    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError as exc:
        raise TokenError("Invalid or expired token") from exc
