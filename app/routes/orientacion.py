from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.dependencies import PaginationParams, pagination_params, require_profiles
from app.models.orientacion_no_clinica import OrientacionNoClinica
from app.models.usuario import Usuario
from app.schemas.common import MessageResponse
from app.schemas.orientacion import OrientacionCreate, OrientacionResponse, OrientacionUpdate

router = APIRouter(prefix="/orientacion", tags=["Orientaciones No Clinicas"])
settings = get_settings()
admin_required = require_profiles(*settings.admin_profile_ids)


@router.post("/", response_model=OrientacionResponse, status_code=status.HTTP_201_CREATED)
def crear_orientacion(
    orientacion_data: OrientacionCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(admin_required),
):
    nueva = OrientacionNoClinica(nombre=orientacion_data.nombre)

    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    return nueva


@router.get("/", response_model=list[OrientacionResponse])
def listar_orientaciones(
    db: Session = Depends(get_db),
    pagination: PaginationParams = Depends(pagination_params),
    _: Usuario = Depends(admin_required),
):
    return (
        db.query(OrientacionNoClinica)
        .filter(OrientacionNoClinica.estado.is_(True))
        .offset(pagination.offset)
        .limit(pagination.limit)
        .all()
    )


@router.put("/{id_orientacion}", response_model=OrientacionResponse)
def modificar_orientacion(
    id_orientacion: int,
    orientacion_data: OrientacionUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(admin_required),
):
    orientacion = db.query(OrientacionNoClinica).filter(OrientacionNoClinica.id_orientacion == id_orientacion).first()

    if not orientacion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orientacion no encontrada")

    orientacion.nombre = orientacion_data.nombre

    db.commit()
    db.refresh(orientacion)

    return orientacion


@router.delete("/{id_orientacion}", response_model=MessageResponse)
def inhabilitar_orientacion(
    id_orientacion: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(admin_required),
):
    orientacion = db.query(OrientacionNoClinica).filter(OrientacionNoClinica.id_orientacion == id_orientacion).first()

    if not orientacion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orientacion no encontrada")

    orientacion.estado = False

    db.commit()

    return MessageResponse(mensaje="Orientacion inhabilitada")
