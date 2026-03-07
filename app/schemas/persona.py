from pydantic import BaseModel


class PersonaCreate(BaseModel):
    nombre: str
    apellido: str
    correo: str


class PersonaUpdate(BaseModel):
    nombre: str
    apellido: str
    correo: str
