from sqlalchemy import Column, Integer, String, Boolean, ForeignKey  # Column y tipos de datos para las columnas de la tabla
from sqlalchemy.orm import relationship  # ayuda para definir relaciones entre modelos (ORM)
from app.database import Base  # clase base declarativa (declarative_base) para los modelos


class Usuario(Base):  # modelo ORM que representa la tabla `usuario` en la base de datos
    __tablename__ = "usuario"  # nombre de la tabla en la base de datos

    id_usuario = Column(Integer, primary_key=True, index=True)  # clave primaria entera con índice
    username = Column(String(50), nullable=False, unique=True)  # nombre de usuario (cadena, obligatorio, único)
    password = Column(String(255), nullable=False)  # contraseña (o hash), campo obligatorio

    id_persona = Column(Integer, ForeignKey("persona.id_persona"), unique=True)  # FK hacia `persona.id_persona` (relación 1:1)
    id_perfil = Column(Integer, ForeignKey("perfil.id_perfil"))  # FK hacia `perfil.id_perfil` (relación muchos:1)

    estado = Column(Boolean, default=True)  # indicador booleano de estado (activo/inactivo)

    persona = relationship("Persona")  # relación ORM: permite acceder al objeto `Persona` asociado
    perfil = relationship("Perfil")  # relación ORM: permite acceder al objeto `Perfil` asociado