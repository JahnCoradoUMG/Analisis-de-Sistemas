# GymFlow — Ejecución y pruebas

## Requisitos

| Escenario | Necesita |
|-----------|----------|
| Solo Docker | [Docker Desktop](https://docs.docker.com/desktop/) (o motor compatible) con plugin **Compose v2** |
| Local sin Docker | Python 3.11+, Redis accesible en `REDIS_URL` |

## Opción A: Docker Compose (recomendado)

Desde la carpeta del proyecto (`Tarea03`):

```bash
docker compose up --build
```

En segundo plano:

```bash
docker compose up --build -d
```

Parar y quitar contenedores:

```bash
docker compose down
```

- API: http://127.0.0.1:8000  
- Swagger: http://127.0.0.1:8000/docs  
- Salud (incluye estado de Redis): `GET /health` → `{"status":"ok","redis":"up"|"down"}`  
- Redis en el host: `localhost:6379`

Si `redis` aparece `down` en `/health`, revisa logs del contenedor `api` y que `REDIS_URL` apunte al servicio `redis` dentro de Compose (`redis://redis:6379/0`).

### Problemas frecuentes (Docker)

- **Puerto en uso:** otro proceso usa `8000` o `6379`. Cambia el mapeo en `docker-compose.yml`, por ejemplo `"8001:8000"`.
- **Docker no arranca:** en Windows, abre Docker Desktop y espera a que el motor esté *Running*.
- **OneDrive / rutas largas:** si el build falla al copiar contexto, prueba clonar o copiar el proyecto fuera de OneDrive.

## Opción B: Python local + Redis

1. Arranca Redis (por ejemplo `docker run -d -p 6379:6379 redis:7-alpine` o instalación local).
2. Variables (o copia `.env.example` a `.env` y carga con tu herramienta preferida):

```bash
# PowerShell
$env:REDIS_URL = "redis://127.0.0.1:6379/0"

# bash
export REDIS_URL=redis://127.0.0.1:6379/0
```

3. Instalar y ejecutar:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Si Redis no está disponible, la API arranca igualmente; `GET /clients/{id}` usará `X-Cache: BYPASS` y `/health` mostrará `"redis":"down"`.

## Probar cache (PowerShell)

En Windows, evita `curl -d '{...}'` sin escapar comillas; usa `Invoke-RestMethod`:

```powershell
$base = "http://127.0.0.1:8000"
$r = Invoke-RestMethod -Method Post -Uri "$base/clients" -ContentType "application/json" `
  -Body '{"full_name":"Demo","email":"demo@example.com"}'
$id = $r.id
(Invoke-WebRequest -Uri "$base/clients/$id" -UseBasicParsing).Headers["X-Cache"]   # MISS
(Invoke-WebRequest -Uri "$base/clients/$id" -UseBasicParsing).Headers["X-Cache"]   # HIT
```

## Probar con Postman

1. Importar `docs/GymFlow.postman_collection.json`.
2. Variable `baseUrl` = `http://127.0.0.1:8000`.
3. Orden sugerido: Health → Create Client → Get Client By ID (dos veces, revisar cabecera `X-Cache`) → Create Membership → Create Payment → Check-In.

## Validaciones esperadas

- Email de cliente duplicado: `409`.
- Referencias inválidas: `404` / `400` según endpoint.
- `POST /check-in` con membresía inactiva o fuera de vigencia: `400`.

## OpenAPI

Contrato en la raíz del repo: `openapi.yaml` (si está presente en tu copia). La fuente viva sigue siendo `/openapi.json` expuesto por FastAPI.
