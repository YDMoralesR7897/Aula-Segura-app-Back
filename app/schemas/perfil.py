from pydantic import BaseModel


class PerfilCreate(BaseModel):
    nombre: str
    descripcion: str


class PerfilUpdate(BaseModel):
    nombre: str
    descripcion: str
