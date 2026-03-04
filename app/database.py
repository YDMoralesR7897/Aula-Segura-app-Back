# Importa 'create_engine' para crear la conexión a la base de datos
from sqlalchemy import create_engine

# Importa 'sessionmaker' para crear sesiones de base de datos y 'declarative_base' para definir modelos
from sqlalchemy.orm import sessionmaker, declarative_base

# Importa 'Session' (tipo de dato para sesiones de SQLAlchemy)
from sqlalchemy.orm import Session

# Define la cadena de conexión a la base de datos MySQL con usuario, contraseña, host y nombre de BD
DATABASE_URL = "mysql+pymysql://root:root123@localhost:3306/aula_segura"

# Crea un motor de SQLAlchemy que maneja la conexión a la base de datos
engine = create_engine(DATABASE_URL)

# Crea una fábrica de sesiones con autocommit y autoflush desactivados, vinculada al motor
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crea una clase base para definir modelos de ORM (mapeo objeto-relacional)
Base = declarative_base()

# Define una función generadora que proporciona una sesión de base de datos
def get_db():
    # Crea una nueva sesión de base de datos
    db = SessionLocal()
    # Intenta usar la sesión
    try:
        yield db
    # En caso de error o al finalizar, ejecuta el bloque finally
    finally:
        # Cierra la conexión de la sesión
        db.close()