# GymFlow — Sistema de gestión de gimnasio

API REST con **FastAPI** (clientes, membresías, pagos, check-in), **cache Redis** (cache-aside con TTL) en `GET /clients/{client_id}` y despliegue local con **Docker Compose**.

## Stack

- FastAPI, Pydantic  
- Almacenamiento en memoria (MVP)  
- Redis 7 (cache)  
- Docker / Docker Compose  

## Inicio rápido con Docker

```bash
docker compose up --build
```

Modo detached:

```bash
docker compose up --build -d
```

- API: http://127.0.0.1:8000  
- Documentación: http://127.0.0.1:8000/docs  
- Salud: `GET /health` → `status` y `redis` (`up` / `down`)  

Variables del servicio `api` (ver `docker-compose.yml`): `REDIS_URL`, `CACHE_TTL_CLIENT_SECONDS`.

### Solución de problemas

| Síntoma | Qué hacer |
|---------|-----------|
| Error al conectar con Docker | Iniciar Docker Desktop y esperar al estado *Running*. |
| `port is already allocated` | Liberar el puerto o cambiar `"8000:8000"` / `"6379:6379"` en `docker-compose.yml`. |
| `redis: down` en `/health` | Ver logs: `docker compose logs api`. La API reintenta Redis unos ~20 s al arrancar. |

Guía detallada: [docs/run-and-test.md](docs/run-and-test.md).

## Estructura del proyecto

```
Tarea03/
  main.py
  Dockerfile
  docker-compose.yml
  requirements.txt
  .env.example
  app/
    api/routes/
    core/config.py
    models/
    services/
  docs/
    architecture.md
    cache.md
    requirements.md
    run-and-test.md
    system-brief.md
```

## Ejecución local (sin contenedor de la API)

Necesitas Redis accesible. Ejemplo de variables:

```powershell
$env:REDIS_URL = "redis://127.0.0.1:6379/0"
```

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Plantilla de variables: [.env.example](.env.example).

## Endpoints principales

| Método | Ruta | Notas |
|--------|------|--------|
| `GET` | `/health` | `redis`: conexión a cache |
| `POST` | `/clients` | Alta de socio |
| `GET` | `/clients/{client_id}` | Cache Redis; cabecera `X-Cache`: `HIT`, `MISS` o `BYPASS` |
| `POST` | `/memberships` | |
| `POST` | `/payments` | |
| `POST` | `/check-in` | Membresía activa y vigente |

## Evidencia de cache (PowerShell)

```powershell
$base = "http://127.0.0.1:8000"
$r = Invoke-RestMethod -Method Post -Uri "$base/clients" -ContentType "application/json" `
  -Body '{"full_name":"Demo","email":"demo@example.com"}'
$id = $r.id
(Invoke-WebRequest -Uri "$base/clients/$id" -UseBasicParsing).Headers["X-Cache"]
(Invoke-WebRequest -Uri "$base/clients/$id" -UseBasicParsing).Headers["X-Cache"]
```

Primera línea: `MISS`. Segunda: `HIT` (con Redis activo).

## Documentación del curso

- [docs/architecture.md](docs/architecture.md) — diagramas Mermaid y rol de Redis  
- [docs/cache.md](docs/cache.md) — claves, TTL, estrategia  
- [docs/system-brief.md](docs/system-brief.md) — brief del sistema  
- [docs/requirements.md](docs/requirements.md) — requerimientos y backlog  
- [docs/run-and-test.md](docs/run-and-test.md) — ejecución y pruebas  

## Check-in

`POST /check-in` exige membresía existente, estado `active` y fecha entre `start_date` y `end_date`.
