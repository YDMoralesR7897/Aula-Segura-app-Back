from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.dependencies import PaginationParams, pagination_params, require_profiles
from app.models.perfil import Perfil
from app.models.usuario import Usuario
from app.schemas.common import MessageResponse
from app.schemas.perfil import PerfilCreate, PerfilResponse, PerfilUpdate

router = APIRouter(prefix="/perfil", tags=["Perfil"])
settings = get_settings()
admin_required = require_profiles(*settings.admin_profile_ids)


@router.post("/", response_model=PerfilResponse, status_code=status.HTTP_201_CREATED)
def crear_perfil(
    perfil_data: PerfilCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(admin_required),
):
    perfil_existente = db.query(Perfil).filter(Perfil.nombre == perfil_data.nombre).first()
    if perfil_existente:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El perfil ya existe")

    nuevo_perfil = Perfil(nombre=perfil_data.nombre, descripcion=perfil_data.descripcion)
    db.add(nuevo_perfil)
    db.commit()
    db.refresh(nuevo_perfil)

    return nuevo_perfil


@router.get("/", response_model=list[PerfilResponse])
def listar_perfiles(
    db: Session = Depends(get_db),
    pagination: PaginationParams = Depends(pagination_params),
    _: Usuario = Depends(admin_required),
):
    return (
        db.query(Perfil)
        .filter(Perfil.estado.is_(True))
        .offset(pagination.offset)
        .limit(pagination.limit)
        .all()
    )


@router.put("/{id_perfil}", response_model=PerfilResponse)
def actualizar_perfil(
    id_perfil: int,
    perfil_data: PerfilUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(admin_required),
):
    perfil = db.query(Perfil).filter(Perfil.id_perfil == id_perfil).first()
    if not perfil:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil no encontrado")

    perfil.nombre = perfil_data.nombre
    perfil.descripcion = perfil_data.descripcion
    db.commit()
    db.refresh(perfil)

    return perfil


@router.delete("/{id_perfil}", response_model=MessageResponse)
def inhabilitar_perfil(
    id_perfil: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(admin_required),
):
    perfil = db.query(Perfil).filter(Perfil.id_perfil == id_perfil).first()
    if not perfil:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil no encontrado")

    perfil.estado = False
    db.commit()

    return MessageResponse(mensaje="Perfil inhabilitado correctamente")
