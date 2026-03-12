from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.dependencies import PaginationParams, pagination_params, require_profiles
from app.models.persona import Persona
from app.models.usuario import Usuario
from app.schemas.common import MessageResponse
from app.schemas.persona import PersonaCreate, PersonaResponse, PersonaUpdate

router = APIRouter(prefix="/persona", tags=["Persona"])
settings = get_settings()
admin_required = require_profiles(*settings.admin_profile_ids)


@router.post("/", response_model=PersonaResponse, status_code=status.HTTP_201_CREATED)
def crear_persona(
    persona_data: PersonaCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(admin_required),
):
    persona_existente = db.query(Persona).filter(Persona.correo == persona_data.correo).first()
    if persona_existente:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El correo ya esta registrado")

    nueva_persona = Persona(nombre=persona_data.nombre, apellido=persona_data.apellido, correo=persona_data.correo)
    db.add(nueva_persona)
    db.commit()
    db.refresh(nueva_persona)

    return nueva_persona


@router.get("/", response_model=list[PersonaResponse])
def listar_personas(
    db: Session = Depends(get_db),
    pagination: PaginationParams = Depends(pagination_params),
    _: Usuario = Depends(admin_required),
):
    return (
        db.query(Persona)
        .filter(Persona.estado.is_(True))
        .offset(pagination.offset)
        .limit(pagination.limit)
        .all()
    )


@router.put("/{id_persona}", response_model=PersonaResponse)
def actualizar_persona(
    id_persona: int,
    persona_data: PersonaUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(admin_required),
):
    persona = db.query(Persona).filter(Persona.id_persona == id_persona).first()
    if not persona:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Persona no encontrada")

    persona.nombre = persona_data.nombre
    persona.apellido = persona_data.apellido
    persona.correo = persona_data.correo
    db.commit()
    db.refresh(persona)

    return persona


@router.delete("/{id_persona}", response_model=MessageResponse)
def inhabilitar_persona(
    id_persona: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(admin_required),
):
    persona = db.query(Persona).filter(Persona.id_persona == id_persona).first()
    if not persona:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Persona no encontrada")

    persona.estado = False
    db.commit()

    return MessageResponse(mensaje="Persona inhabilitada correctamente")
