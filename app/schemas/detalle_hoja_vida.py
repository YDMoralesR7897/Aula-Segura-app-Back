from pydantic import BaseModel


class DetalleHojaVidaCreate(BaseModel):
    id_hoja: int
    id_criterio: int
    id_orientacion: int
    id_tipop: int
    observaciones: str
    persona_registra: int


class DetalleHojaVidaUpdate(BaseModel):
    observaciones: str
