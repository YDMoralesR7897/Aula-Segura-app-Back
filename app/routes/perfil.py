# Importa utilidades de FastAPI para crear rutas, inyectar dependencias y lanzar errores HTTP.
from fastapi import APIRouter, Depends, HTTPException
# Importa el tipo Session de SQLAlchemy para trabajar con la base de datos.
from sqlalchemy.orm import Session
# Importa la funcion que devuelve una sesion de base de datos.
from app.database import get_db
# Importa el modelo Perfil para consultar y guardar perfiles.
from app.models.perfil import Perfil
# Importa el schema para validar datos del perfil en el body (JSON).
from app.schemas.perfil import PerfilCreate, PerfilUpdate

# Crea el enrutador de este modulo con prefijo /perfil y etiqueta para la documentacion.
router = APIRouter(prefix="/perfil", tags=["Perfil"])

# =========================
# CREAR PERFIL
# =========================
# Define un endpoint POST en /perfil/ para crear un perfil nuevo.
@router.post("/")
# Define la funcion del endpoint con body JSON y sesion de BD inyectada.
def crear_perfil(perfil_data: PerfilCreate, db: Session = Depends(get_db)):
    # Busca si ya existe un perfil con el mismo nombre.
    perfil_existente = db.query(Perfil).filter(Perfil.nombre == perfil_data.nombre).first()

    # Si existe, devuelve error 400 porque no se permite duplicar nombres.
    if perfil_existente:
        # Lanza una excepcion HTTP con detalle para el cliente.
        raise HTTPException(status_code=400, detail="El perfil ya existe")

    # Crea una instancia del modelo Perfil con los datos recibidos.
    nuevo_perfil = Perfil(nombre=perfil_data.nombre, descripcion=perfil_data.descripcion)
    # Marca la nueva instancia para insertar en la base de datos.
    db.add(nuevo_perfil)
    # Confirma la transaccion para guardar el registro.
    db.commit()
    # Recarga el objeto con valores actualizados desde la BD (por ejemplo, ID generado).
    db.refresh(nuevo_perfil)

    # Retorna el perfil creado como respuesta.
    return nuevo_perfil


# =========================
# CONSULTAR PERFILES ACTIVOS
# =========================
# Define un endpoint GET en /perfil/ para listar perfiles activos.
@router.get("/")
# Define la funcion que obtiene la sesion de BD por dependencia.
def listar_perfiles(db: Session = Depends(get_db)):
    # Retorna todos los perfiles cuyo estado es True (activos).
    return db.query(Perfil).filter(Perfil.estado == True).all()


# =========================
# MODIFICAR PERFIL
# =========================
# Define un endpoint PUT en /perfil/{id_perfil} para actualizar un perfil existente.
@router.put("/{id_perfil}")
# Define la funcion con ID del perfil, nuevos datos y sesion de BD.
def actualizar_perfil(id_perfil: int, perfil_data: PerfilUpdate, db: Session = Depends(get_db)):
    # Busca el perfil por su clave primaria.
    perfil = db.query(Perfil).filter(Perfil.id_perfil == id_perfil).first()

    # Si no existe, responde con error 404.
    if not perfil:
        # Lanza una excepcion indicando que el recurso no fue encontrado.
        raise HTTPException(status_code=404, detail="Perfil no encontrado")

    # Actualiza el nombre del perfil con el valor recibido.
    perfil.nombre = perfil_data.nombre
    # Actualiza la descripcion del perfil con el valor recibido.
    perfil.descripcion = perfil_data.descripcion
    # Guarda los cambios en la base de datos.
    db.commit()

    # Devuelve el perfil actualizado.
    return perfil


# =========================
# INHABILITAR PERFIL (BORRADO LOGICO)
# =========================
# Define un endpoint DELETE en /perfil/{id_perfil} para inhabilitar un perfil.
@router.delete("/{id_perfil}")
# Define la funcion con ID del perfil y sesion de BD.
def inhabilitar_perfil(id_perfil: int, db: Session = Depends(get_db)):
    # Busca el perfil que se desea inhabilitar.
    perfil = db.query(Perfil).filter(Perfil.id_perfil == id_perfil).first()

    # Si no existe el perfil, retorna error 404.
    if not perfil:
        # Lanza excepcion HTTP para notificar que no se encontro.
        raise HTTPException(status_code=404, detail="Perfil no encontrado")

    # Realiza borrado logico cambiando el estado a False.
    perfil.estado = False
    # Confirma el cambio en la base de datos.
    db.commit()

    # Retorna un mensaje simple de confirmacion.
    return {"mensaje": "Perfil inhabilitado correctamente"}
