from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class HojaVida(Base):
    __tablename__ = "hoja_vida"

    id_hoja = Column(Integer, primary_key=True, index=True)
    id_persona = Column(Integer, ForeignKey("persona.id_persona"))
    fecha_registro = Column(DateTime, server_default=func.now())
    estado = Column(Boolean, default=True)