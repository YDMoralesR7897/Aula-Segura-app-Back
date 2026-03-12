from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging
from app.database import Base, engine
from app.models import criterio_alerta, detalle_hoja_vida, hoja_vida, orientacion_no_clinica, perfil, persona, tipo_persona, usuario
from app.routes import auth, criterio_alerta as criterio_alerta_router
from app.routes import detalle_hoja_vida as detalle_hoja_vida_router
from app.routes import hoja_vida as hoja_vida_router
from app.routes import orientacion as orientacion_router
from app.routes import perfil as perfil_router
from app.routes import persona as persona_router
from app.routes import tipo_persona as tipo_persona_router
from app.routes import usuario as usuario_router

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    if settings.bootstrap_schema:
        Base.metadata.create_all(bind=engine)
    yield


def create_app() -> FastAPI:
    configure_logging()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.app_debug,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(app)

    app.include_router(perfil_router.router)
    app.include_router(persona_router.router)
    app.include_router(usuario_router.router)
    app.include_router(auth.router)
    app.include_router(tipo_persona_router.router)
    app.include_router(criterio_alerta_router.router)
    app.include_router(orientacion_router.router)
    app.include_router(hoja_vida_router.router)
    app.include_router(detalle_hoja_vida_router.router)

    @app.get("/")
    async def read_root():
        return {"message": "API Aula Segura funcionando"}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
