from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.dependencies import PaginationParams, pagination_params, require_profiles
from app.models.hoja_vida import HojaVida
from app.models.persona import Persona
from app.models.usuario import Usuario
from app.schemas.common import MessageResponse
from app.schemas.hoja_vida import HojaVidaCreate, HojaVidaResponse

router = APIRouter(prefix="/hoja-vida", tags=["Hoja Vida"])
settings = get_settings()
admin_required = require_profiles(*settings.admin_profile_ids)


@router.post("/", response_model=HojaVidaResponse, status_code=status.HTTP_201_CREATED)
def crear_hoja_vida(
    hoja_data: HojaVidaCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(admin_required),
):
    persona = db.query(Persona).filter(Persona.id_persona == hoja_data.id_persona, Persona.estado.is_(True)).first()
    if not persona:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Persona no encontrada")

    nueva = HojaVida(id_persona=hoja_data.id_persona)

    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    return nueva


@router.get("/", response_model=list[HojaVidaResponse])
def listar_hojas(
    db: Session = Depends(get_db),
    pagination: PaginationParams = Depends(pagination_params),
    _: Usuario = Depends(admin_required),
):
    return (
        db.query(HojaVida)
        .filter(HojaVida.estado.is_(True))
        .offset(pagination.offset)
        .limit(pagination.limit)
        .all()
    )


@router.delete("/{id_hoja}", response_model=MessageResponse)
def eliminar_hoja(
    id_hoja: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(admin_required),
):
    hoja = db.query(HojaVida).filter(HojaVida.id_hoja == id_hoja).first()

    if not hoja:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hoja no encontrada")

    hoja.estado = False

    db.commit()

    return MessageResponse(mensaje="Hoja de vida inhabilitada")
