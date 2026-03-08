from pydantic import BaseModel


class OrientacionCreate(BaseModel):
    nombre: str


class OrientacionUpdate(BaseModel):
    nombre: str
