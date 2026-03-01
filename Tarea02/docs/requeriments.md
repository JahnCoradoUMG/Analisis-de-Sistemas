# Requirements — GymFlow

## 🔗 Backlog y tablero de trabajo
El backlog del proyecto se gestiona en **Jira (Free)**.

👉 Link al tablero:  
**https://miumg-team-f4691jef.atlassian.net/jira/software/projects/GYM/boards/34?atlOrigin=eyJpIjoiMjU5OWU0MzU0OTNmNDNkMmEzZjU4ZjUzNzAxYmIzODIiLCJwIjoiaiJ9**

El tablero utiliza los siguientes estados:
- To Do
- Paused
- In Progress
- QA
- Done

La priorización se realiza utilizando el método **MoSCoW**.

---

## 📋 Historias de Usuario

### 1. Registrar socios del gimnasio  
**Prioridad:** Must  

Como administrador o recepción,  
quiero registrar socios con sus datos básicos,  
para llevar un control centralizado de los miembros del gimnasio.

---

### 2. Crear y asignar planes de membresía  
**Prioridad:** Must  

Como administrador,  
quiero definir planes de membresía y asignarlos a socios,  
para controlar la vigencia y el acceso al gimnasio.

---

### 3. Controlar vencimiento de membresías  
**Prioridad:** Must  

Como sistema,  
quiero identificar membresías vencidas,  
para evitar accesos no autorizados y mostrar el estado real del socio.

---

### 4. Registrar pagos de membresías  
**Prioridad:** Must  

Como recepción,  
quiero registrar los pagos de las membresías,  
para mantener actualizado el estado del socio.

---

### 5. Bloquear acceso a socios con membresía vencida  
**Prioridad:** Must  

Como sistema,  
quiero bloquear el check-in de socios con membresía vencida,  
para asegurar que solo ingresen socios activos.

---

### 6. Gestionar reservas de clases o franjas horarias  
**Prioridad:** Should  

Como socio,  
quiero reservar clases o franjas horarias,  
para asegurar mi cupo en el gimnasio.

---

### 7. Gestión de usuarios y roles  
**Prioridad:** Should  

Como administrador,  
quiero gestionar usuarios y roles,  
para controlar los permisos dentro del sistema.

---

### 8. Reporte básico de asistencia y ocupación  
**Prioridad:** Could  

Como administrador,  
quiero ver reportes básicos de asistencia y ocupación,  
para tomar mejores decisiones operativas.

---

## ✅ Historias Must con criterios Given / When / Then

### Historia: Registrar socios del gimnasio

**Criterios de aceptación**

- Given que el administrador está autenticado en el sistema  
- When ingresa los datos obligatorios del socio y guarda el registro  
- Then el sistema crea el socio y lo muestra como activo  

---

### Historia: Bloquear acceso a socios con membresía vencida

**Criterios de aceptación**

- Given que la membresía del socio está vencida  
- When el socio intenta realizar check-in  
- Then el sistema bloquea el acceso y muestra un mensaje de membresía vencida  

---

## 🚀 MVP Rationale

El MVP de GymFlow se enfoca en las funcionalidades críticas para la operación diaria del gimnasio: registro de socios, gestión de membresías, control de pagos y validación de acceso.  
Estas historias **Must** permiten digitalizar el proceso principal del negocio y evitar pérdidas por accesos indebidos o desorden administrativo.  
Las funcionalidades de reservas avanzadas, roles adicionales y reportes se priorizan después del MVP, una vez validado el uso del sistema en operación real.