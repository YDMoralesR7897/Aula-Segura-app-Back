from pydantic import BaseModel


class TipoPersonaCreate(BaseModel):
    nombretp: str
    descripciontp: str


class TipoPersonaUpdate(BaseModel):
    nombretp: str
