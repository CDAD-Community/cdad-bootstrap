# CDAD Bootstrap

> **Cuando el contexto no gobierna a la IA, la IA gobierna la solución.**

Kit de inicio oficial de **Context-Driven AI Development (CDAD)** — contexto gobernado para el desarrollo de software asistido por IA.

**El contexto es la Fuente de Verdad.**

Compatible con Claude Code, Kiro y Codex · CC BY 4.0

🌐 **Idiomas**
- 🇺🇸 [English (canónico)](README-CDAD.md)
- 🇪🇸 Español (actual)

---

## Navegación rápida

- [Flujo de uso](#flujo-de-uso)
- [Instalación manual](#instalación-manual)
- [Instalación asistida por agente](#instalación-asistida-por-agente)
- [Scaffolding obligatorio del workspace CDAD](#scaffolding-obligatorio-del-workspace-cdad)
- [El problema](#el-problema)
- [Dos archivos que siempre tocarás](#dos-archivos-que-siempre-tocarás)
- [El mapa](#el-mapa)
- [Cambiar algo](#cambiar-algo)
- [Mantener el mapa honesto](#mantener-el-mapa-honesto)
- [Principio de diseño](#principio-de-diseño)
- [Estructura](#estructura)
- [Capas de contexto](#capas-de-contexto)
- [Primeros pasos](#primeros-pasos)
- [Compatibilidad con herramientas](#compatibilidad-con-herramientas)
- [Lo que mantienes](#lo-que-mantienes)
- [Requisitos](#requisitos)
- [Evolución](#evolución)
- [Licencia](#licencia)

---

## Flujo de uso

### 1. Inicializar el contexto gobernado

**Paso 1 — Comienza con tu diseño, si ya tienes uno.**

Deja tu documento de diseño en la raíz del proyecto. Puede tener cualquier nombre y cualquier formato habitual: `.md`, `.txt`, Word, PDF o equivalente.

No existe una convención de nombre obligatoria. El documento debería estar terminado y no ser un borrador. Cuando corresponda, debe describir:

- idea y objetivo
- visión
- requisitos
- arquitectura propuesta
- stack tecnológico
- restricciones
- reglas de desarrollo

Idealmente, revisa el diseño con un LLM antes de inicializar CDAD para detectar inconsistencias.

Si todavía no tienes un documento de diseño, omite este paso. El agente puede definir el contexto contigo mediante conversación.

**Paso 2 — Indica a tu ADE/agente de programación con IA que inicialice CDAD.**

Por ejemplo:

> `clone CDAD Bootstrap and bootstrap the project`

El agente puede ser Claude Code, Kiro, Codex, Cursor, Copilot u otro ADE capaz de seguir el procedimiento de bootstrap de CDAD.

El proceso:

1. Descarga/clona CDAD Bootstrap en el proyecto.
2. Comprueba si `cdad/context/` todavía contiene placeholders de plantilla.
3. Busca en la raíz el documento de diseño/origen.
4. Si no existe ninguno, o existe más de un candidato, pregunta en lugar de adivinar.
5. Si existe uno, solicita confirmar que está terminado y no es un borrador.
6. Si no está terminado, se detiene y espera.
7. Lee el documento confirmado y lo mapea a los seis archivos de contexto gobernado.
8. Pregunta directamente aquello que el documento todavía no responde.
9. Resume el contexto resultante y solicita una segunda confirmación explícita: que los seis archivos realmente representan el diseño.
10. Solo después de esa confirmación escribe los archivos de contexto completos.
11. Conserva el documento fuente como `SOURCE-BRIEF.*` en la raíz cuando se haya proporcionado.
12. Indica que debe revisarse el resultado y ejecutarse `cdad/scripts/cdad-freeze.sh` para ratificarlo.

Antes del freeze todavía no existe nada ratificado que proteger. Por eso el agente puede escribir `cdad/context/` durante este bootstrap inicial.

El freeze es una **acción humana**. Valida que el contexto ya no contenga placeholders y crea el marcador `cdad/.frozen`, que cambia el proyecto al régimen gobernado y protege las rutas gobernadas contra escrituras directas del agente.

Consulta `.claude/skills/cdad-bootstrap/SKILL.md` para el procedimiento detallado.

A partir de ese momento, el agente lee primero el contexto gobernado antes de tomar decisiones de implementación.

La idea es simple:

> Tú y el agente definen qué quieren construir y cómo debe construirse; tú lo confirmas; CDAD convierte ese diseño acordado en contexto gobernado; después la IA desarrolla bajo ese contexto.

Para los procedimientos detallados, consulta [INSTALLATION.es.md](INSTALLATION.es.md) y [USAGE.es.md](USAGE.es.md).

### 2. Instalación manual

CDAD también puede instalarse manualmente.

El proyecto debe recibir, como mínimo, el scaffolding definido a continuación. Copia los archivos/directorios distribuidos por CDAD al proyecto, conserva las ubicaciones requeridas, combina el `.gitignore` con el existente en lugar de sobrescribirlo y completa el contexto gobernado antes de congelarlo.

Consulta [INSTALLATION.es.md](INSTALLATION.es.md#instalación-manual).

### 3. Instalación asistida por agente

Un ADE puede instalar CDAD cuando el usuario le proporciona la URL del repositorio o le solicita inicializar CDAD.

El agente debe:

1. Leer primero este README.
2. Identificar el contrato de bootstrap y la estructura obligatoria.
3. Inspeccionar el proyecto anfitrión antes de modificarlo.
4. Detectar documentos de diseño sin adivinar.
5. Informar conflictos en lugar de sobrescribir.
6. Crear el scaffolding requerido.
7. Poblar el contexto mediante el flujo de bootstrap.
8. Obtener confirmación explícita antes de ratificarlo.
9. Ejecutar el freeze cuando corresponda.
10. Informar exactamente qué creó, preservó, omitió o requiere acción humana.

Consulta [AGENTS.md](AGENTS.md) para el contrato orientado a agentes.

---

## Scaffolding obligatorio del workspace CDAD

Al realizar el bootstrap de CDAD en un proyecto, **el agente de programación con IA/ADE DEBE crear y preservar exactamente la siguiente estructura**:

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

### Reglas del scaffolding

- `AGENTS.md`, `CDAD-COMPLETION.md`, `CHANGE-REQUEST.md` e `INDEX.md` DEBEN permanecer en la raíz.
- El README de CDAD Bootstrap DEBE instalarse como `cdad/README.md`.
- Los directorios administrados por CDAD (`adr/`, `context/`, `docs/`, `proposals/`, `scripts/`) DEBEN permanecer bajo `cdad/`.
- El agente NO DEBE mover, renombrar, duplicar ni redistribuir artefactos de CDAD fuera de esta estructura.
- El agente DEBE preservar la estructura existente del proyecto anfitrión y NO DEBE sobrescribir silenciosamente un archivo existente con el mismo nombre. Los conflictos DEBEN informarse y resolverse explícitamente.
- Los archivos específicos del ADE, como `.claude/` o `.kiro/`, permanecen en sus ubicaciones requeridas y no modifican el contrato de workspace de CDAD.

Esta estructura es un **contrato de bootstrap de CDAD**, no solamente una convención documental.

---

## El problema

La IA acelera la implementación. Los humanos gobiernan el contexto y la arquitectura.

El modo de fallo no es necesariamente el código defectuoso: los agentes pueden escribir código razonable de manera individual. El problema más profundo es la **deriva arquitectónica**: una secuencia de cambios individualmente defendibles que, en conjunto, desplaza la solución hacia un lugar que nadie decidió alcanzar.

La deriva suele ser invisible a nivel de commit y solo resulta evidente a nivel de arquitectura, precisamente el nivel que menos se revisa de manera continua.

CDAD convierte la arquitectura y su contexto en activos explícitos, protegidos y legibles por máquinas. Cambiar decisiones gobernadas pasa a ser un acto deliberado y no un efecto secundario de la implementación.

---

## Dos archivos que siempre tocarás

Todo lo demás en este kit es infraestructura de soporte. Estos dos viven en la raíz del proyecto, no dentro de `cdad/`, para que sean fáciles de encontrar:

| Archivo | Qué es | Cuándo lo tocas |
| --- | --- | --- |
| **`SOURCE-BRIEF.*`** | Tu diseño original: visión, arquitectura, stack, restricciones, en tus propias palabras | Una vez, antes o durante la configuración |
| **`CHANGE-REQUEST.md`** | La puerta de entrada para solicitar un cambio | Cuando deba cambiar una decisión gobernada |

`cdad/context/stack.md` es el archivo que leerás con mayor frecuencia —el mapa de una pantalla de lo que es el sistema—, pero es un resultado y no un archivo que normalmente debas editar manualmente. Los cambios aprobados llegan mediante `CHANGE-REQUEST.md`.

---

## El mapa

`cdad/context/stack.md` responde **“¿qué es este sistema?”** sin abrir el código.

Proporciona seis vistas:

| # | Vista | Responde |
| ---: | --- | --- |
| 1 | Stack de un vistazo | ¿Sobre qué está construido y qué ADR lo bloqueó? |
| 2 | Mapa de componentes | ¿Qué se comunica con qué y mediante qué protocolo? |
| 3 | Topología de despliegue | ¿Dónde se ejecuta cada pieza? |
| 4 | Observabilidad | Si falla a las 3 a. m., ¿dónde miro? |
| 5 | Reglas de dependencias | ¿Qué módulo puede llamar a cuál? |
| 6 | Historial de cambios del mapa | Una fila por cada ADR aceptado |

El mapa usa Markdown más Mermaid, por lo que se renderiza en GitHub y en los IDE. No hay una imagen que regenerar ni una herramienta de diagramación que mantener. Además, se puede revisar como código: un pull request muestra exactamente qué cambió en la arquitectura.

Una fila de la tabla de stack sin un ADR en la columna **Locked by** es, por sí misma, un hallazgo: una decisión entró al sistema sin pasar por gobernanza.

---

## Cambiar algo

Existe una única puerta de entrada. No necesitas buscar qué archivo gobernado modificar.

```text
CHANGE-REQUEST.md  ->  cdad/proposals/  ->  cdad/adr/ + cdad/context/stack.md
      declaras intención       el agente propone       apruebas y aplicas
      siempre escribible        escribible por agente   gobernado/protegido
```

Completa el bloque de solicitud en `CHANGE-REQUEST.md` en la raíz: qué debe cambiar, por qué, qué lo desencadenó, alcance, impacto, riesgo y prioridad.

Después solicita al agente que procese la solicitud.

El agente devuelve una propuesta completa con:

- decisión actual
- cambio sugerido
- impacto
- riesgo
- alternativas
- filas exactas del mapa que cambian

Tú apruebas la propuesta. El agente prepara el ADR. El cambio aprobado se aplica mediante el proceso gobernado.

**`cdad/proposals/` es el único directorio bajo `cdad/` donde el agente puede escribir como parte del flujo de cambios gobernados.**

El trabajo rutinario de implementación no necesita entrar en este flujo. Si las tareas normales requieren solicitudes de cambio repetidamente, probablemente las restricciones están escritas de forma demasiado amplia.

---

## Mantener el mapa honesto

Cuatro mecanismos, del más débil al más fuerte:

| Mecanismo | Qué hace |
| --- | --- |
| `AGENTS.md` | Establece que un ADR que no declara su efecto sobre el mapa está incompleto |
| Skill `cdad-adr` | Exige un delta del stack antes/después y una fila de historial |
| Skill `cdad-audit` | Verifica las vistas contra manifests, grafo real de imports y reglas de alertas |
| `cdad/scripts/cdad-check-stack.sh` | **Hace fallar el build** cuando cambia un ADR y el mapa no cambia |

Los tres primeros son instrucciones o procedimientos y dependen parcialmente del comportamiento del modelo. El cuarto es enforcement determinista.

---

## Principio de diseño

Coloca cada preocupación en el plano que puede hacerla cumplir.

| Plano | Mecanismo | Garantía | Coste de contexto |
| --- | --- | --- | --- |
| Control | `permissions.deny` + hook PreToolUse | Determinista | Cero |
| Build | CI gate en `cdad/scripts/` | Determinista, al hacer merge | Cero |
| Instrucción | `AGENTS.md`, `.claude/rules/` | Probabilística | Tokens |
| Procedimental | `.claude/skills/` | Bajo demanda | Cero hasta invocarse |

**Todo lo que pueda hacerse cumplir en el plano de control no debería expresarse solamente como una instrucción.**

Por ejemplo, escribir “la IA no debe modificar los archivos de arquitectura” en el contexto consume tokens en cada sesión y solo ofrece una garantía probabilística. Bloquear la escritura en el plano de control la hace determinista sin consumir contexto.

Las instrucciones siguen siendo necesarias para el trabajo que requiere juicio: decidir si un cambio es arquitectónico, si la implementación contradice el contexto o si una abstracción está justificada.

El segundo principio se deriva de esto: **la capa determina tanto quién puede editar como cuándo se carga**. Solo las reglas y restricciones críticas deben cargarse al inicio; el conocimiento más amplio queda disponible bajo demanda.

---

## Estructura

```text
INDEX.md                        # mapa de todos los archivos — comienza aquí
AGENTS.md                       # reglas centrales portables
CHANGE-REQUEST.md               # puerta de entrada para cambios
SOURCE-BRIEF.*                  # diseño original, preservado tras el bootstrap
.gitignore                      # combinar con el del proyecto anfitrión
│
cdad/
├── proposals/                  # propuestas del agente pendientes de revisión
├── context/                    # L0 — contexto gobernado
│   ├── stack.md                # mapa de arquitectura con seis vistas
│   ├── architecture.md
│   ├── solution-vision.md
│   ├── principles.md
│   ├── constraints.md          # restricciones siempre disponibles
│   └── glossary.md
├── adr/                        # L1 — decisiones aceptadas
├── scripts/
│   └── cdad-check-stack.sh     # CI gate
└── docs/                       # referencia humana
    └── DOCS.md                # metodología, portabilidad, migración
│
.claude/
├── CLAUDE.md
├── settings.json
├── hooks/protect-l0.py
├── rules/
└── skills/
    ├── cdad-bootstrap
    ├── cdad-propose-change
    ├── cdad-adr
    └── cdad-audit
│
.kiro/steering/                 # steering/reglas de Kiro
```

### Por qué algunos archivos permanecen en la raíz

`.claude/` y `.kiro/` permanecen en la raíz porque estas herramientas descubren su configuración en ubicaciones determinadas. Moverlos dentro de `cdad/` puede hacer que dejen de cargar silenciosamente las reglas y skills previstas.

`AGENTS.md` permanece en la raíz porque Kiro y Codex lo leen por convención.

`CHANGE-REQUEST.md` y `SOURCE-BRIEF.*` permanecen en la raíz por descubribilidad humana: son los dos archivos que el Solution Designer necesita localizar rápidamente.

---

## Capas de contexto

| Capa | Contenido | Política | Carga |
| --- | --- | --- | --- |
| L0 | `cdad/context/` | Solo propuesta | Bajo demanda, excepto `constraints.md` |
| L1 | `cdad/adr/` | Propuesta con revisión | Bajo demanda |
| L2 | `cdad/docs/` | Editable con revisión | Nunca automáticamente |
| L3 | `src/`, `tests/`, pipelines, IaC | Editable | Según necesidad |

---

## Primeros pasos

1. Copia `INDEX.md`, `AGENTS.md`, `CHANGE-REQUEST.md`, `.claude/` (incluyendo `.claude/CLAUDE.md`), `cdad/` (incluyendo `cdad/docs/` y `cdad/scripts/`) y `.kiro/` si utilizas Kiro en la raíz del proyecto.
2. Combina el `.gitignore` de CDAD con el existente; no sobrescribas el archivo del proyecto.
3. Ejecuta la skill `cdad-bootstrap` (por ejemplo, “bootstrap CDAD” o “set up CDAD”) en lugar de completar `cdad/context/` manualmente.
4. Si prefieres crear el contexto manualmente, comienza con `cdad/context/stack.md`. Deja una celda vacía en vez de adivinar; un dato desconocido explícito es mejor que una decisión inventada.
5. Ajusta los globs `paths:` de `.claude/rules/` al layout del proyecto anfitrión.
6. Conecta `cdad/scripts/cdad-check-stack.sh` al CI contra la rama por defecto.
7. Ejecuta una sesión e inspecciona `/context`. Solo deberían cargarse automáticamente las reglas centrales y las restricciones esperadas.
8. Verifica el guardrail: pide al agente editar un archivo protegido, como `cdad/context/stack.md`. La escritura debe ser bloqueada por el mecanismo de enforcement correspondiente y no simplemente desaconsejada.
9. Revisa el contexto terminado y ejecuta `cdad/scripts/cdad-freeze.sh` para ratificarlo.

### Actualización al modelo de dos regímenes

Si actualizas un proyecto creado antes de que existiera el modelo de dos regímenes, ejecuta:

```bash
./cdad/scripts/cdad-freeze.sh
```

inmediatamente después de la actualización cuando `cdad/context/` ya contenga contenido real. Hasta que exista el marcador de freeze, ese contexto puede seguir siendo escribible por el agente.

Mapa completo de archivos: [`INDEX.md`](INDEX.md) · Migración: [`cdad/docs/DOCS.md#migrating-from-cdad-v1`](cdad/docs/DOCS.md#migrating-from-cdad-v1)

---

## Compatibilidad con herramientas

| Capacidad | Claude Code | Kiro | Codex |
| --- | --- | --- | --- |
| Reglas centrales portables | mediante import | nativo | nativo |
| Carga condicional | `paths:` | `inclusion: fileMatch` | `AGENTS.md` anidados |
| Procedimientos bajo demanda | Skills | `inclusion: manual` | prompt |
| Bloqueo determinista de escritura | sí | `permissions.yaml` (1.0+) | globs de configuración |
| Contexto gobernado + CI gate | sí | sí | sí |

Claude Code soporta el conjunto completo de adaptadores. `permissions.yaml` de Kiro cubre declarativamente las rutas de infraestructura incondicionales; las rutas dependientes del régimen utilizan el hook compartido y el CI gate cuando corresponde. Codex mantiene el modelo de protección de escritura, pero dispone de menos controles de carga condicional.

Detalles y notas de portabilidad: [`cdad/docs/DOCS.md`](cdad/docs/DOCS.md#portability-claude-code-kiro-codex)

### Elimina lo que no utilices

El kit incluye adaptadores para las herramientas soportadas. Mantener adaptadores que nadie lee introduce duplicación y aumenta la posibilidad de deriva. **Elimina los adaptadores no utilizados el primer día.**

| Utilizas | Mantén | Elimina |
| --- | --- | --- |
| Solo Claude Code | `AGENTS.md`, `.claude/` | `.kiro/` |
| Solo Kiro | `AGENTS.md`, `.kiro/` | `.claude/` |
| Solo Codex | `AGENTS.md` | `.claude/`, `.kiro/` |
| Más de una | todo | nada |

```bash
# Solo Claude Code
rm -rf .kiro

# Solo Kiro
rm -rf .claude

# Solo Codex
rm -rf .claude .kiro
```

**Nunca elimines `AGENTS.md`.** Contiene las reglas centrales portables. Claude Code las importa; Kiro y Codex las leen de forma nativa.

Eliminar `.claude/` elimina su capa local de enforcement. En Kiro, `permissions.yaml` proporciona protección incondicional donde es compatible; las rutas dependientes del régimen pueden depender del hook compartido y del CI gate. En Codex, utiliza `AGENTS.md` anidados cuando necesites reglas específicas por ámbito:

```text
AGENTS.md
src/AGENTS.md
infra/AGENTS.md
```

---

## Lo que mantienes

- `cdad/context/` y `cdad/adr/`: se aplican mediante el proceso gobernado y, una vez congelados, no deben ser escritos directamente por un agente.
- `CHANGE-REQUEST.md`: tu puerta de entrada cuando deba cambiar una decisión gobernada.
- `SOURCE-BRIEF.*`: se escribe una vez durante el bootstrap y se conserva como fuente original.
- `.claude/`, `.kiro/` y `cdad/scripts/`: activos de runtime/integración de CDAD que normalmente requieren pocos cambios, aparte de la configuración de rutas.

---

## Requisitos

Claude Code, Kiro o Codex.

El hook de protección necesita `python3`, presente por defecto en Linux y macOS. El CI gate necesita `git` y `bash`.

---

## Evolución

CDAD es una metodología en evolución centrada en la gobernanza del contexto en el desarrollo asistido por IA. El trabajo futuro puede extenderla a soluciones de software, nube e infraestructura, sistemas agénticos, documentación y gobernanza del conocimiento, preservando el principio central:

> **El contexto es la Fuente de Verdad.**

Relacionado: [CDAD Framework](https://github.com/mgriott/context-driven-ai-development) — metodología, whitepapers, principios y modelo de gobernanza.

---

## Licencia

Creative Commons Attribution 4.0 International (CC BY 4.0).

Eres libre de compartir, adaptar y construir sobre este trabajo, incluso comercialmente, siempre que se otorgue la atribución correspondiente.

**Atribución:** Copyright © 2026 Moisés Griott. Mantenido por **CDAD Community**.

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

---

**CDAD Community** · Context-Driven AI Development
