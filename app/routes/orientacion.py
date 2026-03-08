from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.orientacion_no_clinica import OrientacionNoClinica

router = APIRouter(prefix="/orientacion", tags=["Orientaciones No Clínicas"])


# CREAR
@router.post("/")
def crear_orientacion(nombre: str, db: Session = Depends(get_db)):

    nueva = OrientacionNoClinica(nombre=nombre)

    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    return nueva


# CONSULTAR
@router.get("/")
def listar_orientaciones(db: Session = Depends(get_db)):
    return db.query(OrientacionNoClinica).filter(
        OrientacionNoClinica.estado == True
    ).all()


# MODIFICAR
@router.put("/{id_orientacion}")
def modificar_orientacion(id_orientacion: int, nombre: str, db: Session = Depends(get_db)):

    orientacion = db.query(OrientacionNoClinica).filter(
        OrientacionNoClinica.id_orientacion == id_orientacion
    ).first()

    if not orientacion:
        raise HTTPException(status_code=404, detail="Orientación no encontrada")

    orientacion.nombre = nombre

    db.commit()

    return {"mensaje": "Orientación actualizada"}


# INHABILITAR
@router.delete("/{id_orientacion}")
def inhabilitar_orientacion(id_orientacion: int, db: Session = Depends(get_db)):

    orientacion = db.query(OrientacionNoClinica).filter(
        OrientacionNoClinica.id_orientacion == id_orientacion
    ).first()

    if not orientacion:
        raise HTTPException(status_code=404, detail="Orientación no encontrada")

    orientacion.estado = False

    db.commit()

    return {"mensaje": "Orientación inhabilitada"}