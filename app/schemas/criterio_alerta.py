from pydantic import BaseModel


class CriterioAlertaCreate(BaseModel):
    nombre: str


class CriterioAlertaUpdate(BaseModel):
    nombre: str
