from sqlalchemy import Column, Integer, String, Boolean  # Column y tipos para definir columnas en la tabla
from app.database import Base  # Base declarativa (declarative_base) compartida para todos los modelos


class Perfil(Base):  # modelo ORM que representa la tabla `perfil`
    __tablename__ = "perfil"  # nombre de la tabla en la base de datos

    id_perfil = Column(Integer, primary_key=True, index=True)  # id autoincremental, clave primaria y con índice
    nombre = Column(String(50), nullable=False, unique=True)  # nombre del perfil, obligatorio y único
    descripcion = Column(String(150))  # descripción opcional del perfil
    estado = Column(Boolean, default=True)  # bandera booleana para estado (activo/inactivo)