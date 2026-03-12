from pydantic import BaseModel, Field

from app.schemas.common import ORMModel


class PerfilBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=50)
    descripcion: str = Field(min_length=2, max_length=150)


class PerfilCreate(PerfilBase):
    pass


class PerfilUpdate(PerfilBase):
    pass


class PerfilResponse(PerfilBase, ORMModel):
    id_perfil: int
    estado: bool
