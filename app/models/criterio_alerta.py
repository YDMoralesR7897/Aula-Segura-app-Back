from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class CriterioAlerta(Base):
    __tablename__ = "criterio_alerta"

    id_criterio = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    estado = Column(Boolean, default=True)