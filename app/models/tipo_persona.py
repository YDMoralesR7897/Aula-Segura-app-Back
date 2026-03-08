from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class TipoPersona(Base):
    __tablename__ = "tipo_persona"

    id_tipop = Column(Integer, primary_key=True, index=True)
    nombretp = Column(String(100))
    descripciontp = Column(String(200))
    estado = Column(Boolean, default=True)