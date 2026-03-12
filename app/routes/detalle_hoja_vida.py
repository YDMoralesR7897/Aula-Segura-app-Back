from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.dependencies import PaginationParams, pagination_params, require_profiles
from app.models.criterio_alerta import CriterioAlerta
from app.models.detalle_hoja_vida import DetalleHojaVida
from app.models.hoja_vida import HojaVida
from app.models.orientacion_no_clinica import OrientacionNoClinica
from app.models.persona import Persona
from app.models.tipo_persona import TipoPersona
from app.models.usuario import Usuario
from app.schemas.common import MessageResponse
from app.schemas.detalle_hoja_vida import (
    DetalleHojaVidaCreate,
    DetalleHojaVidaResponse,
    DetalleHojaVidaUpdate,
)

router = APIRouter(prefix="/detalle-hoja-vida", tags=["Detalle Hoja Vida"])
settings = get_settings()
admin_required = require_profiles(*settings.admin_profile_ids)


@router.post("/", response_model=DetalleHojaVidaResponse, status_code=status.HTTP_201_CREATED)
def crear_detalle(
    detalle_data: DetalleHojaVidaCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(admin_required),
):
    hoja = db.query(HojaVida).filter(HojaVida.id_hoja == detalle_data.id_hoja, HojaVida.estado.is_(True)).first()
    criterio = db.query(CriterioAlerta).filter(
        CriterioAlerta.id_criterio == detalle_data.id_criterio,
        CriterioAlerta.estado.is_(True),
    ).first()
    orientacion = db.query(OrientacionNoClinica).filter(
        OrientacionNoClinica.id_orientacion == detalle_data.id_orientacion,
        OrientacionNoClinica.estado.is_(True),
    ).first()
    tipo = db.query(TipoPersona).filter(TipoPersona.id_tipop == detalle_data.id_tipop, TipoPersona.estado.is_(True)).first()
    persona = db.query(Persona).filter(Persona.id_persona == detalle_data.persona_registra, Persona.estado.is_(True)).first()

    if not all([hoja, criterio, orientacion, tipo, persona]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Alguna relacion referenciada no existe o esta inhabilitada",
        )

    nuevo = DetalleHojaVida(
        id_hoja=detalle_data.id_hoja,
        id_criterio=detalle_data.id_criterio,
        id_orientacion=detalle_data.id_orientacion,
        id_tipop=detalle_data.id_tipop,
        observaciones=detalle_data.observaciones,
        persona_registra=detalle_data.persona_registra,
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


@router.get("/", response_model=list[DetalleHojaVidaResponse])
def listar_detalles(
    db: Session = Depends(get_db),
    pagination: PaginationParams = Depends(pagination_params),
    _: Usuario = Depends(admin_required),
):
    return db.query(DetalleHojaVida).offset(pagination.offset).limit(pagination.limit).all()


@router.get("/hoja/{id_hoja}", response_model=list[DetalleHojaVidaResponse])
def detalles_por_hoja(
    id_hoja: int,
    db: Session = Depends(get_db),
    pagination: PaginationParams = Depends(pagination_params),
    _: Usuario = Depends(admin_required),
):
    return (
        db.query(DetalleHojaVida)
        .filter(DetalleHojaVida.id_hoja == id_hoja)
        .offset(pagination.offset)
        .limit(pagination.limit)
        .all()
    )


@router.put("/{id_detalle}", response_model=DetalleHojaVidaResponse)
def modificar_detalle(
    id_detalle: int,
    detalle_data: DetalleHojaVidaUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(admin_required),
):
    detalle = db.query(DetalleHojaVida).filter(DetalleHojaVida.id_detalle == id_detalle).first()

    if not detalle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Detalle no encontrado")

    detalle.observaciones = detalle_data.observaciones
    db.commit()
    db.refresh(detalle)

    return detalle


@router.delete("/{id_detalle}", response_model=MessageResponse)
def eliminar_detalle(
    id_detalle: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(admin_required),
):
    detalle = db.query(DetalleHojaVida).filter(DetalleHojaVida.id_detalle == id_detalle).first()

    if not detalle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Detalle no encontrado")

    db.delete(detalle)
    db.commit()

    return MessageResponse(mensaje="Detalle eliminado correctamente")
