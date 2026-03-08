"""Launcher sencillo para ejecutar la aplicación desde la raíz del proyecto.
Permite usar `python main.py` en lugar de invocar uvicorn manualmente.
"""
from typing import Generator
from app.routes import persona, usuario, perfil
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.routes import auth
from app.database import Base, engine
from app.routes import tipo_persona
from app.routes import criterio_alerta
from app.routes import orientacion
from app.routes import hoja_vida
from app.routes import detalle_hoja_vida

app = FastAPI(title="Aula Segura API")
app.include_router(perfil.router)
app.include_router(persona.router)
app.include_router(usuario.router)
app.include_router(auth.router)
app.include_router(tipo_persona.router)
app.include_router(criterio_alerta.router)
app.include_router(orientacion.router)
app.include_router(hoja_vida.router)
app.include_router(detalle_hoja_vida.router)


# Cadena de conexión (ajusta usuario/clave/host/DB si hace falta)
DATABASE_URL = "mysql+pymysql://root:root123@localhost:3306/aula_segura"

# Motor, sesión y base
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



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


"""
create database aula_segura;
use aula_segura;
select * from perfil;
select * from persona;
select * from usuario;
select * from hoja_vida;
select * from orientacion_no_clinica;
select * from tipo_persona;
select * from detalle_hoja_vida;
CREATE TABLE tipo_persona (
    id_tipop INT AUTO_INCREMENT PRIMARY KEY,
    nombretp VARCHAR(100) NOT NULL,
    descripciontp TEXT,
    estado BOOLEAN DEFAULT TRUE
);

INSERT INTO tipo_persona (nombretp, descripciontp)
VALUES
('Psicólogo', 'Profesional de apoyo emocional'),
('Docente', 'Profesor de la institución'),
('Orientador', 'Encargado de convivencia escolar');

CREATE TABLE criterio_alerta (
    id_criterio INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    estado BOOLEAN DEFAULT TRUE
);

INSERT INTO criterio_alerta (nombre)
VALUES
('Bullying'),
('Aislamiento social'),
('Bajo rendimiento académico');

CREATE TABLE orientacion_no_clinica (
    id_orientacion INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    estado BOOLEAN DEFAULT TRUE
);

INSERT INTO orientacion_no_clinica (nombre)
VALUES
('Recomendación pedagógica'),
('Citación a padres'),
('Actividad de integración');

CREATE TABLE hoja_vida (
    id_hoja INT AUTO_INCREMENT PRIMARY KEY,
    id_persona INT,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE,

    FOREIGN KEY (id_persona) REFERENCES persona(id_persona)
);

CREATE TABLE detalle_hoja_vida (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_hoja INT,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,

    id_criterio INT,
    id_orientacion INT,
    id_tipop INT,

    observaciones TEXT,
    persona_registra INT,

    FOREIGN KEY (id_hoja) REFERENCES hoja_vida(id_hoja),
    FOREIGN KEY (id_criterio) REFERENCES criterio_alerta(id_criterio),
    FOREIGN KEY (id_orientacion) REFERENCES orientacion_no_clinica(id_orientacion),
    FOREIGN KEY (id_tipop) REFERENCES tipo_persona(id_tipop),
    FOREIGN KEY (persona_registra) REFERENCES persona(id_persona)
);
"""