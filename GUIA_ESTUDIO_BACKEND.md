# Guia De Estudio Del Backend Aula Segura

Esta guia explica el backend archivo por archivo. La idea no es solo decir "que hace", sino tambien "de donde viene" y "por que se hace asi".

## 1. Vision General

El proyecto esta construido con:

- `FastAPI`: framework web para exponer endpoints HTTP.
- `SQLAlchemy`: ORM para mapear clases Python a tablas MySQL.
- `Pydantic`: validacion de datos que entran y salen por la API.
- `PyMySQL`: driver para conectar Python con MySQL.
- `bcrypt`: hashing de contrasenas.

El flujo general es:

1. `main.py` crea la aplicacion FastAPI.
2. `app/database.py` configura la conexion a MySQL.
3. `app/models/*.py` define las tablas como clases.
4. `app/schemas/*.py` define la forma de los datos que entran y salen.
5. `app/routes/*.py` implementa los endpoints.
6. `seed_data.py` inserta datos iniciales para pruebas.

## 2. Archivo Principal

### [main.py](C:/Users/yerso/OneDrive/Desktop/programmingProjects/AulaSeguraAppBack/main.py)

`"""Launcher sencillo..."""`: este docstring describe el objetivo del archivo. No afecta la ejecucion; sirve como documentacion.

`from typing import Generator`: importa `Generator` desde la libreria estandar. Se usa para tipar la funcion `get_db`, porque esa funcion no devuelve un valor normal, sino que hace `yield`.

`from app.routes import persona, usuario, perfil`: importa tres modulos de rutas. Cada modulo trae un `router` con endpoints.

`from fastapi import FastAPI`: importa la clase principal de FastAPI. Esta clase representa la aplicacion web.

`from fastapi.middleware.cors import CORSMiddleware`: importa el middleware que permite que un frontend en otro origen haga peticiones al backend.

`from sqlalchemy import create_engine`: importa la funcion para crear motores de conexion a base de datos.

`from sqlalchemy.orm import sessionmaker, Session`: importa herramientas de SQLAlchemy ORM. `sessionmaker` fabrica sesiones y `Session` se usa para tipado.

`from app.routes import auth`: importa las rutas de autenticacion.

`from app.database import Base, engine`: importa la base declarativa y el motor principal desde `app/database.py`.

`from app.routes import tipo_persona`, `criterio_alerta`, `orientacion`, `hoja_vida`, `detalle_hoja_vida`: importa el resto de modulos de rutas.

`app = FastAPI(title="Aula Segura API")`: crea la aplicacion. `title` se usa especialmente en la documentacion Swagger.

`app.add_middleware(...)`: registra middleware CORS.

`CORSMiddleware`: le dice a FastAPI que intercepte peticiones del navegador antes de llegar a las rutas.

`allow_origins=[...]`: lista de orígenes permitidos. Aqui se autorizan los puertos comunes de Vite en local.

`allow_credentials=True`: permite enviar cookies o cabeceras de autenticacion entre frontend y backend.

`allow_methods=["*"]`: permite todos los metodos HTTP.

`allow_headers=["*"]`: permite todas las cabeceras HTTP.

`app.include_router(...)`: cada llamada agrega un grupo de rutas a la app. Por ejemplo, `perfil.router` aporta endpoints como `GET /perfil/` y `POST /perfil/`.

`DATABASE_URL = "mysql+pymysql://..."`: define una cadena de conexion local. El formato es `dialecto+driver://usuario:clave@host:puerto/base`.

`engine = create_engine(DATABASE_URL)`: crea un motor nuevo. Este `engine` local sobra un poco porque ya existe uno en `app.database`; funcionalmente es otra conexion equivalente.

`SessionLocal = sessionmaker(...)`: fabrica sesiones nuevas enlazadas al `engine`.

`def get_db() -> Generator[Session, None, None]:`: define una dependencia para FastAPI. Cada request que la use obtiene una sesion SQLAlchemy y al final se cierra.

`db = SessionLocal()`: crea una sesion nueva.

`try: yield db`: entrega la sesion a la ruta que la solicito.

`finally: db.close()`: cierre garantizado de la sesion, incluso si hubo error.

`Base.metadata.create_all(bind=engine)`: revisa todos los modelos registrados en `Base` y crea las tablas que no existan.

`@app.get("/")`: decorador que registra una ruta GET en `/`.

`async def read_root():`: funcion asincrona que responde al root.

`return {"message": ...}`: devuelve JSON.

`if __name__ == "__main__":`: este bloque solo corre cuando ejecutas `python main.py` directamente.

`import uvicorn`: importa el servidor ASGI.

`uvicorn.run("main:app", ...)`: inicia el servidor apuntando a la variable `app` del modulo `main`.

El bloque SQL final dentro de triple comilla no se ejecuta. Es solo una nota/manual incrustado por el autor.

## 3. Conexion A Base De Datos

### [app/database.py](C:/Users/yerso/OneDrive/Desktop/programmingProjects/AulaSeguraAppBack/app/database.py)

`from sqlalchemy import create_engine`: trae la funcion para abrir conexion de alto nivel.

`from sqlalchemy.orm import sessionmaker, declarative_base`: `sessionmaker` crea sesiones y `declarative_base` crea la clase base sobre la que heredan todos los modelos.

`from sqlalchemy.orm import Session`: se importa para tipado o documentacion.

`DATABASE_URL = ...`: define la conexion principal a MySQL.

`engine = create_engine(DATABASE_URL)`: crea el motor compartido del proyecto.

`SessionLocal = sessionmaker(...)`: fabrica sesiones ORM que luego se usan en rutas.

`Base = declarative_base()`: esta variable es critica. Todas las clases modelo que heredan de `Base` quedan registradas como tablas.

`def get_db():`: dependencia usada en rutas.

`db = SessionLocal()`: crea sesion.

`yield db`: entrega la sesion a la ruta.

`db.close()`: la cierra al terminar.

## 4. Seguridad De Contrasenas

### [app/utils/security.py](C:/Users/yerso/OneDrive/Desktop/programmingProjects/AulaSeguraAppBack/app/utils/security.py)

`import base64`, `import hashlib`, `import bcrypt`: traen utilidades criptograficas.

`def _prehash(password: str) -> bytes:`: funcion interna. Recibe una contrasena en texto y devuelve bytes.

`digest = hashlib.sha256(password.encode("utf-8")).digest()`: convierte el string a bytes UTF-8, calcula SHA-256 y obtiene el resultado binario.

`return base64.b64encode(digest)`: codifica el hash binario en Base64 para que bcrypt reciba un tamaño controlado.

La razon de este prehash es el limite de 72 bytes de entrada que tiene bcrypt.

`def hash_password(password: str):`: funcion publica para guardar una contrasena.

`bcrypt.hashpw(_prehash(password), bcrypt.gensalt())`: aplica bcrypt al valor prehasheado con una sal aleatoria.

`.decode("utf-8")`: convierte el hash final a string para almacenarlo en la base de datos.

`def verify_password(plain_password: str, hashed_password: str):`: compara una contrasena escrita por el usuario contra el hash guardado.

`bcrypt.checkpw(...)`: devuelve `True` o `False`.

`except ValueError: return False`: evita que hashes invalidos rompan el login.

## 5. Modelos ORM

Los modelos representan tablas. Cada atributo `Column(...)` representa una columna real.

### [app/models/perfil.py](C:/Users/yerso/OneDrive/Desktop/programmingProjects/AulaSeguraAppBack/app/models/perfil.py)

`Column`, `Integer`, `String`, `Boolean`: tipos de columnas SQLAlchemy.

`Base`: clase base declarativa.

`class Perfil(Base)`: clase que representa la tabla `perfil`.

`__tablename__ = "perfil"`: nombre exacto de la tabla en MySQL.

`id_perfil = Column(Integer, primary_key=True, index=True)`: clave primaria autoincremental e indexada.

`nombre = Column(String(50), nullable=False, unique=True)`: nombre obligatorio y unico.

`descripcion = Column(String(150))`: texto opcional.

`estado = Column(Boolean, default=True)`: usado para borrado logico.

### [app/models/persona.py](C:/Users/yerso/OneDrive/Desktop/programmingProjects/AulaSeguraAppBack/app/models/persona.py)

La estructura es igual a `Perfil`, pero ahora representa personas.

`correo` es `unique=True`: no puede haber dos personas con el mismo correo.

### [app/models/usuario.py](C:/Users/yerso/OneDrive/Desktop/programmingProjects/AulaSeguraAppBack/app/models/usuario.py)

`ForeignKey("persona.id_persona")`: indica que `id_persona` depende de un registro existente en la tabla `persona`.

`unique=True` en `id_persona`: fuerza relacion 1 a 1 entre `usuario` y `persona`.

`ForeignKey("perfil.id_perfil")`: enlaza cada usuario a un perfil.

`relationship("Persona")`: permite hacer `usuario.persona` y obtener el objeto relacionado.

`relationship("Perfil")`: permite hacer `usuario.perfil`.

### [app/models/tipo_persona.py](C:/Users/yerso/OneDrive/Desktop/programmingProjects/AulaSeguraAppBack/app/models/tipo_persona.py)

Tabla catalogo para clasificar quien registra o participa.

`nombretp`: nombre del tipo.

`descripciontp`: descripcion corta.

### [app/models/criterio_alerta.py](C:/Users/yerso/OneDrive/Desktop/programmingProjects/AulaSeguraAppBack/app/models/criterio_alerta.py)

Tabla catalogo para criterios de alerta como bullying o ausentismo.

### [app/models/orientacion_no_clinica.py](C:/Users/yerso/OneDrive/Desktop/programmingProjects/AulaSeguraAppBack/app/models/orientacion_no_clinica.py)

Tabla catalogo para orientaciones.

### [app/models/hoja_vida.py](C:/Users/yerso/OneDrive/Desktop/programmingProjects/AulaSeguraAppBack/app/models/hoja_vida.py)

`id_hoja`: PK.

`id_persona = Column(Integer, ForeignKey("persona.id_persona"))`: cada hoja pertenece a una persona.

`fecha_registro = Column(DateTime, server_default=func.now())`: si no envias fecha, MySQL pone la actual.

`estado = Column(Boolean, default=True)`: activa/inactiva.

### [app/models/detalle_hoja_vida.py](C:/Users/yerso/OneDrive/Desktop/programmingProjects/AulaSeguraAppBack/app/models/detalle_hoja_vida.py)

Esta tabla guarda eventos o anotaciones dentro de una hoja de vida.

`id_hoja`: a que hoja pertenece el detalle.

`fecha = Column(DateTime, server_default=func.now())`: fecha automatica del detalle.

`id_criterio`: FK a criterio de alerta.

`id_orientacion`: FK a orientacion no clinica.

`id_tipop`: FK a tipo persona.

`observaciones = Column(Text)`: texto libre del caso.

`persona_registra`: FK a persona que hace el registro.

### [app/models/__init__.py](C:/Users/yerso/OneDrive/Desktop/programmingProjects/AulaSeguraAppBack/app/models/__init__.py)

Importa algunos modulos para exponerlos como paquete. No es esencial para FastAPI, pero ayuda a estructurar.

## 6. Schemas Pydantic

Los schemas controlan que JSON acepta o devuelve la API.

### [app/schemas/auth.py](C:/Users/yerso/OneDrive/Desktop/programmingProjects/AulaSeguraAppBack/app/schemas/auth.py)

`class RecuperarPasswordRequest(BaseModel)`: valida que el body traiga `correo`.

`class LoginRequest(BaseModel)`: valida `username` y `password`.

### [app/schemas/perfil.py](C:/Users/yerso/OneDrive/Desktop/programmingProjects/AulaSeguraAppBack/app/schemas/perfil.py)

`PerfilCreate`: body para crear perfil.

`PerfilUpdate`: body para modificar perfil.

Ambos tienen `nombre` y `descripcion`.

### [app/schemas/persona.py](C:/Users/yerso/OneDrive/Desktop/programmingProjects/AulaSeguraAppBack/app/schemas/persona.py)

Define `nombre`, `apellido`, `correo` para crear o actualizar persona.

### [app/schemas/usuario.py](C:/Users/yerso/OneDrive/Desktop/programmingProjects/AulaSeguraAppBack/app/schemas/usuario.py)

`ConfigDict` viene de Pydantic v2 y permite configuraciones del schema.

`UsuarioBase`: evita repetir campos comunes.

`UsuarioCreate(UsuarioBase)`: hereda esos campos y agrega `password`.

`UsuarioUpdate`: en este proyecto permite cambiar `username`, `password` y `id_perfil`.

`UsuarioResponse(UsuarioBase)`: schema de salida.

`model_config = ConfigDict(from_attributes=True)`: permite convertir objetos ORM directamente a este schema sin transformarlos manualmente a diccionario.

### [app/schemas/tipo_persona.py](C:/Users/yerso/OneDrive/Desktop/programmingProjects/AulaSeguraAppBack/app/schemas/tipo_persona.py)

`TipoPersonaCreate`: requiere `nombretp` y `descripciontp`.

`TipoPersonaUpdate`: solo pide `nombretp`.

### [app/schemas/criterio_alerta.py](C:/Users/yerso/OneDrive/Desktop/programmingProjects/AulaSeguraAppBack/app/schemas/criterio_alerta.py)

Tanto create como update usan solo `nombre`.

### [app/schemas/orientacion.py](C:/Users/yerso/OneDrive/Desktop/programmingProjects/AulaSeguraAppBack/app/schemas/orientacion.py)

Igual al anterior, solo con `nombre`.

### [app/schemas/hoja_vida.py](C:/Users/yerso/OneDrive/Desktop/programmingProjects/AulaSeguraAppBack/app/schemas/hoja_vida.py)

Para crear hoja solo se necesita `id_persona`.

### [app/schemas/detalle_hoja_vida.py](C:/Users/yerso/OneDrive/Desktop/programmingProjects/AulaSeguraAppBack/app/schemas/detalle_hoja_vida.py)

`DetalleHojaVidaCreate`: requiere todos los ids relacionados y `observaciones`.

`DetalleHojaVidaUpdate`: en este proyecto solo deja actualizar `observaciones`.

## 7. Rutas FastAPI

Cada archivo de `routes` expone un conjunto de endpoints.

### [app/routes/perfil.py](C:/Users/yerso/OneDrive/Desktop/programmingProjects/AulaSeguraAppBack/app/routes/perfil.py)

`APIRouter(...)`: crea un router con prefijo `/perfil`.

`@router.post("/")`: define el endpoint crear.

`perfil_existente = db.query(...).first()`: consulta si ya existe un perfil con ese nombre.

`raise HTTPException(...)`: aborta la request con un codigo y mensaje HTTP.

`nuevo_perfil = Perfil(...)`: crea una instancia ORM en memoria.

`db.add(...)`: pone la instancia en la sesion.

`db.commit()`: confirma la transaccion en la base de datos.

`db.refresh(...)`: vuelve a cargar el objeto ya persistido para tener el id generado.

`@router.get("/")`: lista perfiles activos.

`.filter(Perfil.estado == True).all()`: filtra por activos y devuelve lista.

`@router.put("/{id_perfil}")`: modifica por id.

`perfil.nombre = ...`, `perfil.descripcion = ...`: cambia atributos del objeto ORM. SQLAlchemy detecta el cambio y lo traduce a `UPDATE` en `commit`.

`@router.delete("/{id_perfil}")`: no borra fisicamente; hace borrado logico con `estado = False`.

### [app/routes/persona.py](C:/Users/yerso/OneDrive/Desktop/programmingProjects/AulaSeguraAppBack/app/routes/persona.py)

La logica es equivalente a `perfil`, pero usando `correo` como validacion de unicidad.

### [app/routes/usuario.py](C:/Users/yerso/OneDrive/Desktop/programmingProjects/AulaSeguraAppBack/app/routes/usuario.py)

Este archivo tiene mas validaciones porque `Usuario` depende de `Persona` y `Perfil`.

`usuario_existente = db.query(Usuario)...`: valida username unico.

`persona = db.query(Persona)...`: asegura que la FK apunte a una persona real.

`perfil = db.query(Perfil)...`: asegura que la FK apunte a un perfil real.

`password=hash_password(usuario_data.password)`: nunca guarda la contrasena plana en la base.

`@router.get("/", response_model=list[UsuarioResponse])`: obliga a que la salida cumpla el schema `UsuarioResponse`.

En `actualizar_usuario`, observa algo importante: la contrasena se guarda como llega y no se vuelve a hashear. Eso es un detalle tecnico a corregir en el futuro.

### [app/routes/auth.py](C:/Users/yerso/OneDrive/Desktop/programmingProjects/AulaSeguraAppBack/app/routes/auth.py)

`from fastapi_mail import FastMail, MessageSchema`: integra envio de correos.

`from app.config.mail import conf`: importa la configuracion SMTP. Ese archivo no aparece en el listado principal que revisamos, pero se espera que exista para el modulo mail.

`generar_password_temporal()`: arma un string aleatorio de 8 caracteres alfanumericos.

`@router.post("/login")`: endpoint de autenticacion.

`usuario = db.query(Usuario)...`: busca usuario por username.

`verify_password(login_data.password, usuario.password)`: compara password ingresada contra hash guardado.

`if not usuario.estado`: evita login de usuarios inactivos.

`return {...}`: devuelve un JSON simple. Aqui no hay JWT ni tokens; es autenticacion basica para prototipo.

`@router.post("/recuperar-password")`: flujo de recuperacion.

`.join(Persona)`: hace join SQL entre `usuario` y `persona`.

`Persona.correo == correo`: busca el usuario a partir del correo de la persona.

`usuario.password = hash_password(nueva_password)`: reemplaza el hash por una contrasena temporal.

`MessageSchema(...)`: define asunto, destinatario y cuerpo del correo.

`await fm.send_message(mensaje)`: envia el correo de forma asincrona.

### [app/routes/tipo_persona.py](C:/Users/yerso/OneDrive/Desktop/programmingProjects/AulaSeguraAppBack/app/routes/tipo_persona.py)

CRUD simple de catalogo.

`crear_tipo_persona`: inserta un tipo.

`listar_tipo_persona`: solo devuelve activos.

`modificar_tipo_persona`: permite cambiar solo el nombre.

`inhabilitar_tipo_persona`: hace borrado logico.

### [app/routes/criterio_alerta.py](C:/Users/yerso/OneDrive/Desktop/programmingProjects/AulaSeguraAppBack/app/routes/criterio_alerta.py)

Mismo patron del catalogo anterior.

### [app/routes/orientacion.py](C:/Users/yerso/OneDrive/Desktop/programmingProjects/AulaSeguraAppBack/app/routes/orientacion.py)

Tambien sigue el mismo patron CRUD con borrado logico.

### [app/routes/hoja_vida.py](C:/Users/yerso/OneDrive/Desktop/programmingProjects/AulaSeguraAppBack/app/routes/hoja_vida.py)

`crear_hoja_vida`: crea una hoja asociada a una persona.

`listar_hojas`: lista solo hojas activas.

`eliminar_hoja`: no borra fisicamente, solo desactiva.

### [app/routes/detalle_hoja_vida.py](C:/Users/yerso/OneDrive/Desktop/programmingProjects/AulaSeguraAppBack/app/routes/detalle_hoja_vida.py)

`crear_detalle`: inserta un detalle completo.

`listar_detalles`: devuelve todos los detalles, sin filtrar por estado porque esta tabla no tiene columna `estado`.

`detalles_por_hoja`: devuelve los detalles de una hoja especifica.

`modificar_detalle`: solo actualiza `observaciones`.

`eliminar_detalle`: borra fisicamente el detalle con `db.delete(detalle)`.

Eso es distinto a otros modulos que usan borrado logico.

## 8. Datos Iniciales

### [seed_data.py](C:/Users/yerso/OneDrive/Desktop/programmingProjects/AulaSeguraAppBack/seed_data.py)

Este archivo sirve para poblar la base con datos coherentes.

Cada funcion `get_or_create_*` sigue el mismo patron:

1. Busca si el registro ya existe con un criterio de negocio.
2. Si existe, lo devuelve.
3. Si no existe, lo crea, hace `db.add`, luego `db.flush`.

`db.flush()` no hace commit definitivo. Solo fuerza a SQLAlchemy a sincronizar con la base y obtener ids generados para seguir usandolos dentro de la misma transaccion.

`seed()`:

`Base.metadata.create_all(bind=engine)`: se asegura de que las tablas existan.

`db = SessionLocal()`: abre una sesion.

`try:`: encapsula toda la siembra como una sola transaccion logica.

`admin`, `orientador`, `docente`: crea perfiles.

`p_admin`, `p_orientador`, `p_docente`, `p_estudiante`: crea personas.

`get_or_create_usuario(...)`: crea usuarios con contrasenas hasheadas.

`tp_orientador`, `tp_docente`, `tp_acudiente`: crea catalogo de tipos de persona.

`c_bullying`, `c_ausentismo`, `c_rendimiento`: crea criterios de alerta.

`o_citacion`, `o_plan`, `o_taller`: crea orientaciones.

`hoja_estudiante = get_or_create_hoja_vida(...)`: crea la hoja de vida del estudiante.

Las tres llamadas a `get_or_create_detalle(...)`: crean eventos relacionados a esa hoja.

`db.commit()`: guarda toda la siembra.

`except Exception: db.rollback()`: si algo falla, deshace todo.

`finally: db.close()`: cierra la sesion.

`if __name__ == "__main__": seed()`: permite ejecutar el archivo directamente.

## 9. Flujo Completo De Una Peticion

Ejemplo: crear un usuario.

1. El frontend envia `POST /usuario/` con JSON.
2. FastAPI recibe la request en [app/routes/usuario.py](C:/Users/yerso/OneDrive/Desktop/programmingProjects/AulaSeguraAppBack/app/routes/usuario.py).
3. Pydantic valida el body contra `UsuarioCreate`.
4. FastAPI inyecta una sesion `db` usando `get_db`.
5. La ruta consulta si el username ya existe.
6. Valida que existan la persona y el perfil.
7. Hashea la contrasena.
8. Crea el objeto `Usuario`.
9. Hace `commit`.
10. Responde JSON.

## 10. Conceptos Clave Que Debes Entender

`APIRouter`: agrupa rutas relacionadas.

`Depends(get_db)`: le dice a FastAPI que antes de ejecutar la ruta cree e inyecte la sesion de BD.

`BaseModel`: clase de Pydantic para validar datos.

`Base`: clase base ORM para modelos SQLAlchemy.

`ForeignKey`: relacion entre tablas.

`relationship`: acceso orientado a objetos entre modelos relacionados.

`commit`: guarda definitivamente.

`refresh`: recarga el objeto desde la base.

`rollback`: deshace cambios no confirmados.

`borrado logico`: no elimina la fila; cambia un flag como `estado=False`.

`borrado fisico`: elimina la fila con `DELETE`.

## 11. Observaciones Tecnicas Del Proyecto

Hay algunos puntos importantes para aprender leyendo este codigo:

- En [main.py](C:/Users/yerso/OneDrive/Desktop/programmingProjects/AulaSeguraAppBack/main.py) se redefine `engine` y `SessionLocal`, aunque ya existen en [app/database.py](C:/Users/yerso/OneDrive/Desktop/programmingProjects/AulaSeguraAppBack/app/database.py). Funciona, pero es redundante.
- En [app/routes/usuario.py](C:/Users/yerso/OneDrive/Desktop/programmingProjects/AulaSeguraAppBack/app/routes/usuario.py) la actualizacion de password no la vuelve a hashear.
- `login` devuelve un JSON simple, no un token JWT. Para un prototipo esta bien, para produccion no.
- Algunos archivos ya tienen comentarios docentes y otros no; esta guia busca unificar la explicacion.

## 12. Orden Recomendado Para Estudiarlo

1. Lee [app/database.py](C:/Users/yerso/OneDrive/Desktop/programmingProjects/AulaSeguraAppBack/app/database.py).
2. Lee los modelos de `app/models`.
3. Lee los schemas de `app/schemas`.
4. Lee las rutas mas simples: `perfil`, `persona`, `criterio_alerta`.
5. Luego revisa `usuario` y `auth`.
6. Finalmente estudia `hoja_vida`, `detalle_hoja_vida` y [seed_data.py](C:/Users/yerso/OneDrive/Desktop/programmingProjects/AulaSeguraAppBack/seed_data.py).

Si quieres, el siguiente paso util es hacer una segunda guia igual para el frontend o convertir esta guia en preguntas y respuestas tipo examen.
