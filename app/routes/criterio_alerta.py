from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.criterio_alerta import CriterioAlerta

router = APIRouter(prefix="/criterio-alerta", tags=["Criterio Alerta"])


# CREAR
@router.post("/")
def crear_criterio(nombre: str, db: Session = Depends(get_db)):

    nuevo = CriterioAlerta(nombre=nombre)

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


# CONSULTAR
@router.get("/")
def listar_criterios(db: Session = Depends(get_db)):
    return db.query(CriterioAlerta).filter(CriterioAlerta.estado == True).all()


# MODIFICAR
@router.put("/{id_criterio}")
def modificar_criterio(id_criterio: int, nombre: str, db: Session = Depends(get_db)):

    criterio = db.query(CriterioAlerta).filter(
        CriterioAlerta.id_criterio == id_criterio
    ).first()

    if not criterio:
        raise HTTPException(status_code=404, detail="Criterio no encontrado")

    criterio.nombre = nombre

    db.commit()

    return {"mensaje": "Criterio actualizado"}


# INHABILITAR
@router.delete("/{id_criterio}")
def inhabilitar_criterio(id_criterio: int, db: Session = Depends(get_db)):

    criterio = db.query(CriterioAlerta).filter(
        CriterioAlerta.id_criterio == id_criterio
    ).first()

    if not criterio:
        raise HTTPException(status_code=404, detail="Criterio no encontrado")

    criterio.estado = False

    db.commit()

    return {"mensaje": "Criterio inhabilitado"}