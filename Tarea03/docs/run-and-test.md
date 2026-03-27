# GymFlow - Guia de ejecucion y pruebas

## 1) Requisitos previos
- Python 3.11+ instalado
- `pip` habilitado
- Postman (opcional, para pruebas manuales)

## 2) Instalar dependencias
Desde la carpeta `Tarea02`:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 3) Ejecutar FastAPI
```bash
uvicorn main:app --reload
```

La API quedara disponible en:
- `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## 4) Probar con Postman
1. Abrir Postman.
2. Importar el archivo `docs/GymFlow.postman_collection.json`.
3. Verificar variable `baseUrl` con valor `http://127.0.0.1:8000`.
4. Ejecutar requests en este orden:
   - `Health Check`
   - `Create Client`
   - `Get Client By ID`
   - `Create Membership`
   - `Create Payment`
   - `Check-In (Membership Validacion)`

La coleccion guarda automaticamente:
- `clientId` desde `Create Client`
- `membershipId` desde `Create Membership`

## 5) Validaciones clave esperadas
- Si el `email` de cliente ya existe: error `409`.
- Si no existe cliente o membresia en referencias: error `404` o `400` segun el caso.
- En `POST /check-in`, si la membresia no esta activa o no esta vigente: error `400`.

## 6) Export OpenAPI
El contrato OpenAPI para documentacion/manual QA se incluye en:
- `openapi.yaml`
