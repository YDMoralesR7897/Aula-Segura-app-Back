from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine
from app.models.criterio_alerta import CriterioAlerta
from app.models.detalle_hoja_vida import DetalleHojaVida
from app.models.hoja_vida import HojaVida
from app.models.orientacion_no_clinica import OrientacionNoClinica
from app.models.perfil import Perfil
from app.models.persona import Persona
from app.models.tipo_persona import TipoPersona
from app.models.usuario import Usuario
from app.utils.security import hash_password


def get_or_create_perfil(db: Session, nombre: str, descripcion: str) -> Perfil:
    perfil = db.query(Perfil).filter(Perfil.nombre == nombre).first()
    if perfil:
        return perfil
    perfil = Perfil(nombre=nombre, descripcion=descripcion, estado=True)
    db.add(perfil)
    db.flush()
    return perfil


def get_or_create_persona(
    db: Session, nombre: str, apellido: str, correo: str
) -> Persona:
    persona = db.query(Persona).filter(Persona.correo == correo).first()
    if persona:
        return persona
    persona = Persona(nombre=nombre, apellido=apellido, correo=correo, estado=True)
    db.add(persona)
    db.flush()
    return persona


def get_or_create_usuario(
    db: Session, username: str, plain_password: str, id_persona: int, id_perfil: int
) -> Usuario:
    usuario = db.query(Usuario).filter(Usuario.username == username).first()
    if usuario:
        return usuario
    usuario = Usuario(
        username=username,
        password=hash_password(plain_password),
        id_persona=id_persona,
        id_perfil=id_perfil,
        estado=True,
    )
    db.add(usuario)
    db.flush()
    return usuario


def get_or_create_tipo_persona(
    db: Session, nombretp: str, descripciontp: str
) -> TipoPersona:
    tipo = db.query(TipoPersona).filter(TipoPersona.nombretp == nombretp).first()
    if tipo:
        return tipo
    tipo = TipoPersona(nombretp=nombretp, descripciontp=descripciontp, estado=True)
    db.add(tipo)
    db.flush()
    return tipo


def get_or_create_criterio(db: Session, nombre: str) -> CriterioAlerta:
    criterio = db.query(CriterioAlerta).filter(CriterioAlerta.nombre == nombre).first()
    if criterio:
        return criterio
    criterio = CriterioAlerta(nombre=nombre, estado=True)
    db.add(criterio)
    db.flush()
    return criterio


def get_or_create_orientacion(db: Session, nombre: str) -> OrientacionNoClinica:
    orientacion = (
        db.query(OrientacionNoClinica)
        .filter(OrientacionNoClinica.nombre == nombre)
        .first()
    )
    if orientacion:
        return orientacion
    orientacion = OrientacionNoClinica(nombre=nombre, estado=True)
    db.add(orientacion)
    db.flush()
    return orientacion


def get_or_create_hoja_vida(db: Session, id_persona: int) -> HojaVida:
    hoja = db.query(HojaVida).filter(HojaVida.id_persona == id_persona).first()
    if hoja:
        return hoja
    hoja = HojaVida(id_persona=id_persona, estado=True)
    db.add(hoja)
    db.flush()
    return hoja


def get_or_create_detalle(
    db: Session,
    id_hoja: int,
    id_criterio: int,
    id_orientacion: int,
    id_tipop: int,
    observaciones: str,
    persona_registra: int,
) -> DetalleHojaVida:
    detalle = (
        db.query(DetalleHojaVida)
        .filter(
            DetalleHojaVida.id_hoja == id_hoja,
            DetalleHojaVida.id_criterio == id_criterio,
            DetalleHojaVida.persona_registra == persona_registra,
        )
        .first()
    )
    if detalle:
        return detalle
    detalle = DetalleHojaVida(
        id_hoja=id_hoja,
        id_criterio=id_criterio,
        id_orientacion=id_orientacion,
        id_tipop=id_tipop,
        observaciones=observaciones,
        persona_registra=persona_registra,
    )
    db.add(detalle)
    db.flush()
    return detalle


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        admin = get_or_create_perfil(db, "Admin", "Administrador del sistema")
        orientador = get_or_create_perfil(db, "Orientador", "Gestion de convivencia")
        docente = get_or_create_perfil(db, "Docente", "Docente de aula")

        p_admin = get_or_create_persona(
            db, "Laura", "Gomez", "laura.gomez@aulasegura.local"
        )
        p_orientador = get_or_create_persona(
            db, "Carlos", "Ruiz", "carlos.ruiz@aulasegura.local"
        )
        p_docente = get_or_create_persona(
            db, "Ana", "Torres", "ana.torres@aulasegura.local"
        )
        p_estudiante = get_or_create_persona(
            db, "Mateo", "Perez", "mateo.perez@aulasegura.local"
        )

        get_or_create_usuario(db, "admin", "Admin123*", p_admin.id_persona, admin.id_perfil)
        get_or_create_usuario(
            db,
            "orientador.carlos",
            "Orienta123*",
            p_orientador.id_persona,
            orientador.id_perfil,
        )
        get_or_create_usuario(
            db, "docente.ana", "Docente123*", p_docente.id_persona, docente.id_perfil
        )

        tp_orientador = get_or_create_tipo_persona(
            db, "Orientador", "Profesional de apoyo no clinico"
        )
        tp_docente = get_or_create_tipo_persona(
            db, "Docente", "Docente titular del curso"
        )
        tp_acudiente = get_or_create_tipo_persona(
            db, "Acudiente", "Responsable familiar del estudiante"
        )

        c_bullying = get_or_create_criterio(db, "Bullying")
        c_ausentismo = get_or_create_criterio(db, "Ausentismo reiterado")
        c_rendimiento = get_or_create_criterio(db, "Bajo rendimiento academico")

        o_citacion = get_or_create_orientacion(db, "Citacion a acudiente")
        o_plan = get_or_create_orientacion(db, "Plan de acompanamiento")
        o_taller = get_or_create_orientacion(db, "Taller de habilidades sociales")

        hoja_estudiante = get_or_create_hoja_vida(db, p_estudiante.id_persona)

        get_or_create_detalle(
            db,
            hoja_estudiante.id_hoja,
            c_bullying.id_criterio,
            o_taller.id_orientacion,
            tp_orientador.id_tipop,
            "Se reportan comentarios ofensivos frecuentes en descanso.",
            p_orientador.id_persona,
        )
        get_or_create_detalle(
            db,
            hoja_estudiante.id_hoja,
            c_ausentismo.id_criterio,
            o_citacion.id_orientacion,
            tp_docente.id_tipop,
            "Tres inasistencias injustificadas durante la ultima semana.",
            p_docente.id_persona,
        )
        get_or_create_detalle(
            db,
            hoja_estudiante.id_hoja,
            c_rendimiento.id_criterio,
            o_plan.id_orientacion,
            tp_acudiente.id_tipop,
            "Se acuerda plan de estudio con seguimiento quincenal.",
            p_admin.id_persona,
        )

        db.commit()

        print("Seed completado")
        print("Usuarios de prueba:")
        print("  admin / Admin123*")
        print("  orientador.carlos / Orienta123*")
        print("  docente.ana / Docente123*")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
