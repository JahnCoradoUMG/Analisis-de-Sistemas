# Cache con Redis — GymFlow

## Endpoints con cache

| Método y ruta | Uso de Redis |
|---------------|--------------|
| `GET /clients/{client_id}` | Cache-aside del documento JSON del socio (modelo `Client`). |

### Por qué este endpoint

La consulta de ficha de socio en recepción o en kioscos suele repetirse muchas veces con los mismos `client_id` mientras el dato cambia con poca frecuencia. Cachear esta lectura reduce latencia y presión sobre la fuente principal (hoy, almacenamiento en memoria dentro del mismo proceso; en el futuro podría ser una base de datos).

## Claves en Redis

| Clave | Contenido |
|-------|-----------|
| `gymflow:client:{client_id}` | JSON serializado del `Client` (id, full_name, email, phone, created_at). |

Convención de prefijo `gymflow:` para evitar colisiones con otros servicios en el mismo Redis de desarrollo.

## TTL

- **Variable de entorno:** `CACHE_TTL_CLIENT_SECONDS`
- **Valor por defecto:** `300` segundos (5 minutos)
- **En Docker Compose:** se fija explícitamente en `300` para el servicio `api`.

Toda escritura en cache usa `SET ... EX` (TTL obligatorio). Si la clave expira, el siguiente `GET` vuelve a la fuente y repuebla el cache.

## Estrategia: cache-aside

1. La aplicación intenta leer primero en Redis.
2. Si hay valor válido (**cache hit**), se deserializa y se responde sin consultar el almacenamiento principal.
3. Si no hay valor (**cache miss**), se lee del almacenamiento principal; si existe el recurso, se guarda en Redis con TTL y se responde.

No se usa *write-through*: los `POST` que crean clientes no escriben cache (el nuevo id no se consultará hasta el primer `GET`).

## Comportamiento por escenario

### Cache hit

- Redis devuelve el JSON del socio.
- Respuesta HTTP incluye cabecera `X-Cache: HIT`.
- No se accede al diccionario en memoria para la lectura del documento cacheado.

### Cache miss

- Redis no tiene la clave (o expiró).
- Se obtiene el cliente desde `InMemoryStorage` (o se responde `404` si no existe).
- Si el cliente existe, se hace `SET` con TTL y `X-Cache: MISS`.

### Redis no disponible o error de Redis

- La API sigue respondiendo leyendo solo del almacenamiento en memoria.
- Cabecera `X-Cache: BYPASS` para dejar trazabilidad en pruebas y en el video de evidencia.

## Evidencia de mejora (para video o informe)

1. Levantar el stack: `docker compose up --build` (o `-d` en segundo plano).
2. Comprobar `GET /health`: debe mostrar `"redis":"up"` cuando el contenedor `api` alcanzó Redis.
3. Crear un socio: `POST /clients`.
4. Llamar dos veces `GET /clients/{id}` y revisar la cabecera `X-Cache`:
   - Primera: `MISS` (lee memoria y escribe Redis con TTL).
   - Segunda: `HIT` (lee Redis).
5. Opcional: `redis-cli -h 127.0.0.1 GET gymflow:client:<uuid>` y `TTL gymflow:client:<uuid>`.

En **Windows PowerShell**, para no romper el JSON al usar `curl`, conviene `Invoke-RestMethod` / `Invoke-WebRequest` (ver [run-and-test.md](run-and-test.md)).

## Riesgos y limitaciones

- **Datos obsoletos:** si en el futuro existiera `PATCH /clients/{id}`, habría que invalidar o actualizar la clave; hoy no hay actualización de socio y el TTL acota el staleness.
- **Instancia única:** el almacenamiento sigue siendo en memoria del proceso; varias réplicas de la API no comparten el diccionario; Redis sí sería compartido pero los datos “fuente” no, por lo que este diseño es válido para demo/MVP, no para balanceo horizontal sin base de datos compartida.
- **Reinicio del contenedor API:** se pierde la memoria principal; el cache en Redis puede quedar apuntando a ids ya inexistentes hasta que expire el TTL (las lecturas seguirían devolviendo JSON hasta expiración; en un sistema real convendría invalidar al borrar o usar TTL corto).
