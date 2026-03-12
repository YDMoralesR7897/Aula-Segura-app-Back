from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.dependencies import PaginationParams, pagination_params, require_profiles
from app.models.tipo_persona import TipoPersona
from app.models.usuario import Usuario
from app.schemas.common import MessageResponse
from app.schemas.tipo_persona import TipoPersonaCreate, TipoPersonaResponse, TipoPersonaUpdate

router = APIRouter(prefix="/tipo-persona", tags=["Tipo Persona"])
settings = get_settings()
admin_required = require_profiles(*settings.admin_profile_ids)


@router.post("/", response_model=TipoPersonaResponse, status_code=status.HTTP_201_CREATED)
def crear_tipo_persona(
    tipo_persona_data: TipoPersonaCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(admin_required),
):
    nuevo = TipoPersona(
        nombretp=tipo_persona_data.nombretp,
        descripciontp=tipo_persona_data.descripciontp,
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.get("/", response_model=list[TipoPersonaResponse])
def listar_tipo_persona(
    db: Session = Depends(get_db),
    pagination: PaginationParams = Depends(pagination_params),
    _: Usuario = Depends(admin_required),
):
    return (
        db.query(TipoPersona)
        .filter(TipoPersona.estado.is_(True))
        .offset(pagination.offset)
        .limit(pagination.limit)
        .all()
    )


@router.put("/{id_tipop}", response_model=TipoPersonaResponse)
def modificar_tipo_persona(
    id_tipop: int,
    tipo_persona_data: TipoPersonaUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(admin_required),
):
    tipo = db.query(TipoPersona).filter(TipoPersona.id_tipop == id_tipop).first()

    if not tipo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo persona no encontrado")

    tipo.nombretp = tipo_persona_data.nombretp

    db.commit()
    db.refresh(tipo)
    return tipo


@router.delete("/{id_tipop}", response_model=MessageResponse)
def inhabilitar_tipo_persona(
    id_tipop: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(admin_required),
):
    tipo = db.query(TipoPersona).filter(TipoPersona.id_tipop == id_tipop).first()

    if not tipo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo persona no encontrado")

    tipo.estado = False
    db.commit()

    return MessageResponse(mensaje="Tipo persona inhabilitado")
