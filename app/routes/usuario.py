from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.models.persona import Persona
from app.models.perfil import Perfil
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.utils.security import hash_password 

router = APIRouter(prefix="/usuario", tags=["Usuario"])

# =========================
# CREAR USUARIO
# =========================
@router.post("/")
def crear_usuario(username: str, password: str, id_persona: int, id_perfil: int, db: Session = Depends(get_db)):
    
    usuario_existente = db.query(Usuario).filter(Usuario.username == username).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El username ya existe")

    persona = db.query(Persona).filter(Persona.id_persona == id_persona).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")

    perfil = db.query(Perfil).filter(Perfil.id_perfil == id_perfil).first()
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")

    nuevo_usuario = Usuario(
    username=username,
    password=hash_password(password),
    id_persona=id_persona,
    id_perfil=id_perfil
)

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return nuevo_usuario


# =========================
# LISTAR USUARIOS
# =========================

@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).filter(Usuario.estado == True).all()


# =========================
# MODIFICAR USUARIO
# =========================
@router.put("/{id_usuario}")
def actualizar_usuario(id_usuario: int, username: str, password: str, id_perfil: int, db: Session = Depends(get_db)):
    
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.username = username
    usuario.password = password
    usuario.id_perfil = id_perfil

    db.commit()

    return usuario


# =========================
# INHABILITAR USUARIO
# =========================
@router.delete("/{id_usuario}")
def inhabilitar_usuario(id_usuario: int, db: Session = Depends(get_db)):

    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.estado = False
    db.commit()

    return {"mensaje": "Usuario inhabilitado correctamente"}