from pydantic import BaseModel, EmailStr, Field

from app.schemas.common import ORMModel


class PersonaBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=50)
    apellido: str = Field(min_length=2, max_length=50)
    correo: EmailStr


class PersonaCreate(PersonaBase):
    pass


class PersonaUpdate(PersonaBase):
    pass


class PersonaResponse(PersonaBase, ORMModel):
    id_persona: int
    estado: bool
