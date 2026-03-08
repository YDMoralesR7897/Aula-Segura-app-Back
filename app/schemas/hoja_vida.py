from pydantic import BaseModel


class HojaVidaCreate(BaseModel):
    id_persona: int
