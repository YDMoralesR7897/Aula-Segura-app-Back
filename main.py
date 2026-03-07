"""Launcher sencillo para ejecutar la aplicación desde la raíz del proyecto.
Permite usar `python main.py` en lugar de invocar uvicorn manualmente.
"""
from typing import Generator
from app.routes import persona, usuario, perfil
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from app.routes import auth


app = FastAPI(title="Aula Segura API")
app.include_router(perfil.router)
app.include_router(persona.router)
app.include_router(usuario.router)
app.include_router(auth.router)




# Cadena de conexión (ajusta usuario/clave/host/DB si hace falta)
DATABASE_URL = "mysql+pymysql://root:root123@localhost:3306/aula_segura"

# Motor, sesión y base
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Dependencia de sesión
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Crea tablas si no existen
Base.metadata.create_all(bind=engine)

"""
@app.get("/")
async def read_root():
    return {"message": "API Aula Segura funcionando"}
"""


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)