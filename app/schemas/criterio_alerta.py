from pydantic import BaseModel, Field

from app.schemas.common import ORMModel


class CriterioAlertaBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)


class CriterioAlertaCreate(CriterioAlertaBase):
    pass


class CriterioAlertaUpdate(CriterioAlertaBase):
    pass


class CriterioAlertaResponse(CriterioAlertaBase, ORMModel):
    id_criterio: int
    estado: bool
