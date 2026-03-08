from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.detalle_hoja_vida import DetalleHojaVida

router = APIRouter(prefix="/detalle-hoja-vida", tags=["Detalle Hoja Vida"])


# CREAR REGISTRO
@router.post("/")
def crear_detalle(
    id_hoja: int,
    id_criterio: int,
    id_orientacion: int,
    id_tipop: int,
    observaciones: str,
    persona_registra: int,
    db: Session = Depends(get_db)
):

    nuevo = DetalleHojaVida(
        id_hoja=id_hoja,
        id_criterio=id_criterio,
        id_orientacion=id_orientacion,
        id_tipop=id_tipop,
        observaciones=observaciones,
        persona_registra=persona_registra
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


# CONSULTAR DETALLES
@router.get("/")
def listar_detalles(db: Session = Depends(get_db)):

    return db.query(DetalleHojaVida).all()


# CONSULTAR POR HOJA
@router.get("/hoja/{id_hoja}")
def detalles_por_hoja(id_hoja: int, db: Session = Depends(get_db)):

    return db.query(DetalleHojaVida).filter(
        DetalleHojaVida.id_hoja == id_hoja
    ).all()


# MODIFICAR
@router.put("/{id_detalle}")
def modificar_detalle(
    id_detalle: int,
    observaciones: str,
    db: Session = Depends(get_db)
):

    detalle = db.query(DetalleHojaVida).filter(
        DetalleHojaVida.id_detalle == id_detalle
    ).first()

    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")

    detalle.observaciones = observaciones

    db.commit()

    return {"mensaje": "Detalle actualizado"}