from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class DetalleHojaVida(Base):
    __tablename__ = "detalle_hoja_vida"

    id_detalle = Column(Integer, primary_key=True, index=True)

    id_hoja = Column(Integer, ForeignKey("hoja_vida.id_hoja"))
    fecha = Column(DateTime, server_default=func.now())

    id_criterio = Column(Integer, ForeignKey("criterio_alerta.id_criterio"))
    id_orientacion = Column(Integer, ForeignKey("orientacion_no_clinica.id_orientacion"))
    id_tipop = Column(Integer, ForeignKey("tipo_persona.id_tipop"))

    observaciones = Column(Text)

    persona_registra = Column(Integer, ForeignKey("persona.id_persona"))