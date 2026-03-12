# AulaSeguraAppBack

Backend API de Aula Segura construido con FastAPI + SQLAlchemy.

## Requisitos

- Python 3.10+
- Base de datos (MySQL recomendada para desarrollo real)

## Configuracion

1. Crear entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instalar dependencias:

```powershell
pip install -r requirements.txt
```

3. Crear archivo de entorno:

```powershell
Copy-Item .env.example .env
```

4. Ajustar `DATABASE_URL`, `JWT_SECRET_KEY` y datos de correo en `.env`.

## Migraciones

Aplicar migracion inicial:

```powershell
alembic upgrade head
```

Crear nuevas migraciones:

```powershell
alembic revision -m "descripcion_cambio"
```

## Ejecucion

```powershell
uvicorn main:app --reload
```

- API: http://127.0.0.1:8000/
- Docs: http://127.0.0.1:8000/docs

## Pruebas

```powershell
pytest
```
