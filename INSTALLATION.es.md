# CDAD Bootstrap — Guía de instalación

Este documento contiene los procedimientos detallados para instalar CDAD Bootstrap.

El README del repositorio sigue siendo la puerta de entrada canónica. Esta guía amplía la instalación sin sacar el Quick Start del README.

## Modos de instalación

CDAD admite dos modos de instalación inicial:

1. **Instalación manual** — una persona integra los archivos de CDAD en un proyecto existente.
2. **Instalación asistida por agente** — un ADE/agente de programación con IA lee la documentación de CDAD y realiza el bootstrap bajo reglas explícitas.

En ambos casos, el objetivo final es el mismo: establecer el contrato del workspace CDAD, poblar el contexto gobernado, obtener confirmación humana y congelar el contexto antes del desarrollo gobernado normal.

---

## Requisitos previos

- Un proyecto/repositorio.
- Git.
- Bash para el CI gate y los scripts.
- Python 3 para el hook de protección.
- Claude Code, Kiro, Codex u otro ADE capaz de seguir el procedimiento de bootstrap.
- Se recomienda un documento de diseño/origen terminado, aunque no es obligatorio.

El documento de diseño puede estar en Markdown, texto, Word, PDF u otro formato habitual.

---

## Instalación manual

### 1. Inspeccionar el proyecto anfitrión

Antes de copiar CDAD, inspecciona la raíz del proyecto.

Identifica:

- `AGENTS.md` existente
- `INDEX.md` existente
- `CHANGE-REQUEST.md` existente
- `.claude/` existente
- `.kiro/` existente
- `.gitignore` existente
- documentos de diseño/origen
- archivos o directorios cuyos nombres sean requeridos por CDAD

**No sobrescribas archivos existentes silenciosamente.**

Si ya existe un nombre requerido por CDAD, detente y resuelve el conflicto explícitamente.

### 2. Instalar el scaffolding de CDAD

El workspace final debe contener:

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

Los directorios de integración del ADE, como `.claude/` y `.kiro/`, permanecen en la raíz.

### 3. Preservar el diseño original

Si el proyecto contiene un documento de diseño y se utilizará como fuente del bootstrap, consérvalo como:

```text
SOURCE-BRIEF.*
```

No modifiques silenciosamente el documento original.

### 4. Combinar `.gitignore`

Si el proyecto ya posee `.gitignore`, combina las entradas necesarias de CDAD con él.

No reemplaces el `.gitignore` del proyecto.

### 5. Poblar el contexto

Método recomendado:

```text
bootstrap CDAD
```

o:

```text
set up CDAD
```

No comiences inventando manualmente los seis archivos de contexto si el procedimiento de bootstrap está disponible.

Si decides crearlos manualmente, comienza por:

```text
cdad/context/stack.md
```

y marca explícitamente las decisiones desconocidas en lugar de adivinarlas.

### 6. Revisar

El responsable humano debe revisar:

- arquitectura
- stack tecnológico
- requisitos
- restricciones
- principios
- visión de solución
- glosario
- mapa de stack

La generación de archivos no significa que el contexto esté ratificado.

### 7. Freeze

Cuando el contexto esté completo y confirmado:

```bash
./cdad/scripts/cdad-freeze.sh
```

Esto crea:

```text
cdad/.frozen
```

y establece el régimen gobernado.

### 8. Verificar el guardrail

Solicita al agente modificar:

```text
cdad/context/stack.md
```

El mecanismo de enforcement correspondiente debe bloquear la escritura.

Que el modelo diga “no debería hacerlo” no equivale a enforcement determinista.

### 9. Instalar el CI gate

Conecta:

```text
cdad/scripts/cdad-check-stack.sh
```

al CI contra la rama por defecto.

---

## Instalación asistida por agente

El agente debe tratar este repositorio como un contrato documental ejecutable, no como una colección de archivos que puede copiar sin analizar.

### Procedimiento del agente

1. Leer `README-CDAD.md`.
2. Leer `AGENTS.md`.
3. Inspeccionar el proyecto anfitrión.
4. Identificar el documento de diseño/origen.
5. Si no existe, trabajar mediante conversación.
6. Si existen varios candidatos, preguntar.
7. Nunca adivinar cuál es la fuente autorizada.
8. Nunca sobrescribir silenciosamente un archivo existente con el mismo nombre.
9. Crear el contrato de workspace CDAD.
10. Mapear la fuente confirmada al contexto gobernado.
11. Solicitar confirmación del contexto generado.
12. Preservar la fuente como `SOURCE-BRIEF.*`.
13. Ejecutar freeze solo después de confirmación humana explícita.
14. Verificar la protección.
15. Informar el estado final.

### Informe obligatorio del agente

Debe informar:

- archivos creados
- archivos preservados
- conflictos encontrados
- archivos omitidos deliberadamente
- documento fuente utilizado
- si el contexto fue confirmado
- si se ejecutó freeze
- si se verificó la protección
- si se conectó el CI gate
- acciones humanas pendientes

---

## Checklist

- [ ] Proyecto anfitrión inspeccionado.
- [ ] Archivos requeridos identificados.
- [ ] Protegidos los archivos existentes contra sobrescritura silenciosa.
- [ ] Scaffolding CDAD creado.
- [ ] `SOURCE-BRIEF.*` preservado cuando corresponde.
- [ ] `.gitignore` combinado.
- [ ] Contexto poblado.
- [ ] Revisión humana completada.
- [ ] Contexto confirmado explícitamente.
- [ ] `cdad/.frozen` creado.
- [ ] Escritura protegida verificada.
- [ ] CI gate conectado.
- [ ] Instalación informada.

---

## Siguiente paso

Continúa con [USAGE.es.md](USAGE.es.md).

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
