from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.dependencies import PaginationParams, pagination_params, require_profiles
from app.models.criterio_alerta import CriterioAlerta
from app.models.usuario import Usuario
from app.schemas.common import MessageResponse
from app.schemas.criterio_alerta import CriterioAlertaCreate, CriterioAlertaResponse, CriterioAlertaUpdate

router = APIRouter(prefix="/criterio-alerta", tags=["Criterio Alerta"])
settings = get_settings()
admin_required = require_profiles(*settings.admin_profile_ids)


@router.post("/", response_model=CriterioAlertaResponse, status_code=status.HTTP_201_CREATED)
def crear_criterio(
    criterio_data: CriterioAlertaCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(admin_required),
):
    nuevo = CriterioAlerta(nombre=criterio_data.nombre)

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


@router.get("/", response_model=list[CriterioAlertaResponse])
def listar_criterios(
    db: Session = Depends(get_db),
    pagination: PaginationParams = Depends(pagination_params),
    _: Usuario = Depends(admin_required),
):
    return (
        db.query(CriterioAlerta)
        .filter(CriterioAlerta.estado.is_(True))
        .offset(pagination.offset)
        .limit(pagination.limit)
        .all()
    )


@router.put("/{id_criterio}", response_model=CriterioAlertaResponse)
def modificar_criterio(
    id_criterio: int,
    criterio_data: CriterioAlertaUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(admin_required),
):
    criterio = db.query(CriterioAlerta).filter(CriterioAlerta.id_criterio == id_criterio).first()

    if not criterio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Criterio no encontrado")

    criterio.nombre = criterio_data.nombre

    db.commit()
    db.refresh(criterio)

    return criterio


@router.delete("/{id_criterio}", response_model=MessageResponse)
def inhabilitar_criterio(
    id_criterio: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(admin_required),
):
    criterio = db.query(CriterioAlerta).filter(CriterioAlerta.id_criterio == id_criterio).first()

    if not criterio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Criterio no encontrado")

    criterio.estado = False

    db.commit()

    return MessageResponse(mensaje="Criterio inhabilitado")
