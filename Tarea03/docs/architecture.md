# GymFlow - Arquitectura (v1)

Este documento describe la arquitectura del API **GymFlow**, construido con **FastAPI**, **Pydantic** y **almacenamiento en memoria** (diccionarios de Python).

## Objetivo

Proveer una API REST modular para:

- Clientes
- Membresias
- Pagos
- Check-in con validacion de membresia vigente

## Estructura de carpetas

```
Tarea02/
  main.py
  requirements.txt
  openapi.yaml
  app/
    api/
      router.py
      routes/
        clients.py
        memberships.py
        payments.py
        checkins.py
    models/
      schemas.py
    services/
      storage.py
      client_service.py
      membership_service.py
      payment_service.py
      checkin_service.py
  docs/
    run-and-test.md
    GymFlow.postman_collection.json
    architecture.md
```

## Capas y responsabilidades

### 1) Capa de API (Rutas)

Ubicacion: `app/api/routes/*.py`

- Define endpoints y contratos (request/response) via modelos Pydantic.
- No contiene logica compleja: delega a servicios.

Router central: `app/api/router.py` agrega todos los routers de rutas.

### 2) Capa de Servicios (Logica de negocio)

Ubicacion: `app/services/*.py`

- Implementa reglas de negocio y validaciones del dominio.
- Centraliza el acceso al almacenamiento en memoria.
- Lanza errores HTTP (FastAPI) con codigos y mensajes consistentes.

Servicios principales:

- `ClientService`: crea y consulta clientes (incluye validacion de email unico).
- `MembershipService`: crea membresias y valida vigencia/estado para check-in.
- `PaymentService`: crea pagos y valida referencias (cliente/membresia).
- `CheckInService`: registra check-in y exige membresia activa+vigente.

### 3) Capa de Modelos (Esquemas)

Ubicacion: `app/models/schemas.py`

- Modelos Pydantic para requests y responses.
- Validaciones de datos (ej: `end_date > start_date`, `amount > 0`).
- Enums del dominio (`MembershipStatus`, `PaymentMethod`).

### 4) Almacenamiento (In-Memory)

Ubicacion: `app/services/storage.py`

- `InMemoryStorage` mantiene diccionarios:
  - `clients: dict[id, Client]`
  - `memberships: dict[id, Membership]`
  - `payments: dict[id, Payment]`
  - `checkins: dict[id, CheckIn]`
- Nota: al reiniciar la app, los datos se pierden (es intencional para v1).

## Flujos principales

### Alta de cliente

1. `POST /clients` -> `ClientService.create`
2. Se valida email unico (si existe: `409`).
3. Se genera `id` y se guarda en memoria.

### Crear membresia

1. `POST /memberships` -> `MembershipService.create`
2. Se valida existencia de cliente (si no existe: `404`).
3. Se guarda la membresia.

### Registrar pago

1. `POST /payments` -> `PaymentService.create`
2. Se valida cliente existe (`404`).
3. Se valida membresia existe (`404`) y pertenece al cliente (`400`).
4. Se guarda el pago.

### Check-in (regla critica)

1. `POST /check-in` -> `CheckInService.create`
2. Valida cliente existe (`404`).
3. Busca la membresia mas reciente del cliente.
4. Valida:
  - existe membresia (`400` si no hay),
  - `status == active` (`400` si no),
  - `start_date <= checked_in_at <= end_date` (`400` si no).
5. Registra el check-in asociado a la `membership_id`.

## Contrato y documentacion

- Documentacion interactiva: `GET /docs` (Swagger UI).
- Contrato OpenAPI YAML: `openapi.yaml`.
- Coleccion de pruebas Postman: `docs/GymFlow.postman_collection.json`.

## Consideraciones y limites (v1)

- Sin base de datos: no hay persistencia.
- Sin autenticacion/autorizacion (roles fuera de alcance en esta entrega).
- Concurrencia: al ser in-memory, no esta disenado para multiples instancias ni escalado horizontal.

