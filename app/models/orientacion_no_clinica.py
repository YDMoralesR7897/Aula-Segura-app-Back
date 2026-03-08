from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class OrientacionNoClinica(Base):
    __tablename__ = "orientacion_no_clinica"

    id_orientacion = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    estado = Column(Boolean, default=True)