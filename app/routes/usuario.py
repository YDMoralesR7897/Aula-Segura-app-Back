# Importa utilidades de FastAPI para crear rutas, dependencias y errores HTTP.
from fastapi import APIRouter, Depends, HTTPException
# Importa el tipo Session para manejar transacciones con SQLAlchemy.
from sqlalchemy.orm import Session
# Importa la funcion que entrega la sesion de base de datos.
from app.database import get_db
# Importa el modelo Usuario para consultas y registros de usuarios.
from app.models.usuario import Usuario
# Importa el modelo Persona para validar que la persona exista.
from app.models.persona import Persona
# Importa el modelo Perfil para validar que el perfil exista.
from app.models.perfil import Perfil
# Importa esquemas de salida/entrada relacionados con usuario.
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioUpdate
# Importa la funcion para cifrar la contrasena antes de guardarla.
from app.utils.security import hash_password

# Crea el enrutador para endpoints de usuario con prefijo /usuario.
router = APIRouter(prefix="/usuario", tags=["Usuario"])

# =========================
# CREAR USUARIO
# =========================
# Define un endpoint POST en /usuario/ para crear un nuevo usuario.
@router.post("/")
# Define la funcion con datos del usuario y sesion de BD inyectada.
def crear_usuario(usuario_data: UsuarioCreate, db: Session = Depends(get_db)):
    # Busca si ya existe un usuario con el mismo username.
    usuario_existente = db.query(Usuario).filter(Usuario.username == usuario_data.username).first()
    # Si ya existe, responde con error 400.
    if usuario_existente:
        # Lanza una excepcion HTTP para indicar username duplicado.
        raise HTTPException(status_code=400, detail="El username ya existe")

    # Busca la persona asociada por su ID.
    persona = db.query(Persona).filter(Persona.id_persona == usuario_data.id_persona).first()
    # Si no existe la persona, responde 404.
    if not persona:
        # Lanza error indicando que la persona no fue encontrada.
        raise HTTPException(status_code=404, detail="Persona no encontrada")

    # Busca el perfil asociado por su ID.
    perfil = db.query(Perfil).filter(Perfil.id_perfil == usuario_data.id_perfil).first()
    # Si no existe el perfil, responde 404.
    if not perfil:
        # Lanza error indicando que el perfil no fue encontrado.
        raise HTTPException(status_code=404, detail="Perfil no encontrado")

    # Crea una instancia Usuario con los datos recibidos.
    nuevo_usuario = Usuario(
        # Asigna el nombre de usuario.
        username=usuario_data.username,
        # Guarda la contrasena cifrada, no en texto plano.
        password=hash_password(usuario_data.password),
        # Guarda la referencia a la persona.
        id_persona=usuario_data.id_persona,
        # Guarda la referencia al perfil.
        id_perfil=usuario_data.id_perfil
    )

    # Agrega el nuevo usuario a la sesion.
    db.add(nuevo_usuario)
    # Confirma la transaccion en la base de datos.
    db.commit()
    # Refresca el objeto para cargar datos generados por BD (como ID).
    db.refresh(nuevo_usuario)

    # Retorna el usuario creado.
    return nuevo_usuario


# =========================
# LISTAR USUARIOS
# =========================
# Define un endpoint GET en /usuario/ para listar usuarios activos.
@router.get("/", response_model=list[UsuarioResponse])
# Define la funcion con inyeccion de sesion de BD.
def listar_usuarios(db: Session = Depends(get_db)):
    # Devuelve todos los usuarios con estado True.
    return db.query(Usuario).filter(Usuario.estado == True).all()


# =========================
# MODIFICAR USUARIO
# =========================
# Define un endpoint PUT en /usuario/{id_usuario} para actualizar datos.
@router.put("/{id_usuario}")
# Define la funcion con ID, nuevos valores y sesion de BD.
def actualizar_usuario(id_usuario: int, usuario_data: UsuarioUpdate, db: Session = Depends(get_db)):
    # Busca el usuario por su ID.
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()

    # Si no existe, devuelve error 404.
    if not usuario:
        # Lanza excepcion indicando que el usuario no existe.
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Actualiza el username.
    usuario.username = usuario_data.username
    # Actualiza la contrasena (en este codigo se guarda como llega).
    usuario.password = usuario_data.password
    # Actualiza el perfil asignado.
    usuario.id_perfil = usuario_data.id_perfil

    # Guarda los cambios en la base de datos.
    db.commit()

    # Retorna el usuario actualizado.
    return usuario


# =========================
# INHABILITAR USUARIO
# =========================
# Define un endpoint DELETE en /usuario/{id_usuario} para borrado logico.
@router.delete("/{id_usuario}")
# Define la funcion con ID y sesion de BD.
def inhabilitar_usuario(id_usuario: int, db: Session = Depends(get_db)):
    # Busca el usuario por su ID.
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()

    # Si no lo encuentra, responde con 404.
    if not usuario:
        # Lanza error de recurso no encontrado.
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Marca al usuario como inactivo.
    usuario.estado = False
    # Confirma el cambio en la BD.
    db.commit()

    # Devuelve un mensaje de confirmacion.
    return {"mensaje": "Usuario inhabilitado correctamente"}
