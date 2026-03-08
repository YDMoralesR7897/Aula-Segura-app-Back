from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.detalle_hoja_vida import DetalleHojaVida
from app.schemas.detalle_hoja_vida import DetalleHojaVidaCreate, DetalleHojaVidaUpdate

router = APIRouter(prefix="/detalle-hoja-vida", tags=["Detalle Hoja Vida"])


# CREAR REGISTRO
@router.post("/")
def crear_detalle(detalle_data: DetalleHojaVidaCreate, db: Session = Depends(get_db)):

    nuevo = DetalleHojaVida(
        id_hoja=detalle_data.id_hoja,
        id_criterio=detalle_data.id_criterio,
        id_orientacion=detalle_data.id_orientacion,
        id_tipop=detalle_data.id_tipop,
        observaciones=detalle_data.observaciones,
        persona_registra=detalle_data.persona_registra
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
def modificar_detalle(id_detalle: int, detalle_data: DetalleHojaVidaUpdate, db: Session = Depends(get_db)):

    detalle = db.query(DetalleHojaVida).filter(
        DetalleHojaVida.id_detalle == id_detalle
    ).first()

    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")

    detalle.observaciones = detalle_data.observaciones

    db.commit()

    return {"mensaje": "Detalle actualizado"}
