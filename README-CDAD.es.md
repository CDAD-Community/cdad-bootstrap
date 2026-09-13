**# CDAD Bootstrap**

\> **\*\*Cuando el contexto no gobierna a la IA, la IA gobierna la solución.\*\***

El kit de inicio oficial para **\*\*Context-Driven AI Development (CDAD)\*\*** — contexto gobernado para el desarrollo de software asistido por IA.

**\*\*El contexto es la Fuente de Verdad.\*\***

Compatible con Claude Code, Kiro y Codex · CC BY 4.0

🌐 **Idiomas / Languages**

- 🇺🇸 [English](README.md)
- 🇪🇸 Español (actual)

\---

**## Navegación rápida**

\- [Flujo de uso]\(#flujo-de-uso)

\- [Scaffolding obligatorio del workspace CDAD]\(#scaffolding-obligatorio-del-workspace-cdad)

\- [El problema]\(#el-problema)

\- [El mapa]\(#el-mapa)

\- [Cambiar algo]\(#cambiar-algo)

\- [Mantener el mapa honesto]\(#mantener-el-mapa-honesto)

\- [Principio de diseño]\(#principio-de-diseño)

\- [Estructura]\(#estructura)

\- [Capas de contexto]\(#capas-de-contexto)

\- [Primeros pasos]\(#primeros-pasos)

\- [Compatibilidad con herramientas]\(#compatibilidad-con-herramientas)

\- [Lo que mantienes]\(#lo-que-mantienes)

\- [Requisitos]\(#requisitos)

\- [Evolución]\(#evolución)

\- [Licencia]\(#licencia)

\---

**## Flujo de uso**

**### 1. Inicializar el contexto gobernado**

**\*\*Paso 1: deja tu documento de diseño en la raíz del proyecto, si tienes uno.\*\*** Cualquier nombre y cualquier formato habitual — \`.md\`, \`.txt\`, Word, PDF. No hay ninguna convención que seguir; simplemente deja el archivo allí. Debe estar terminado, no ser un borrador: idea, objetivo, visión, requisitos, arquitectura propuesta, stack tecnológico, restricciones y reglas de desarrollo — idealmente revisado y discutido previamente con un LLM para detectar inconsistencias. ¿Todavía no tienes uno? Omite este paso; el agente definirá el contexto contigo mediante conversación.

**\*\*Paso 2: dile a tu agente del IDE que descargue CDAD Bootstrap y lo configure\*\*** (say *\*"clone CDAD Bootstrap and bootstrap the project"\** — el agente ejecuta la \`cdad-bootstrap\` skill). El agente (Kiro, Codex, Cursor, Claude Code, or whichever ADE you use):

→ clona/descarga CDAD Bootstrap en el proyecto → comprueba si \`cdad/context/\` todavía contiene placeholders de plantilla → comprueba si en la raíz existe el documento que dejaste en el paso 1; si no existe ninguno o existe más de uno, pregunta en lugar de adivinar → si existe un documento, te pide confirmar que está terminado —no es un borrador— antes de utilizarlo; si indicas que no lo está, se detiene y espera a que lo termines en lugar de intentar completar los vacíos mediante preguntas → una vez confirmado (or si there was nunca a document to confirm), lo lee y lo transforma en los seis archivos de contexto → te pregunta directamente aquello que todavía no responde — cuanto menos material inicial exista, más preguntas hará, y eso es lo esperado → resume el resultado y espera tu confirmación explícita — una segunda confirmación, separada de la anterior: la anterior era sobre si tu diseño estaba definido; esta es sobre si los seis archivos realmente lo representan → solo entonces escribe directamente los archivos de contexto completos — además de tu documento fuente, renombrado como \`SOURCE-BRIEF.\*\`, si you had one, de forma permanente en la raíz del proyecto, no escondido en otro directorio — y te indica que lo revises, y luego ejecutes \`cdad/scripts/cdad-freeze.sh\` para ratsiicarlo

Antes de congelar el proyecto, todavía no existe nada ratsiicado que proteger, so el agente puede escribir \`cdad/context/\` directamente como parte de este bootstrap inicial. El freeze es una acción humana: valida que el contexto ya no contenga texto de plantilla, y luego crea el \`cdad/.frozen\` marcador que cambia el proyecto al régimen gobernado, donde esas rutas vuelven a ser de solo lectura para el agente. Consulta \`.claude/skills/cdad-bootstrap/SKILL.md\` para conocer el procedimiento completo.

A partir de ese momento, el agente lee primero ese contexto gobernado antes de tomar cualquier decisión de implementación.

La idea es simple: tú y el agente definen qué quieren construir y cómo debe ser, tú lo confirmas; luego el contexto gobernado de CDAD se construye a partir de ello; finalmente, la IA desarrolla bajo ese contexto.

\---

**## Scaffolding obligatorio del workspace CDAD**

Al realizar el bootstrap de CDAD en un proyecto, **\*\*el agente de programación con IA/ADE DEBE crear y preservar exactamente la siguiente estructura de workspace\*\***:

\`\`\`text

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

\`\`\`

**\*\*Reglas del scaffolding:\*\***

\- \`AGENTS.md\`, \`CDAD-COMPLETION.md\`, \`CHANGE-REQUEST.md\`, and \`INDEX.md\` DEBEN permanecer en la raíz del proyecto.

\- The CDAD bootstrap README DEBE instalarse como \`cdad/README.md\`.

\- Los directorios administrados por CDAD (\`adr/\`, \`context/\`, \`docs/\`, \`proposals/\`, \`scripts/\`) DEBEN permanecer bajo \`cdad/\`.

\- El agente NO DEBE mover, renombrar, duplicar ni redistribuir artefactos de CDAD fuera de esta estructura.

\- El agente DEBE preservar la estructura de código existente del proyecto anfitrión y no debe sobrescribir silenciosamente un archivo existente con el mismo nombre; los conflictos DEBEN informarse y resolverse explícitamente.

\- Los archivos específicos del ADE requeridos por la herramienta anfitriona (for example \`.claude/\` or \`.kiro/\`) son archivos de integración de la herramienta y permanecen en las ubicaciones requeridas; no modsiican la estructura del workspace CDAD anterior.

This structure is a **\*\*CDAD bootstrap contract\*\***, not merely a documentation convention.

**## El problema**

La IA acelera la implementación. Los humanos gobiernan el contexto y la arquitectura.

El modo de fallo no es el código defectuoso: los agentes escriben código razonable. It is **\*\*architectural drsit\*\***: una secuencia de cambios individualmente defendibles que, en conjunto, desplazan la solución hacia un lugar que nadie decidió alcanzar.

La deriva es invisible a nivel de commit y solo resulta visible a nivel de arquitectura, precisamente el nivel que nadie revisa.

CDAD convierte la arquitectura en un activo explícito, protegido y legible por máquinas, y hace que cambiarla sea un acto deliberado en lugar de un efecto secundario.

\---

**## Dos archivos que siempre tocarás**

Todo lo demás en este kit es infraestructura. Estos dos viven en la raíz del proyecto, no dentro de \`cdad/\` — nunca deberías tener que buscarlos.

\| File | Qué es | Cuándo lo tocas |

\| --- | --- | --- |

\| **\*\*\`SOURCE-BRIEF.\*\`\*\*** | Tu diseño original —visión, arquitectura, stack y restricciones, en tus propias palabras | Una vez, antes o durante la configuración |

\| **\*\*\`CHANGE-REQUEST.md\`\*\*** | La puerta de entrada. Aquí solicitas cualquier cambio | Cada vez que una decisión deba cambiar |

\`cdad/context/stack.md\` is the file you'll *\*read\** the most — el mapa de una sola pantalla que muestra qué es este sistema — pero es una salida, no algo que debas escribir manualmente. Los cambios aprobados llegan a él mediante \`CHANGE-REQUEST.md\`, nunca directamente.

\---

**## El mapa**

\`cdad/context/stack.md\` responde "¿qué es este sistema?" sin abrir el código. Six views:

\| # | Vista | Responde |

\| ---: | --- | --- |

\| 1 | Stack de un vistazo | sobre qué está construido y qué ADR lo dejó fijado |

\| 2 | Mapa de componentes | qué componente se comunica con cuál y mediante qué protocolo |

\| 3 | Topología de despliegue | dónde se ejecuta cada pieza |

\| 4 | Observabilidad | si falla a las 3 a. m., qué debo revisar |

\| 5 | Reglas de dependencias | qué módulo puede llamar a cuál |

\| 6 | Registro de cambios del mapa | una fila por cada ADR aceptado |

Markdown más Mermaid, para que se renderice en GitHub y en cualquier IDE — sin imágenes que regenerar ni herramientas de diagramación que mantener licenciadas, and **\*\*funciona con dsifs como el código\*\***. En un pull request puedes ver exactamente qué cambió en la arquitectura.

Una fila de la tabla de stack sin un ADR en su columna "Locked by" es en sí misma un hallazgo: una decisión que entró al sistema sin pasar por la gobernanza.

\---

**## Cambiar algo**

Un único punto de entrada. Nunca tienes que buscar el archivo correcto.

\`\`\`

CHANGE-REQUEST.md  ->  cdad/proposals/  ->  cdad/adr/ + cdad/context/stack.md

     tú declaras la intención      el agente redacta el borrador           tú apruebas y aplicas

     siempre escribible       escribible por el agente         bloqueado para los agentes

\`\`\`

Completa el bloque de solicitud in \`CHANGE-REQUEST.md\`, en la raíz del proyecto — qué debe cambiar, por qué, qué lo desencadenó, alcance, impacto, riesgo y prioridad. Say *\*"process the change request"\**. El agente devuelve una propuesta completa: decisión actual, cambio sugerido, impacto, riesgo y alternativas, y las filas exactas del mapa de stack que cambian. Tú apruebas; el agente redacta el ADR; tú lo aplicas.

**\*\*\`cdad/proposals/\` es el único directorio bajo \`cdad/\` en el que un agente puede escribir.\*\*** Esa única asimetría es lo que hace que la gobernanza sea real y no aspiracional: an agent that wants to change the architecture has exactly one move available — entregarte un borrador revisable.

El trabajo rutinario de implementación nunca pasa por este flujo. Si te encuentras creando solicitudes de cambio para tareas ordinarias, tus restricciones están definidas de forma demasiado amplia. Redúcelas.

\---

**## Mantener el mapa honesto**

Cuatro mecanismos, del más débil al más fuerte:

\| Mecanismo | Qué hace |

\| --- | --- |

\| \`AGENTS.md\` | Declara la regla: an ADR that doesn't declare its effect on the map is incomplete |

\| Skill \`cdad-adr\` | Exige un delta del stack antes/después más una fila en el registro de cambios |

\| Skill \`cdad-audit\` | Versiica cada vista contra los mansiiestos, el grafo real de imports y las reglas de alertas |

\| \`cdad/scripts/cdad-check-stack.sh\` | **\*\*Fails the build\*\*** when an ADR changes and the map does not |

Los tres primeros son instrucciones: un modelo puede incumplirlas. El cuarto es determinista.

\---

**## Principio de diseño**

Coloca cada preocupación en el plano que puede hacerla cumplir.

\| Plano | Mecanismo | Garantía | Costo de contexto |

\| --- | --- | --- | --- |

\| Control | \`permissions.deny\` + PreToolUse hook | Determinista | Zero |

\| Build | compuerta de CI in \`cdad/scripts/\` | Determinista, at merge | Zero |

\| Instrucción | \`AGENTS.md\`, \`.claude/rules/\` | Probabilístico | Tokens |

\| Procedimental | \`.claude/skills/\` | Bajo demanda | Zero until invoked |

**\*\*Todo lo que pueda hacerse cumplir en el plano de control nunca se escribe como una instrucción.\*\*** Poner "AI must not modsiy architecture files" en la ventana de contexto consume tokens en cada sesión y solo funciona de forma probabilística. Bloquear la escritura funciona de forma absoluta y no cuesta tokens.

Las instrucciones siguen siendo necesarias para todo lo que requiere juicio: si un cambio es arquitectónico, si el código contradice el contexto o si una abstracción está justsiicada. Ninguna regla de permisos decide esas cuestiones.

De aquí se deriva el segundo principio: **\*\*la capa determina tanto quién puede editar como cuándo se carga.\*\*** Al iniciar la sesión no se lee nada salvo las reglas y las restricciones estrictas — roughly 85 lines, no toda la base de conocimiento.

\---

**## Estructura**

\`\`\`

INDEX.md                        # mapa de todos los archivos — comienza aquí

AGENTS.md                       # reglas centrales portables — Kiro y Codex las leen de forma nativa

CHANGE-REQUEST.md               # ← la puerta de entrada: aquí declaras la intención

SOURCE-BRIEF.\*                  # ← tu diseño original, creado por cdad-bootstrap, que no vuelve a modsiicarse

.gitignore                      # ignora \_\_pycache\_\_/ generado por el hook — fusiónalo con el tuyo; no lo sobrescribas

│

cdad/

├── proposals/                  # aquí llegan los borradores del agente, a la espera de tu revisión

├── context/                    # L0 — gobernado, de solo lectura para los agentes

│   ├── stack.md                #   ← el mapa: 6 vistas, incluida observabilidad

│   ├── architecture.md

│   ├── solution-vision.md

│   ├── principles.md

│   ├── constraints.md          #   siempre en contexto, importado por .claude/CLAUDE.md

│   └── glossary.md

├── adr/                        # L1 — decisiones aceptadas

├── scripts/cdad-check-stack.sh # compuerta de CI

└── docs/                       # referencia humana, nunca cargada por agentes

    └── DOCS.md                 # metodología, portabilidad, migración

│

.claude/

├── CLAUDE.md                   # imports AGENTS.md + Claude Code specsiics

├── settings.json               # write protection for governed paths

├── hooks/protect-l0.py         # same block via shell too — exit 2

├── rules/                      # path-scoped: load only for matching files

└── skills/                     # cdad-bootstrap, cdad-propose-change, cdad-adr, cdad-audit

│

.kiro/steering/                 # Kiro mirrors of the reglas por ruta

\`\`\`

**### Por qué algunos archivos permanecen en la raíz**

Todo lo que no sea un punto de entrada fijo de una herramienta, ni uno de los dos archivos que tú modsiicas, vive bajo \`cdad/\`. \`.claude/\`, \`.kiro/\`, \`CHANGE-REQUEST.md\`, and \`SOURCE-BRIEF.\*\` son las excepciones, por dos razones dsierentes.

\`.claude/\` and \`.kiro/\` staying at the root no es una decisión de estilo — es la forma en que estas herramientas descubren su configuración.

Claude Code carga \`./CLAUDE.md\` or \`./.claude/CLAUDE.md\` (plus ancestor directories above the cwd) al iniciar la sesión. No recorre subdirectorios arbitrarios buscando uno. Nest \`.claude/\` a level deeper — say, inside \`cdad/.claude/\` — and Claude Code simply nunca carga it. No hay error ni advertencia: las reglas y skills quedan silenciosamente ausentes de todas las sesiones.

Kiro funciona de la misma manera with \`.kiro/steering/\`: it se descubre en una ubicación fija relativa a la raíz del proyecto, no mediante una búsqueda. Muévelo bajo \`cdad/\` and Kiro deja de encontrarlo, again without telling you.

\`AGENTS.md\` permanece en la raíz por la misma razón — it is the file Kiro and Codex leen de forma nativa por convención. Solo el contenido que ninguna herramienta descubre mediante una ruta fija — docs, the CI script, \`CLAUDE.md\` itself once redirected through \`.claude/CLAUDE.md\` — puede moverse a \`cdad/\`.

\`CHANGE-REQUEST.md\` and \`SOURCE-BRIEF.\*\` permanecen en la raíz por una razón dsierente: no por descubrimiento de herramientas, sino por ti. Ninguna herramienta lee automáticamente ninguno de los dos, so nada se rompería si vivieran bajo \`cdad/\`. But son los únicos dos archivos que el Solution Designer necesita encontrar — uno el primer día y otro cada vez que una decisión necesita cambiar — and ocultarlos junto a dos docenas de archivos de infraestructura contradice el objetivo de tener una única puerta de entrada evidente. Ambos permanecen exactamente tan protegidos como cualquier archivo de \`cdad/context/\` or \`cdad/adr/\` — las reglas de permisos y el hook los identsiican por nombre, no por ubicación.

\---

**## Capas de contexto**

\| Layer | Contenido | Política | Carga |

\| --- | --- | --- | --- |

\| L0 | \`cdad/context/\` | solo proponer | on demand (except \`constraints.md\`) |

\| L1 | \`cdad/adr/\` | proponer con revisión | on demand |

\| L2 | \`docs/\` | editable con revisión | nunca |

\| L3 | \`src/\`, \`tests/\`, pipelines, IaC | editable | n/a |

\---

**## Primeros pasos**

1\. Copia \`INDEX.md\`, \`AGENTS.md\`, \`CHANGE-REQUEST.md\`, \`.claude/\` (includes \`.claude/CLAUDE.md\`), \`cdad/\` (includes \`cdad/docs/\` and \`cdad/scripts/\`), and \`.kiro/\` si you use Kiro a la raíz de tu proyecto. \`CHANGE-REQUEST.md\` pertenece a la raíz exactamente como se entrega — no lo muevas bajo \`cdad/\`, y no vuelvas a crear \`CLAUDE.md\`, \`docs/\`, or \`scripts/\` como carpetas independientes de primer nivel; those live inside \`.claude/\` and \`cdad/\` now. Fusiona el \`.gitignore\` con el tuyo si ya tienes uno — it just ignora the \`\_\_pycache\_\_/\` the protection hook generates the first time it runs.

2\. Ejecuta el \`cdad-bootstrap\` skill (say *\*"bootstrap CDAD"\** or *\*"set up CDAD"\**) en lugar de completar \`cdad/context/\` manualmente. Comprueba si ya tienes un documento de solución, te pregunta directamente aquello que no responde, confirma el resultado contigo, y solo entonces redacta los seis archivos para que los apliques. Conservar \`constraints.md\` breve en cualquier caso: it is el único que se carga en cada sesión..

3\. Si prefieres completarlo tú mismo: comienza con \`cdad/context/stack.md\`, obliga a definir las decisiones que los demás archivos describen en prosa. Deja una celda vacía en lugar de adivinar — una celda vacía representa una decisión aún no tomada, y precisamente ese es el objetivo.

4\. Ajusta the \`paths:\` globs in \`.claude/rules/\` a la estructura de carpetas de tu proyecto. They ship with \`src/\`, \`tests/\`, \`infra/\`, \`deploy/\`.

5\. Conecta \`cdad/scripts/cdad-check-stack.sh\` a CI contra tu rama por defecto.

6\. Ejecuta una sesión y luego \`/context\`. Solo \`.claude/CLAUDE.md\`, \`AGENTS.md\`, and \`constraints.md\` deberían estar cargados.

7\. **\*\*Versiica que el guardrail sea real:\*\*** pide al agente que edite \`cdad/context/stack.md\`. It must be *\*blocked\**, not merely reluctant. Si solo duda, la capa de enforcement no se está cargando.

**### Actualización al modelo de dos regímenes**

Si estás incorporando este cambio a un proyecto cuyo bootstrap se realizó antes de que existiera, run \`./cdad/scripts/cdad-freeze.sh\` inmediatamente después de actualizar, si \`cdad/context/\` ya contiene contenido real. Hasta hacerlo, ese contenido vuelve a ser escribible por el agente.

Mapa completo de archivos: [\`INDEX.md\`]\(https\://github.com/mgriott/cdad-bootstrap/blob/main/INDEX.md) · Actualización desde v1: [\`cdad/docs/DOCS.md\`]\(cdad/docs/DOCS.md#migrating-from-cdad-v1)

\---

**## Compatibilidad con herramientas**

\| Capacidad | Claude Code | Kiro | Codex |

\| --- | --- | --- | --- |

\| Reglas centrales portables | mediante importación | nativo | nativo |

\| Carga condicional | \`paths:\` | \`inclusion: fileMatch\` | nested \`AGENTS.md\` |

\| Procedimientos bajo demanda | Skills | \`inclusion: manual\` | prompt |

\| Bloqueo determinista de escritura | yes | \`permissions.yaml\` (1.0+) | config globs |

\| Contexto gobernado + compuerta de CI | yes | yes | yes |

Claude Code ejecuta todo. Kiro's \`permissions.yaml\` cubre declarativamente las rutas de infraestructura incondicionales (1.0+); the regime-conditional paths (\`cdad/context/\`, \`cdad/adr/\`) recurren al hook compartido más la compuerta de CI, porque un archivo estático no puede expresar una condición sobre \`cdad/.frozen\`. Codex mantiene el bloqueo de escritura pero pierde la carga condicional de grano fino.

Detalles y soluciones alternativas: [\`cdad/docs/DOCS.md\`]\(cdad/docs/DOCS.md#portability-claude-code-kiro-codex)

**### Elimina lo que no uses**

El kit incluye adaptadores para las tres herramientas. Mantener adaptadores que nadie utiliza reproduce el mismo defecto de duplicación que CDAD v2 fue diseñado para eliminar — los espejos divergen y dejas de confiar en cualquiera de los dos. **\*\*Elimínalos desde el primer día.\*\***

\| Usas | Conservar | Eliminar |

\| --- | --- | --- |

\| Claude Code only | \`AGENTS.md\`, \`.claude/\` (incl. \`.claude/CLAUDE.md\`) | \`.kiro/\` |

\| Kiro only | \`AGENTS.md\`, \`.kiro/\` | \`.claude/\` |

\| Codex only | \`AGENTS.md\` | \`.claude/\`, \`.kiro/\` |

\| More than one | todo | nada |

\`\`\`

\# Claude Code only

rm -rf .kiro

\# Kiro only

rm -rf .claude

\# Codex only

rm -rf .claude .kiro

\`\`\`

**\*\*Nunca elimines \`AGENTS.md\`.\*\*** Contiene las reglas centrales. Claude Code imports it from \`.claude/CLAUDE.md\`; Kiro and Codex read it nativoly.

Dos consecuencias que conviene conocer antes de eliminar:

**\*\*Eliminar \`.claude/\` elimina la capa de enforcement.\*\*** \`settings.json\` and \`hooks/protect-l0.py\` are what make L0 protection deterministic rather than advisory. On Kiro, \`permissions.yaml\` (1.0+) covers the unconditional machinery paths; on Codex, or for the regime-conditional \`cdad/context/\`/\`cdad/adr/\` paths on Kiro, you are falling back to the compuerta de CI — weaker, but still real. No la omitas.

**\*\*En Codex, agrega archivos de instrucciones anidados.\*\*** Codex has no reglas por ruta, so recrea el efecto by colocando \`AGENTS.md\` files cerca del código que gobiernan, porting the content from \`.claude/rules/\` antes de eliminarlo:

\`\`\`

AGENTS.md          # core

src/AGENTS.md      # implementation rules

infra/AGENTS.md    # infrastructure rules

\`\`\`

Ten en cuenta también que Kiro carga \`AGENTS.md\` completo en cada sesión — no tiene modos de inclusión. Tu núcleo permanece pequeño de cualquier manera, pero el ahorro al inicio es menor allí que en Claude Code.

\---

**## Lo que mantienes**

\`cdad/context/\` and \`cdad/adr/\` — aplicados por ti, nunca escritos por un agente. \`CHANGE-REQUEST.md\` es tuyo para completarlo cada vez que algo necesite cambiar. \`SOURCE-BRIEF.\*\` se escribe una vez, por \`cdad-bootstrap\`, y luego se deja intacto. Todo lo que está bajo \`.claude/\`, \`.kiro/\`, and \`cdad/scripts/\` is CDAD runtime and rara vez necesita cambios más allá de los globs de rutas.

\---

**## Requisitos**

Claude Code, Kiro, or Codex. El hook de protección necesita \`python3\`, presente de forma predeterminada en Linux y macOS. La compuerta de CI necesita \`git\` and \`bash\`.

\---

**## Evolución**

CDAD es una metodología en evolución centrada en la gobernanza del contexto en el desarrollo asistido por IA. El trabajo futuro puede extenderla a software solutions, cloud and infrastructure, agentic systems, documentation, and knowledge governance — preservando el principio central:

\> **\*\*El contexto es la Fuente de Verdad.\*\***

Relacionado: [CDAD Framework]\(https\://github.com/mgriott/context-driven-ai-development) — metodología, whitepapers, principios y modelo de gobernanza.

\---

**## Licencia**

Creative Commons Attribution 4.0 Internacional (CC BY 4.0).

Eres libre de compartir, adaptar y desarrollar este trabajo, incluso con fines comerciales, siempre que se otorgue la atribución correspondiente.

[https\://creativecommons.org/licenses/by/4.0/]\(https\://creativecommons.org/licenses/by/4.0/)

Copiaright © 2026 Moisés Griott