from sqlalchemy import Column, Integer, String, Boolean  # Column y tipos de datos para las columnas
from app.database import Base  # Base declarativa usada por los modelos


class Persona(Base):  # modelo ORM que representa la tabla `persona`
    __tablename__ = "persona"  # nombre de la tabla en la base de datos

    id_persona = Column(Integer, primary_key=True, index=True)  # clave primaria entera con índice
    nombre = Column(String(50), nullable=False)  # nombre, obligatorio
    apellido = Column(String(50), nullable=False)  # apellido, obligatorio
    correo = Column(String(100), nullable=False, unique=True)  # correo electrónico, obligatorio y único
    estado = Column(Boolean, default=True)  # indicador booleano de estado (activo/inactivo)