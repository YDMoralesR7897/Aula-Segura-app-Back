from pydantic import BaseModel, Field

from app.schemas.common import ORMModel


class OrientacionBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)


class OrientacionCreate(OrientacionBase):
    pass


class OrientacionUpdate(OrientacionBase):
    pass


class OrientacionResponse(OrientacionBase, ORMModel):
    id_orientacion: int
    estado: bool
