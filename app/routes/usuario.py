from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.dependencies import PaginationParams, pagination_params, require_profiles
from app.models.perfil import Perfil
from app.models.persona import Persona
from app.models.usuario import Usuario
from app.schemas.common import MessageResponse
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from app.utils.security import hash_password

router = APIRouter(prefix="/usuario", tags=["Usuario"])
settings = get_settings()
admin_required = require_profiles(*settings.admin_profile_ids)


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario(
    usuario_data: UsuarioCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(admin_required),
):
    usuario_existente = db.query(Usuario).filter(Usuario.username == usuario_data.username).first()
    if usuario_existente:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El username ya existe")

    persona = db.query(Persona).filter(Persona.id_persona == usuario_data.id_persona, Persona.estado.is_(True)).first()
    if not persona:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Persona no encontrada")

    perfil = db.query(Perfil).filter(Perfil.id_perfil == usuario_data.id_perfil, Perfil.estado.is_(True)).first()
    if not perfil:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil no encontrado")

    nuevo_usuario = Usuario(
        username=usuario_data.username,
        password=hash_password(usuario_data.password),
        id_persona=usuario_data.id_persona,
        id_perfil=usuario_data.id_perfil,
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(
    db: Session = Depends(get_db),
    pagination: PaginationParams = Depends(pagination_params),
    _: Usuario = Depends(admin_required),
):
    return (
        db.query(Usuario)
        .filter(Usuario.estado.is_(True))
        .offset(pagination.offset)
        .limit(pagination.limit)
        .all()
    )


@router.put("/{id_usuario}", response_model=UsuarioResponse)
def actualizar_usuario(
    id_usuario: int,
    usuario_data: UsuarioUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(admin_required),
):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    usuario.username = usuario_data.username
    usuario.password = hash_password(usuario_data.password)
    usuario.id_perfil = usuario_data.id_perfil

    db.commit()
    db.refresh(usuario)
    return usuario


@router.delete("/{id_usuario}", response_model=MessageResponse)
def inhabilitar_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(admin_required),
):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    usuario.estado = False
    db.commit()

    return MessageResponse(mensaje="Usuario inhabilitado correctamente")
