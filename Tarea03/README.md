# GymFlow - Sistema de Gestion de Gimnasio

API REST construida con FastAPI para gestionar clientes, membresias, pagos y check-in.

## Stack
- FastAPI
- Pydantic
- Almacenamiento en memoria (diccionarios de Python)

## Estructura del proyecto
```
Tarea02/
  app/
    api/
      routes/
        clients.py
        memberships.py
        payments.py
        checkins.py
      router.py
    models/
      schemas.py
    services/
      storage.py
      client_service.py
      membership_service.py
      payment_service.py
      checkin_service.py
  main.py
  requirements.txt
```

## Instalacion y ejecucion
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## Endpoints
- `POST /clients`
- `GET /clients/{client_id}`
- `POST /memberships`
- `POST /payments`
- `POST /check-in`

## Regla clave de negocio
El endpoint `POST /check-in` valida que el cliente tenga una membresia:
- existente,
- en estado `active`,
- vigente segun `start_date` y `end_date`.
