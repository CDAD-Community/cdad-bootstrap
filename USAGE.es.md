# CDAD Bootstrap — Guía de uso

CDAD gobierna el contexto que guía el desarrollo asistido por IA.

El ciclo normal es:

```text
Contexto → Decisión → Propuesta → Aprobación → Implementación → Verificación
```

## Flujo normal

### 1. Comenzar desde el contexto gobernado

Antes de tomar una decisión de implementación, el agente debe leer el contexto gobernado aplicable.

No se busca cargar toda la documentación en cada sesión. CDAD separa deliberadamente las restricciones que deben estar siempre disponibles del contexto que solo se necesita para una tarea específica.

### 2. Trabajar en la implementación

El trabajo rutinario pertenece a la capa de implementación.

El agente puede modificar código, pruebas, pipelines e infraestructura según las reglas del proyecto.

El trabajo rutinario no requiere un `CHANGE-REQUEST.md`.

### 3. Detectar un cambio arquitectónico

Si una solicitud afecta una decisión arquitectónica, una tecnología, una regla de dependencias, la topología de despliegue, la observabilidad u otra decisión gobernada, no se debe modificar silenciosamente el mapa.

Utiliza:

```text
CHANGE-REQUEST.md
```

### 4. Proponer el cambio

El agente crea una propuesta revisable en:

```text
cdad/proposals/
```

Debe explicar:

- decisión actual
- cambio solicitado
- motivo
- disparador
- alcance
- impacto
- riesgo
- alternativas
- filas afectadas del mapa arquitectónico

### 5. Aprobar

La persona responsable revisa la propuesta.

La aprobación es una decisión de gobernanza, no un detalle de implementación.

### 6. Registrar la decisión

El cambio aprobado se convierte en un ADR bajo:

```text
cdad/adr/
```

El mapa:

```text
cdad/context/stack.md
```

debe reflejar la decisión aceptada.

### 7. Verificar

Ejecuta los mecanismos de auditoría/check correspondientes.

El CI gate:

```text
cdad/scripts/cdad-check-stack.sh
```

debe fallar cuando el mapa arquitectónico y las decisiones gobernadas dejan de estar sincronizados.

---

## El mapa arquitectónico

`cdad/context/stack.md` proporciona seis vistas:

1. stack
2. componentes
3. despliegue
4. observabilidad
5. reglas de dependencias
6. historial de cambios del mapa

Utiliza este mapa como primer punto de orientación arquitectónica.

Si una entrada del stack no tiene un ADR en `Locked by`, debe investigarse como una decisión no gobernada.

---

## Ejemplo de solicitud de cambio

La solicitud debe comunicar intención, no imponer ciegamente una implementación.

```text
¿Qué debe cambiar?
Reemplazar la tecnología actual de caché.

¿Por qué?
La tecnología actual ya no cumple las restricciones operativas acordadas.

Disparador:
Nuevos requisitos de despliegue.

Alcance:
Capa de caché y observabilidad relacionada.

Impacto:
Arquitectura, despliegue, configuración y documentación operativa.

Riesgo:
Compatibilidad de migración e invalidación de caché.

Prioridad:
Alta.
```

El agente debe convertir esto en una propuesta, no editar directamente el mapa arquitectónico.

---

## Capas de contexto

### L0 — contexto gobernado

```text
cdad/context/
```

Contiene la comprensión gobernada actual de la solución.

### L1 — decisiones arquitectónicas

```text
cdad/adr/
```

Contiene decisiones aceptadas y su justificación.

### L2 — documentación

```text
cdad/docs/
```

Contiene material de referencia humana y documentación metodológica.

### L3 — implementación

```text
src/
tests/
pipelines/
IaC/
```

Contiene la implementación gobernada por las capas superiores.

---

## Freeze y modelo de dos regímenes

CDAD distingue:

### Régimen de bootstrap

Antes del freeze:

- el contexto puede ser poblado por el procedimiento de bootstrap;
- el diseño todavía está siendo confirmado;
- el contexto aún no está ratificado.

### Régimen gobernado

Después de:

```text
cdad/.frozen
```

el contexto gobernado queda protegido.

Los cambios arquitectónicos deben seguir el flujo de solicitud/propuesta/ADR.

---

## Mantener útil el contexto

Mantén pequeño el contexto que se carga siempre.

`constraints.md` debe contener únicamente restricciones que realmente necesiten estar disponibles continuamente.

Las explicaciones detalladas, metodología, migraciones y material de referencia deben permanecer en `cdad/docs/`.

No conviertas cada instrucción en una regla permanentemente cargada.

---

## Adaptadores por herramienta

CDAD proporciona adaptadores para los ADE soportados.

- Claude Code utiliza `.claude/`.
- Kiro utiliza `.kiro/`.
- Codex utiliza `AGENTS.md` y la configuración aplicable.

Conserva solamente los adaptadores que utilizas.

**Nunca elimines `AGENTS.md`.**

---

## Checklist operativo

Antes de implementar:

- [ ] Leer el contexto gobernado aplicable.
- [ ] Determinar si la tarea es rutinaria o arquitectónica.
- [ ] Si es arquitectónica, crear/procesar una solicitud de cambio.

Durante la implementación:

- [ ] Mantener la implementación alineada con el contexto.
- [ ] No modificar silenciosamente decisiones gobernadas.
- [ ] Preservar la estructura del proyecto anfitrión.

Antes del merge:

- [ ] Confirmar que existen ADR para los cambios arquitectónicos.
- [ ] Confirmar que el mapa refleja las decisiones aceptadas.
- [ ] Ejecutar el stack check.
- [ ] Revisar el diff resultante.

---

## Principio rector

> **El contexto es la Fuente de Verdad.**

CDAD no intenta impedir que la IA modifique software. Establece un límite gobernado alrededor de las decisiones que definen qué debe ser el software.

### Destino del despliegue: repositorio Bootstrap vs. proyecto anfitrión

Los archivos de documentación de este repositorio Bootstrap permanecen en la **raíz del repositorio Bootstrap**.

Cuando un agente despliega CDAD dentro de un proyecto anfitrión, DEBE reorganizar el workspace instalado para que el contenido operativo y propio de CDAD quede bajo `cdad/`:

```text
/
├── AGENTS.md
├── CDAD-COMPLETION.md
├── CHANGE-REQUEST.md
├── INDEX.md
└── cdad/
    ├── README.md
    ├── adr/
    ├── context/
    ├── docs/
    ├── proposals/
    └── scripts/
```

Para Claude Code y/o Kiro, `.claude/` y `.kiro/` permanecen en la raíz del proyecto anfitrión.

No copies `README-CDAD.md`, `INSTALLATION.md` ni `USAGE.md` del repositorio Bootstrap a la raíz del proyecto anfitrión. El README orientado al proyecto instalado debe quedar en `cdad/README.md`.

El agente debe preservar los archivos existentes del proyecto, no sobrescribir conflictos silenciosamente y no ejecutar automáticamente el freeze. La revisión y confirmación humana deben ocurrir antes del freeze.
