from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import ORMModel


class DetalleHojaVidaCreate(BaseModel):
    id_hoja: int = Field(gt=0)
    id_criterio: int = Field(gt=0)
    id_orientacion: int = Field(gt=0)
    id_tipop: int = Field(gt=0)
    observaciones: str = Field(min_length=2)
    persona_registra: int = Field(gt=0)


class DetalleHojaVidaUpdate(BaseModel):
    observaciones: str = Field(min_length=2)


class DetalleHojaVidaResponse(ORMModel):
    id_detalle: int
    id_hoja: int
    fecha: datetime
    id_criterio: int
    id_orientacion: int
    id_tipop: int
    observaciones: str | None = None
    persona_registra: int
