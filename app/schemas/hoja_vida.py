from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import ORMModel


class HojaVidaCreate(BaseModel):
    id_persona: int = Field(gt=0)


class HojaVidaResponse(ORMModel):
    id_hoja: int
    id_persona: int
    fecha_registro: datetime
    estado: bool
