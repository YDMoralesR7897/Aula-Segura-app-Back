from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.perfil import Perfil

router = APIRouter(prefix="/perfil", tags=["Perfil"])

# =========================
# CREAR PERFIL
# =========================
@router.post("/")
def crear_perfil(nombre: str, descripcion: str, db: Session = Depends(get_db)):
    perfil_existente = db.query(Perfil).filter(Perfil.nombre == nombre).first()
    
    if perfil_existente:
        raise HTTPException(status_code=400, detail="El perfil ya existe")

    nuevo_perfil = Perfil(nombre=nombre, descripcion=descripcion)
    db.add(nuevo_perfil)
    db.commit()
    db.refresh(nuevo_perfil)

    return nuevo_perfil


# =========================
# CONSULTAR PERFILES ACTIVOS
# =========================
@router.get("/")
def listar_perfiles(db: Session = Depends(get_db)):
    return db.query(Perfil).filter(Perfil.estado == True).all()


# =========================
# MODIFICAR PERFIL
# =========================
@router.put("/{id_perfil}")
def actualizar_perfil(id_perfil: int, nombre: str, descripcion: str, db: Session = Depends(get_db)):
    perfil = db.query(Perfil).filter(Perfil.id_perfil == id_perfil).first()

    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")

    perfil.nombre = nombre
    perfil.descripcion = descripcion
    db.commit()

    return perfil


# =========================
# INHABILITAR PERFIL (BORRADO LOGICO)
# =========================
@router.delete("/{id_perfil}")
def inhabilitar_perfil(id_perfil: int, db: Session = Depends(get_db)):
    perfil = db.query(Perfil).filter(Perfil.id_perfil == id_perfil).first()

    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")

    perfil.estado = False
    db.commit()

    return {"mensaje": "Perfil inhabilitado correctamente"}