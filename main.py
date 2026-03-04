"""Launcher sencillo para ejecutar la aplicación desde la raíz del proyecto.

Permite usar `python main.py` en lugar de invocar uvicorn manualmente.
"""
from typing import Generator
from app.routes import perfil
from app.routes import persona
from fastapi import FastAPI
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session

app = FastAPI(title="Aula Segura API")
app.include_router(perfil.router)
app.include_router(persona.router)


# Cadena de conexión (ajusta usuario/clave/host/DB si hace falta)
DATABASE_URL = "mysql+pymysql://root:root123@localhost:3306/aula_segura"

# Motor, sesión y base
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Modelos
class Perfil(Base):
    __tablename__ = "perfil"

    id_perfil = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False, unique=True)
    descripcion = Column(String(150))
    estado = Column(Boolean, default=True)


class Persona(Base):
    __tablename__ = "persona"

    id_persona = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    correo = Column(String(100), nullable=False, unique=True)
    estado = Column(Boolean, default=True)


class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

    id_persona = Column(Integer, ForeignKey("persona.id_persona"), unique=True)
    id_perfil = Column(Integer, ForeignKey("perfil.id_perfil"))

    estado = Column(Boolean, default=True)

    persona = relationship("Persona")
    perfil = relationship("Perfil")


# Dependencia de sesión
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Crea tablas si no existen
Base.metadata.create_all(bind=engine)


@app.get("/")
async def read_root():
    return {"message": "API Aula Segura funcionando"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)