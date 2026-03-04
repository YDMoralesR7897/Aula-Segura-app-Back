# AulaSeguraAppBack — Instrucciones de ejecución

Pasos rápidos para ejecutar la API en desarrollo (Windows):

1. Abrir terminal y situarse en la carpeta del proyecto:

```powershell
cd C:\Users\yerso\OneDrive\Desktop\programmingProjects\AulaSeguraAppBack
```

2. Crear y activar el entorno virtual (si no existe):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1    # PowerShell
# o .\.venv\Scripts\activate    # cmd
```

3. Instalar dependencias:

```powershell
pip install -r app\requirements.txt
```

4. Configurar la base de datos (opcional):

- Edita la variable `DATABASE_URL` en `main.py` si necesitas cambiar usuario, contraseña, host, puerto o nombre de la BD.

5. Ejecutar la aplicación:

```powershell
# Ejecutar con el launcher (archivo raíz)
python main.py

# O ejecutar con uvicorn (recomendado para desarrollo)
uvicorn main:app --reload
```

6. Acceder al servicio:

- API: http://127.0.0.1:8000/
- Docs interactivos: http://127.0.0.1:8000/docs

Notas:
- El archivo `app\requirements.txt` contiene las dependencias usadas (FastAPI, Uvicorn, SQLAlchemy, PyMySQL).
- Si aparece `ModuleNotFoundError` instala el paquete faltante con `pip install <paquete>`.