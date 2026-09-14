# CDAD Bootstrap

> **Cuando el contexto no gobierna a la IA, la IA gobierna la solución.**

Kit de inicio oficial de **Context-Driven AI Development (CDAD)** — contexto gobernado para el desarrollo de software asistido por IA.

**El contexto es la Fuente de Verdad.**

Compatible con Claude Code, Kiro, Codex y GitHub Copilot · CC BY 4.0

🌐 **Idiomas**
- 🇺🇸 [English (canónico)](README-CDAD.md)
- 🇪🇸 Español (actual)

---

## Navegación rápida

- [Flujo de uso](#flujo-de-uso)
- [Adaptadores de ADE](#adaptadores-de-ade)
- [Instalación manual](#instalación-manual)
- [Instalación asistida por agente](#instalación-asistida-por-agente)
- [Scaffolding obligatorio del workspace CDAD](#scaffolding-obligatorio-del-workspace-cdad)
- [Higiene del workspace](#higiene-del-workspace)
- [El problema](#el-problema)
- [Los dos archivos que siempre tocarás](#los-dos-archivos-que-siempre-tocarás)
- [El mapa](#el-mapa)
- [Cambiar algo](#cambiar-algo)
- [Backlog](#backlog)
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

1. Descarga/clona CDAD Bootstrap en el proyecto — la distribución fuente es un catálogo de todos los adaptadores, no algo que se instale completo.
2. Detecta qué ADE está ejecutando realmente el bootstrap y resuelve el único adaptador que le corresponde. Si parece haber más de un ADE posible y no puede establecer con confianza cuál lo está ejecutando, pregunta en lugar de adivinar — ver [Adaptadores de ADE](#adaptadores-de-ade).
3. Instala el núcleo portable de CDAD más únicamente el adaptador resuelto, excluyendo explícitamente los demás.
4. Comprueba si `cdad/context/` todavía contiene placeholders de plantilla.
5. Busca en la raíz el documento de diseño/origen.
6. Si no existe ninguno, o existe más de un candidato, pregunta en lugar de adivinar.
7. Si existe uno, solicita confirmar que está terminado y no es un borrador.
8. Si no está terminado, se detiene y espera.
9. Lee el documento confirmado y lo mapea a los seis archivos de contexto gobernado.
10. Pregunta directamente aquello que el documento todavía no responde.
11. Resume el contexto resultante y solicita una segunda confirmación explícita: que los seis archivos realmente representan el diseño.
12. Solo después de esa confirmación escribe los archivos de contexto completos.
13. Conserva el documento fuente como `SOURCE-BRIEF.*` en la raíz cuando se haya proporcionado.
14. Indica que debe revisarse el resultado y ejecutarse `cdad/scripts/cdad-freeze.sh` para ratificarlo.

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

## Adaptadores de ADE

CDAD distribuye un núcleo portable más un adaptador por cada ADE soportado.
Un proyecto destino recibe el núcleo portable más exactamente el adaptador
que corresponde al ADE que ejecuta el bootstrap — nunca el catálogo
completo, nunca más de un adaptador nativo. La distribución fuente de CDAD
Bootstrap contiene todos los adaptadores porque es un catálogo; instalarlos
todos en un proyecto no es el flujo previsto.

**Núcleo portable:** `AGENTS.md`, `README-CDAD.md`, `README-CDAD.es.md`, `SOURCE-BRIEF.*` (si existió documento fuente) en la raíz del proyecto, más `cdad/` en sí — que contiene `INDEX.md`, `CHANGE-REQUEST.md`, `CDAD-COMPLETION.md`, `backlog.md`, `context/`, `adr/`, `proposals/`, `docs/`, `scripts/`.

| ADE anfitrión | Adaptador | `.claude/` | `.kiro/` | `AGENTS.md` | `.github/copilot-instructions.md` |
| --- | --- | :---: | :---: | :---: | :---: |
| Claude Code | Claude | SÍ | NO | SÍ | NO |
| Kiro | Kiro | NO | SÍ | SÍ | NO |
| Codex | Portable/AGENTS | NO | NO | SÍ | NO |
| GitHub Copilot | Copilot | NO | NO | SÍ | SÍ |
| Otro ADE soportado | Solo el adaptador explícito | solo si está mapeado | solo si está mapeado | según soporte | según soporte |
| ADE desconocido | Portable/desconocido | NO | NO | no adivinar | NO |

La decisión del adaptador se basa en el ADE que realmente ejecuta el
bootstrap, nunca en el modelo subyacente. Un modelo Claude no es Claude
Code; un modelo GPT no es Codex; la API de Anthropic u OpenAI por sí sola
tampoco lo es.

Si el proyecto destino ya muestra archivos de más de un ADE (por ejemplo,
una configuración parcial previa dejó tanto `.claude/` como `.kiro/`), el
agente no elige uno solo porque sus archivos existan — determina cuál ADE
está ejecutando este bootstrap, o pregunta:

> Se detectaron múltiples entornos de ADE posibles.
>
> CDAD requiere seleccionar el ADE que está ejecutando este bootstrap.
>
> Detectados:
> - Claude Code
> - Kiro
>
> Por favor confirma qué ADE está ejecutando actualmente el bootstrap de CDAD.

Para un ADE sin adaptador nativo, CDAD instala solo el núcleo portable e
informa claramente que no existe un adaptador nativo — nunca inventa uno.

Volver a ejecutar el bootstrap nunca reintroduce un adaptador que una
ejecución previa excluyó explícitamente, ni instala un segundo adaptador
nativo junto al primero.

Algoritmo completo: `.claude/skills/cdad-bootstrap/SKILL.md` (paso 0). Valida
un proyecto instalado contra esta matriz con
`cdad/scripts/cdad-check-adapter.sh <claude|kiro|codex|copilot|unknown>`.

---

## Scaffolding obligatorio del workspace CDAD

Al realizar el bootstrap de CDAD en un proyecto, **el agente de programación con IA/ADE DEBE crear y preservar exactamente la siguiente estructura**:

```text
/
├── AGENTS.md
├── README-CDAD.md
├── README-CDAD.es.md
├── SOURCE-BRIEF.*                # si existió documento fuente
└── cdad/
    ├── README.md
    ├── INDEX.md
    ├── CHANGE-REQUEST.md
    ├── CDAD-COMPLETION.md
    ├── backlog.md
    ├── adr/
    ├── context/
    ├── docs/
    ├── proposals/
    └── scripts/
```

### Reglas del scaffolding

- `AGENTS.md`, `README-CDAD.md`, `README-CDAD.es.md` y `SOURCE-BRIEF.*` (cuando existe) DEBEN permanecer en la raíz — nada más de lo que posee CDAD lo hace.
- `INDEX.md`, `CHANGE-REQUEST.md`, `CDAD-COMPLETION.md` y `backlog.md` DEBEN generarse directamente bajo `cdad/` — nunca escribirse en la raíz para moverlos después.
- El README de CDAD Bootstrap DEBE instalarse como `cdad/README.md`.
- Los directorios administrados por CDAD (`adr/`, `context/`, `docs/`, `proposals/`, `scripts/`) DEBEN permanecer bajo `cdad/`.
- El agente NO DEBE mover, renombrar, duplicar ni redistribuir artefactos de CDAD fuera de esta estructura.
- El agente DEBE preservar la estructura existente del proyecto anfitrión y NO DEBE sobrescribir silenciosamente un archivo existente con el mismo nombre. Los conflictos DEBEN informarse y resolverse explícitamente.
- Los archivos específicos del ADE — `.claude/`, `.kiro/` o `.github/copilot-instructions.md` — permanecen en sus ubicaciones requeridas y no modifican el contrato de workspace de CDAD. Solo se instala el adaptador correspondiente al ADE que ejecuta el bootstrap; ver [Adaptadores de ADE](#adaptadores-de-ade).

Esta estructura es un **contrato de bootstrap de CDAD**, no solamente una convención documental.

---

## Higiene del workspace

**CDAD mantiene sus artefactos de desarrollo gobernado dentro de `cdad/`.
Solo permanecen en la raíz los archivos necesarios para el
descubrimiento/integración del ADE y los puntos de entrada humanos de
CDAD.**

La raíz del proyecto pertenece al proyecto del usuario; `cdad/` pertenece a
la gobernanza de CDAD. Antes de este principio, los propios archivos de
gobernanza de CDAD (`INDEX.md`, `CHANGE-REQUEST.md`, `CDAD-COMPLETION.md`,
`backlog.md`) se sentaban directamente en la raíz del proyecto junto a la
aplicación real del usuario — ruido visual y cognitivo tanto para el
desarrollador como para cualquier agente que escanee la raíz para entender
qué es el proyecto.

La prueba: *si soy un desarrollador usando CDAD, ¿la raíz del proyecto se
ve como mi proyecto, mientras `cdad/` contiene claramente la maquinaria de
gobernanza de CDAD?* La raíz debe contener solamente:

- Archivos de descubrimiento/integración del ADE que genuinamente requieren ubicación en la raíz/nativa (`.claude/`, `.kiro/`, `.github/copilot-instructions.md`, o `AGENTS.md` en sí).
- Los puntos de entrada humanos de CDAD (`README-CDAD.md`, `README-CDAD.es.md`, `SOURCE-BRIEF.*`).
- Los propios archivos del proyecto del usuario.

Esto es un cambio estructural, no un paso de limpieza: el proceso de
bootstrap genera estos artefactos directamente bajo `cdad/` — nunca los
escribe en la raíz pidiéndote que ordenes después, como versiones
anteriores pedían borrar adaptadores de ADE no usados. Ver *Adaptadores de
ADE* arriba para el mismo principio de generación selectiva aplicado a las
integraciones de herramientas.

---

## El problema

La IA acelera la implementación. Los humanos gobiernan el contexto y la arquitectura.

El modo de fallo no es necesariamente el código defectuoso: los agentes pueden escribir código razonable de manera individual. El problema más profundo es la **deriva arquitectónica**: una secuencia de cambios individualmente defendibles que, en conjunto, desplaza la solución hacia un lugar que nadie decidió alcanzar.

La deriva suele ser invisible a nivel de commit y solo resulta evidente a nivel de arquitectura, precisamente el nivel que menos se revisa de manera continua.

CDAD convierte la arquitectura y su contexto en activos explícitos, protegidos y legibles por máquinas. Cambiar decisiones gobernadas pasa a ser un acto deliberado y no un efecto secundario de la implementación.

---

## Los dos archivos que siempre tocarás

| Archivo | Qué es | Cuándo lo tocas |
| --- | --- | --- |
| **`SOURCE-BRIEF.*`** (raíz del proyecto) | Tu diseño original: visión, arquitectura, stack, restricciones, en tus propias palabras | Una vez, antes o durante la configuración |
| **`cdad/CHANGE-REQUEST.md`** | La puerta de entrada para solicitar un cambio | Cuando deba cambiar una decisión gobernada o la línea de desarrollo |

`SOURCE-BRIEF.*` permanece en la raíz del proyecto — el único artefacto de CDAD que es puramente tuyo para encontrar rápido, nunca maquinaria de gobernanza. `CHANGE-REQUEST.md` vive bajo `cdad/` junto con lo que gobierna, pero sigue siendo el único punto de entrada que usás constantemente; nunca se vuelve más difícil de alcanzar solo porque se movió.

`cdad/context/stack.md` es el archivo que leerás con mayor frecuencia —el mapa de una pantalla de lo que es el sistema—, pero es un resultado y no un archivo que normalmente debas editar manualmente. Los cambios aprobados llegan mediante `cdad/CHANGE-REQUEST.md`.

---

## El mapa

`cdad/context/stack.md` responde **“¿qué es este sistema?”** sin abrir el código.

Proporciona siete vistas:

| # | Vista | Responde |
| ---: | --- | --- |
| 1 | Stack de un vistazo | ¿Sobre qué está construido y qué ADR lo bloqueó? |
| 2 | Mapa de componentes | ¿Qué se comunica con qué y mediante qué protocolo? |
| 3 | Topología de despliegue | ¿Dónde se ejecuta cada pieza? |
| 4 | Observabilidad | Si falla a las 3 a. m., ¿dónde miro? |
| 5 | Reglas de dependencias | ¿Qué módulo puede llamar a cuál? |
| 6 | Historial de cambios del mapa | Una fila por cada ADR aceptado |
| 7 | Señales de drift | ¿Qué rutas fuera de `cdad/` cargan peso arquitectónico, y qué protegen? |

El mapa usa Markdown más Mermaid, por lo que se renderiza en GitHub y en los IDE. No hay una imagen que regenerar ni una herramienta de diagramación que mantener. Además, se puede revisar como código: un pull request muestra exactamente qué cambió en la arquitectura.

Una fila de la tabla de stack sin un ADR en la columna **Locked by** es, por sí misma, un hallazgo: una decisión entró al sistema sin pasar por gobernanza.

---

## Cambiar algo

Existe una única puerta de entrada. No necesitas buscar qué archivo gobernado modificar.

```text
cdad/CHANGE-REQUEST.md  ->  cdad/proposals/  ->  cdad/adr/ + cdad/context/stack.md
      declaras intención           el agente propone        apruebas y aplicas
      siempre escribible           escribible por agente    gobernado/protegido
```

Completa el bloque de solicitud en `cdad/CHANGE-REQUEST.md`: qué debe cambiar, por qué, qué lo desencadenó, alcance, impacto, riesgo y prioridad.

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

## Backlog

`cdad/backlog.md` es la línea de desarrollo: Epics, Stories, y el trabajo
que actualmente se espera construir. Responde "qué existe, qué sigue, qué
está bloqueado" — es un artefacto de planificación, no arquitectura, y
nunca una segunda fuente de verdad junto a `cdad/context/`.

```text
Contexto Gobernado / L0  ->  ADR  ->  cdad/backlog.md  ->  Implementación
```

Una Story que contradice el contexto gobernado o un ADR aceptado es un
hallazgo, no una resolución — nunca sobrescribe silenciosamente la
arquitectura.

**Gobernado igual que todo lo demás, con una excepción rutinaria:**

| Cambio | Vía |
| --- | --- |
| Epic o Story nueva/eliminada, o cambio material de alcance/criterios de aceptación | `cdad/CHANGE-REQUEST.md` → `cdad/proposals/` → decisión del Solution Designer |
| Actualización de estado de Story, *Current Focus*, *Next Work*, *Blocked* durante trabajo ya aprobado | Edición directa — implementación rutinaria, no una decisión gobernada |

Antes de trabajar en desarrollo, el agente establece la Epic/Story
aplicable desde `cdad/backlog.md`. Si hay Epics/Stories definidas en otro lugar
pero ausentes del backlog, esa brecha se reconcilia mediante el proceso de
cambio normal — el agente no las ignora silenciosamente, ni reescribe el
backlog para que coincida sin más. Si no hay ninguna definida, el agente lo
dice explícitamente en vez de inventar requisitos de negocio.

`cdad/scripts/cdad-check-backlog.sh` verifica determinísticamente la
integridad estructural — IDs únicos de Epic/Story, valores de estado
válidos. Si una Epic/Story es real, vigente y realmente refleja el trabajo
en curso es un juicio que hace la skill `cdad-audit`, no algo que un script
pueda verificar.

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
AGENTS.md                       # reglas centrales portables
README-CDAD.md                  # este archivo — configuración, compatibilidad
README-CDAD.es.md               # espejo en español
SOURCE-BRIEF.*                  # diseño original, preservado tras el bootstrap
.gitignore                      # combinar con el del proyecto anfitrión
│
cdad/                           # gobernanza CDAD — todo lo de abajo se genera aquí, no en la raíz
├── README.md                   # README operativo orientado al proyecto
├── INDEX.md                    # mapa de todos los archivos — comienza aquí
├── CHANGE-REQUEST.md           # puerta de entrada para cambios
├── CDAD-COMPLETION.md          # registro durable de finalización del bootstrap
├── backlog.md                  # línea de desarrollo — Epics, Stories, foco actual
├── proposals/                  # propuestas del agente pendientes de revisión
├── context/                    # L0 — contexto gobernado
│   ├── stack.md                # mapa de arquitectura con siete vistas
│   ├── architecture.md
│   ├── solution-vision.md
│   ├── principles.md
│   ├── constraints.md          # restricciones siempre disponibles
│   └── glossary.md
├── adr/                        # L1 — decisiones aceptadas
├── scripts/
│   ├── cdad-check-stack.sh     # CI gate
│   ├── cdad-check-adapter.sh   # valida que el adaptador instalado coincide con la matriz
│   └── cdad-check-backlog.sh   # valida la integridad estructural de backlog.md
└── docs/                       # referencia humana
    └── DOCS.md                # metodología, portabilidad, migración
│
# abajo: el catálogo de adaptadores que distribuye esta fuente — un proyecto
# instalado recibe exactamente UNO, resuelto al momento del bootstrap
│
.claude/                        # adaptador de Claude Code
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
.kiro/steering/                 # adaptador de Kiro
│
.github/copilot-instructions.md # adaptador de GitHub Copilot
```

### Por qué algunos archivos permanecen en la raíz

`.claude/`, `.kiro/` y `.github/copilot-instructions.md` permanecen en la raíz porque estas herramientas descubren su configuración en ubicaciones determinadas. Moverlos dentro de `cdad/` puede hacer que dejen de cargar silenciosamente las reglas y skills previstas. Solo se instala el que corresponde a tu adaptador resuelto — ver [Adaptadores de ADE](#adaptadores-de-ade).

`AGENTS.md` permanece en la raíz porque Kiro, Codex y Copilot lo leen por convención.

`README-CDAD.md`/`.es.md` permanecen en la raíz porque son los puntos de entrada humanos — lo primero que cualquiera que abra el proyecto debería poder encontrar, no algo enterrado bajo `cdad/`.

`SOURCE-BRIEF.*` permanece en la raíz por la misma razón: es el diseño original del Solution Designer, en sus propias palabras, y debe ser tan descubrible como los READMEs. Todo lo demás que posee CDAD — incluyendo `CHANGE-REQUEST.md`, ahora que tiene uno — vive bajo `cdad/`; ver [Higiene del workspace](#higiene-del-workspace).

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

1. Copia el núcleo portable — `AGENTS.md`, `README-CDAD.md`, `README-CDAD.es.md`, y `cdad/` completo (incluyendo `cdad/docs/`, `cdad/scripts/`, y `INDEX.md`/`CHANGE-REQUEST.md`/`CDAD-COMPLETION.md`/`backlog.md` ya dentro de él) — en la raíz del proyecto, más únicamente el adaptador correspondiente a tu ADE: `.claude/` (incluyendo `.claude/CLAUDE.md`) para Claude Code, `.kiro/` para Kiro, `.github/copilot-instructions.md` para GitHub Copilot, o nada adicional para Codex. Ver [Adaptadores de ADE](#adaptadores-de-ade); no copies los demás adaptadores "por las dudas".
2. Combina el `.gitignore` de CDAD con el existente; no sobrescribas el archivo del proyecto.
3. Ejecuta la skill `cdad-bootstrap` (por ejemplo, “bootstrap CDAD” o “set up CDAD”) en lugar de completar `cdad/context/` manualmente — realiza el paso 1 anterior por vos, de forma determinista.
4. Si prefieres crear el contexto manualmente, comienza con `cdad/context/stack.md`. Deja una celda vacía en vez de adivinar; un dato desconocido explícito es mejor que una decisión inventada.
5. Ajusta los globs `paths:` de `.claude/rules/` al layout del proyecto anfitrión (solo Claude Code).
6. Conecta `cdad/scripts/cdad-check-stack.sh` y `cdad/scripts/cdad-check-backlog.sh` al CI contra la rama por defecto.
7. Ejecuta una sesión e inspecciona `/context`. Solo deberían cargarse automáticamente las reglas centrales y las restricciones esperadas.
8. Verifica el guardrail: pide al agente editar un archivo protegido, como `cdad/context/stack.md`. La escritura debe ser bloqueada por el mecanismo de enforcement correspondiente y no simplemente desaconsejada.
9. Verifica el adaptador: `cdad/scripts/cdad-check-adapter.sh <claude|kiro|codex|copilot>` confirma que solo están presentes los archivos del adaptador resuelto.
10. Revisa el contexto terminado y ejecuta `cdad/scripts/cdad-freeze.sh` para ratificarlo.

### Actualización al modelo de dos regímenes

Si actualizas un proyecto creado antes de que existiera el modelo de dos regímenes, ejecuta:

```bash
./cdad/scripts/cdad-freeze.sh
```

inmediatamente después de la actualización cuando `cdad/context/` ya contenga contenido real. Hasta que exista el marcador de freeze, ese contexto puede seguir siendo escribible por el agente.

Mapa completo de archivos: [`cdad/INDEX.md`](cdad/INDEX.md) · Migración: [`cdad/docs/DOCS.md#migrating-from-cdad-v1`](cdad/docs/DOCS.md#migrating-from-cdad-v1)

---

## Compatibilidad con herramientas

| Capacidad | Claude Code | Kiro | Codex | GitHub Copilot |
| --- | --- | --- | --- | --- |
| Reglas centrales portables | mediante import | nativo | nativo | nativo (`AGENTS.md`) + puntero `.github/copilot-instructions.md` |
| Carga condicional | `paths:` | `inclusion: fileMatch` | `AGENTS.md` anidados | ninguna — solo a nivel repo |
| Procedimientos bajo demanda | Skills | `inclusion: manual` | prompt | prompt |
| Bloqueo determinista de escritura | sí | `permissions.yaml` (1.0+) | globs de configuración | no — solo CI gate |
| Contexto gobernado + CI gate | sí | sí | sí | sí |

Claude Code soporta el conjunto completo de adaptadores. `permissions.yaml` de Kiro cubre declarativamente las rutas de infraestructura incondicionales; las rutas dependientes del régimen utilizan el hook compartido y el CI gate cuando corresponde. Codex mantiene el modelo de protección de escritura, pero dispone de menos controles de carga condicional. GitHub Copilot lee instrucciones a nivel de repositorio desde `.github/copilot-instructions.md` e instrucciones de agente desde `AGENTS.md`, según la documentación actual de GitHub; no tiene carga condicional por rutas ni bloqueo determinista de escritura más allá del CI gate — el adaptador de Copilot es deliberadamente delgado y no reclama capacidades que CDAD no haya implementado realmente para él.

Detalles y notas de portabilidad: [`cdad/docs/DOCS.md`](cdad/docs/DOCS.md#portability-claude-code-kiro-codex-copilot)

### Cambiar de ADE más adelante

El bootstrap ya instala solo el adaptador correspondiente a tu ADE — ver
[Adaptadores de ADE](#adaptadores-de-ade). No hay nada que podar el primer
día. Si el proyecto cambia de ADE más adelante (no simplemente suma un
segundo ADE de uso ocasional), elimina el adaptador anterior y vuelve a
ejecutar el bootstrap para que el nuevo se instale siguiendo las mismas
reglas que una instalación desde cero:

```bash
# Migrar a Claude Code
rm -rf .kiro
# luego el bootstrap resuelve e instala .claude/

# Migrar a Kiro
rm -rf .claude
# luego el bootstrap resuelve e instala .kiro/

# Migrar a Codex o Copilot
rm -rf .claude .kiro
# Copilot también necesita .github/copilot-instructions.md; el bootstrap lo instala
```

**Nunca elimines `AGENTS.md`.** Contiene las reglas centrales portables. Claude Code las importa; Kiro, Codex y Copilot las leen de forma nativa.

Eliminar `.claude/` elimina su capa local de enforcement. En Kiro, `permissions.yaml` proporciona protección incondicional donde es compatible; las rutas dependientes del régimen pueden depender del hook compartido y del CI gate. En Codex o Copilot, utiliza `AGENTS.md` anidados cuando necesites reglas específicas por ámbito:

```text
AGENTS.md
src/AGENTS.md
infra/AGENTS.md
```

---

## Lo que mantienes

- `cdad/context/` y `cdad/adr/`: se aplican mediante el proceso gobernado y, una vez congelados, no deben ser escritos directamente por un agente.
- `cdad/backlog.md`: las Epics/Stories cambian vía `cdad/CHANGE-REQUEST.md` como una decisión arquitectónica; las actualizaciones de estado y foco durante implementación rutinaria son ediciones directas.
- `cdad/CHANGE-REQUEST.md`: tu puerta de entrada cuando deba cambiar una decisión gobernada o la línea de desarrollo comprometida.
- `SOURCE-BRIEF.*`: se escribe una vez durante el bootstrap y se conserva como fuente original, en la raíz del proyecto.
- Tu adaptador resuelto (`.claude/`, `.kiro/` o `.github/copilot-instructions.md`) y `cdad/scripts/`: activos de runtime/integración de CDAD que normalmente requieren pocos cambios, aparte de la configuración de rutas.

---

## Requisitos

Claude Code, Kiro, Codex o GitHub Copilot.

El hook de protección (Claude Code) necesita `python3`, presente por defecto en Linux y macOS. El CI gate necesita `git` y `bash`.

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
