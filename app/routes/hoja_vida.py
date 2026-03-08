from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.hoja_vida import HojaVida
from app.schemas.hoja_vida import HojaVidaCreate

router = APIRouter(prefix="/hoja-vida", tags=["Hoja Vida"])


# CREAR HOJA DE VIDA
@router.post("/")
def crear_hoja_vida(hoja_data: HojaVidaCreate, db: Session = Depends(get_db)):

    nueva = HojaVida(id_persona=hoja_data.id_persona)

    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    return nueva


# CONSULTAR
@router.get("/")
def listar_hojas(db: Session = Depends(get_db)):

    return db.query(HojaVida).filter(HojaVida.estado == True).all()


# INHABILITAR
@router.delete("/{id_hoja}")
def eliminar_hoja(id_hoja: int, db: Session = Depends(get_db)):

    hoja = db.query(HojaVida).filter(HojaVida.id_hoja == id_hoja).first()

    if not hoja:
        raise HTTPException(status_code=404, detail="Hoja no encontrada")

    hoja.estado = False

    db.commit()

    return {"mensaje": "Hoja de vida inhabilitada"}
