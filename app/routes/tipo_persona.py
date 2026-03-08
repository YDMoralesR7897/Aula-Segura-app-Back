from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.tipo_persona import TipoPersona

router = APIRouter(prefix="/tipo-persona", tags=["Tipo Persona"])


# CREAR
@router.post("/")
def crear_tipo_persona(nombretp: str, descripciontp: str, db: Session = Depends(get_db)):
    
    nuevo = TipoPersona(
        nombretp=nombretp,
        descripciontp=descripciontp
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


# CONSULTAR
@router.get("/")
def listar_tipo_persona(db: Session = Depends(get_db)):
    return db.query(TipoPersona).filter(TipoPersona.estado == True).all()


# MODIFICAR
@router.put("/{id_tipop}")
def modificar_tipo_persona(id_tipop: int, nombretp: str, db: Session = Depends(get_db)):

    tipo = db.query(TipoPersona).filter(TipoPersona.id_tipop == id_tipop).first()

    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo persona no encontrado")

    tipo.nombretp = nombretp

    db.commit()

    return {"mensaje": "Actualizado correctamente"}


# INHABILITAR
@router.delete("/{id_tipop}")
def inhabilitar_tipo_persona(id_tipop: int, db: Session = Depends(get_db)):

    tipo = db.query(TipoPersona).filter(TipoPersona.id_tipop == id_tipop).first()

    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo persona no encontrado")

    tipo.estado = False

    db.commit()

    return {"mensaje": "Tipo persona inhabilitado"}