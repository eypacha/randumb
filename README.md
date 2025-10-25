
# Randumb API

API de ejemplo usando FastAPI, SQLite y Pydantic para insultos piratas aleatorios.

## Uso rápido

1. Instala dependencias:
   ```sh
   pip install -r requirements.txt
   ```
2. Ejecuta el servidor (desde la raíz):
   ```sh
   uvicorn app.main:app --reload
   ```


## Endpoints

- `POST /pirates/` — Agrega un insulto pirata

## Estructura

- `app/models/` — Modelos de base de datos (listo para crecer)
- `app/schemas/` — Esquemas Pydantic (ver `pirates.py`)
- `app/functions/` — Lógica de negocio y acceso a datos (ver `pirates.py`)
- `app/routes/` — Endpoints de la API (ver `pirates.py`)
- `app/main.py` — Punto de entrada de la aplicación

En la raíz quedan solo archivos de configuración y documentación.
