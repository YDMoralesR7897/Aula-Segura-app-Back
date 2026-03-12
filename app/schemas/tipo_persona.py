from pydantic import BaseModel, Field

from app.schemas.common import ORMModel


class TipoPersonaBase(BaseModel):
    nombretp: str = Field(min_length=2, max_length=100)


class TipoPersonaCreate(TipoPersonaBase):
    descripciontp: str = Field(default="", max_length=200)


class TipoPersonaUpdate(TipoPersonaBase):
    pass


class TipoPersonaResponse(TipoPersonaBase, ORMModel):
    id_tipop: int
    descripciontp: str | None = None
    estado: bool
