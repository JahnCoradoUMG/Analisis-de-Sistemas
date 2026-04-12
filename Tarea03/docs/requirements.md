# Requirements — GymFlow

## Backlog y tablero de trabajo

El backlog del proyecto se gestiona en **Jira (Free)**.

Enlace al tablero:  
https://miumg-team-f4691jef.atlassian.net/jira/software/projects/GYM/boards/34?atlOrigin=eyJpIjoiMjU5OWU0MzU0OTNmNDNkMmEzZjU4ZjUzNzAxYmIzODIiLCJwIjoiaiJ9

Estados del tablero: To Do, Paused, In Progress, QA, Done.  
Priorización: **MoSCoW**.

**Última sincronización con Jira (abril 2026):** historia de entrega Tarea 03 en [GYM-15](https://miumg-team-f4691jef.atlassian.net/browse/GYM-15); tarea de pagos MVP en [GYM-16](https://miumg-team-f4691jef.atlassian.net/browse/GYM-16). Historias MVP marcadas **Finalizada:** [GYM-2](https://miumg-team-f4691jef.atlassian.net/browse/GYM-2), [GYM-3](https://miumg-team-f4691jef.atlassian.net/browse/GYM-3), [GYM-5](https://miumg-team-f4691jef.atlassian.net/browse/GYM-5).

### Historia nueva (cache / performance)

Como equipo de desarrollo,  
quiero integrar **Redis como cache** con **Docker Compose** y TTL en consultas frecuentes de socios,  
para acercar el MVP a un entorno real, reducir lecturas repetidas y documentar la estrategia cache-aside.

**Criterios sugeridos:** `docker compose up --build` operativo; `GET /health` con `"redis":"up"`; `GET /clients/{id}` con `X-Cache` HIT/MISS; `docs/cache.md` y diagramas en `docs/architecture.md`; evidencia en video (dos peticiones + TTL en Redis). Guía de pruebas: [run-and-test.md](run-and-test.md).

---

## Historias de usuario

### 1. Registrar socios del gimnasio  
**Prioridad:** Must  

Como administrador o recepción,  
quiero registrar socios con sus datos básicos,  
para llevar un control centralizado de los miembros del gimnasio.

### 2. Crear y asignar planes de membresía  
**Prioridad:** Must  

Como administrador,  
quiero definir planes de membresía y asignarlos a socios,  
para controlar la vigencia y el acceso al gimnasio.

### 3. Controlar vencimiento de membresías  
**Prioridad:** Must  

Como sistema,  
quiero identificar membresías vencidas,  
para evitar accesos no autorizados y mostrar el estado real del socio.

### 4. Registrar pagos de membresías  
**Prioridad:** Must  

Como recepción,  
quiero registrar los pagos de las membresías,  
para mantener actualizado el estado del socio.

### 5. Bloquear acceso a socios con membresía vencida  
**Prioridad:** Must  

Como sistema,  
quiero bloquear el check-in de socios con membresía vencida,  
para asegurar que solo ingresen socios activos.

### 6. Gestionar reservas de clases o franjas horarias  
**Prioridad:** Should  

Como socio,  
quiero reservar clases o franjas horarias,  
para asegurar mi cupo en el gimnasio.

### 7. Gestión de usuarios y roles  
**Prioridad:** Should  

Como administrador,  
quiero gestionar usuarios y roles,  
para controlar los permisos dentro del sistema.

### 8. Reporte básico de asistencia y ocupación  
**Prioridad:** Could  

Como administrador,  
quiero ver reportes básicos de asistencia y ocupación,  
para tomar mejores decisiones operativas.

---

## Historias Must con criterios Given / When / Then

### Registrar socios del gimnasio

- Given que el administrador está autenticado en el sistema  
- When ingresa los datos obligatorios del socio y guarda el registro  
- Then el sistema crea el socio y lo muestra como activo  

### Bloquear acceso a socios con membresía vencida

- Given que la membresía del socio está vencida  
- When el socio intenta realizar check-in  
- Then el sistema bloquea el acceso y muestra un mensaje de membresía vencida  

---

## MVP Rationale

El MVP de GymFlow se enfoca en las funcionalidades críticas para la operación diaria del gimnasio: registro de socios, gestión de membresías, control de pagos y validación de acceso.  
Las funcionalidades de reservas avanzadas, roles adicionales y reportes se priorizan después del MVP.  
La capa **Redis** añade práctica de despliegue multi-contenedor y mejora de lecturas sin sustituir aún la base de datos persistente.
