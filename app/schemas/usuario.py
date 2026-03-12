from pydantic import BaseModel, Field

from app.schemas.common import ORMModel


class UsuarioBase(BaseModel):
    username: str = Field(min_length=4, max_length=50)
    id_persona: int = Field(gt=0)
    id_perfil: int = Field(gt=0)


class UsuarioCreate(UsuarioBase):
    password: str = Field(min_length=8, max_length=128)


class UsuarioUpdate(BaseModel):
    username: str = Field(min_length=4, max_length=50)
    password: str = Field(min_length=8, max_length=128)
    id_perfil: int = Field(gt=0)


class UsuarioResponse(UsuarioBase, ORMModel):
    id_usuario: int
    estado: bool
