import base64
import hashlib

import bcrypt


def _prehash(password: str) -> bytes:
    # Pre-hash to avoid bcrypt's 72-byte input limit.
    digest = hashlib.sha256(password.encode("utf-8")).digest()
    return base64.b64encode(digest)


def hash_password(password: str):
    return bcrypt.hashpw(_prehash(password), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str):
    try:
        return bcrypt.checkpw(
            _prehash(plain_password), hashed_password.encode("utf-8")
        )
    except ValueError:
        return False
