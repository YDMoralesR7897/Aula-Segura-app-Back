# AulaSeguraAppBack - FastAPI

Instrucciones rápidas para arrancar el proyecto localmente.

1. Crear y activar un entorno virtual

PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

CMD:

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

2. Instalar dependencias

```powershell
pip install -r requirements.txt
```

3. Ejecutar la aplicación

```powershell
python -m uvicorn main:app --reload
# o
python main.py
```

La app quedará disponible en http://127.0.0.1:8000
