from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.persona import Persona

router = APIRouter(prefix="/persona", tags=["Persona"])

# =========================
# CREAR PERSONA
# =========================
@router.post("/")
def crear_persona(nombre: str, apellido: str, correo: str, db: Session = Depends(get_db)):
    persona_existente = db.query(Persona).filter(Persona.correo == correo).first()
    
    if persona_existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    nueva_persona = Persona(nombre=nombre, apellido=apellido, correo=correo)
    db.add(nueva_persona)
    db.commit()
    db.refresh(nueva_persona)

    return nueva_persona


# =========================
# CONSULTAR PERSONAS ACTIVAS
# =========================
@router.get("/")
def listar_personas(db: Session = Depends(get_db)):
    return db.query(Persona).filter(Persona.estado == True).all()


# =========================
# MODIFICAR PERSONA
# =========================
@router.put("/{id_persona}")
def actualizar_persona(id_persona: int, nombre: str, apellido: str, correo: str, db: Session = Depends(get_db)):
    persona = db.query(Persona).filter(Persona.id_persona == id_persona).first()

    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")

    persona.nombre = nombre
    persona.apellido = apellido
    persona.correo = correo
    db.commit()

    return persona


# =========================
# INHABILITAR PERSONA
# =========================
@router.delete("/{id_persona}")
def inhabilitar_persona(id_persona: int, db: Session = Depends(get_db)):
    persona = db.query(Persona).filter(Persona.id_persona == id_persona).first()

    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")

    persona.estado = False
    db.commit()

    return {"mensaje": "Persona inhabilitada correctamente"}