# Importa utilidades de FastAPI para rutas, dependencias y errores.
from fastapi import APIRouter, Depends, HTTPException
# Importa Session para interactuar con la base de datos usando SQLAlchemy.
from sqlalchemy.orm import Session
# Importa la funcion que entrega la conexion/sesion de BD.
from app.database import get_db
# Importa el modelo Persona para crear y consultar personas.
from app.models.persona import Persona
# Importa los schemas para validar datos JSON de entrada.
from app.schemas.persona import PersonaCreate, PersonaUpdate

# Crea el enrutador de persona con prefijo /persona.
router = APIRouter(prefix="/persona", tags=["Persona"])

# =========================
# CREAR PERSONA
# =========================
# Define un endpoint POST en /persona/ para registrar una persona.
@router.post("/")
# Define la funcion con datos de entrada y sesion de BD inyectada.
def crear_persona(persona_data: PersonaCreate, db: Session = Depends(get_db)):
    # Busca si ya existe una persona con el mismo correo.
    persona_existente = db.query(Persona).filter(Persona.correo == persona_data.correo).first()

    # Si el correo ya existe, responde con error 400.
    if persona_existente:
        # Lanza excepcion HTTP para evitar duplicados de correo.
        raise HTTPException(status_code=400, detail="El correo ya esta registrado")

    # Crea una nueva instancia Persona con los datos recibidos.
    nueva_persona = Persona(
        nombre=persona_data.nombre,
        apellido=persona_data.apellido,
        correo=persona_data.correo
    )
    # Agrega la nueva persona a la sesion.
    db.add(nueva_persona)
    # Confirma la insercion en la base de datos.
    db.commit()
    # Recarga el objeto para obtener valores actualizados desde BD.
    db.refresh(nueva_persona)

    # Devuelve la persona creada.
    return nueva_persona


# =========================
# CONSULTAR PERSONAS ACTIVAS
# =========================
# Define un endpoint GET en /persona/ para listar personas activas.
@router.get("/")
# Define la funcion que recibe la sesion de BD.
def listar_personas(db: Session = Depends(get_db)):
    # Devuelve todas las personas con estado True.
    return db.query(Persona).filter(Persona.estado == True).all()


# =========================
# MODIFICAR PERSONA
# =========================
# Define un endpoint PUT en /persona/{id_persona} para actualizar una persona.
@router.put("/{id_persona}")
# Define la funcion con ID, datos nuevos y sesion de BD.
def actualizar_persona(id_persona: int, persona_data: PersonaUpdate, db: Session = Depends(get_db)):
    # Busca la persona por su identificador unico.
    persona = db.query(Persona).filter(Persona.id_persona == id_persona).first()

    # Si no existe, responde con error 404.
    if not persona:
        # Lanza una excepcion indicando que no se encontro la persona.
        raise HTTPException(status_code=404, detail="Persona no encontrada")

    # Actualiza el nombre.
    persona.nombre = persona_data.nombre
    # Actualiza el apellido.
    persona.apellido = persona_data.apellido
    # Actualiza el correo.
    persona.correo = persona_data.correo
    # Guarda los cambios en la base de datos.
    db.commit()

    # Retorna la persona actualizada.
    return persona


# =========================
# INHABILITAR PERSONA
# =========================
# Define un endpoint DELETE en /persona/{id_persona} para borrar logicamente.
@router.delete("/{id_persona}")
# Define la funcion con el ID y la sesion de BD.
def inhabilitar_persona(id_persona: int, db: Session = Depends(get_db)):
    # Busca la persona que se quiere inhabilitar.
    persona = db.query(Persona).filter(Persona.id_persona == id_persona).first()

    # Si no existe, devuelve error 404.
    if not persona:
        # Lanza excepcion de recurso no encontrado.
        raise HTTPException(status_code=404, detail="Persona no encontrada")

    # Cambia el estado a False para inhabilitar sin eliminar fisicamente.
    persona.estado = False
    # Confirma el cambio en BD.
    db.commit()

    # Retorna un mensaje de confirmacion.
    return {"mensaje": "Persona inhabilitada correctamente"}
