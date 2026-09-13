# AGENTS.md — CDAD Bootstrap Agent Contract

This file defines the portable agent-facing contract for CDAD Bootstrap.

## Mission

When asked to bootstrap CDAD into a project, establish the CDAD workspace contract without destroying, moving, guessing, or silently overwriting host-project content.

The governing principle is:

> **Context is the Source of Truth.**

## Before changing anything

1. Read `README-CDAD.md`.
2. Inspect the host project.
3. Identify existing files with CDAD-required names.
4. Identify design/source documents at the project root.
5. If there is no source document, continue through conversation.
6. If multiple candidate source documents exist, ask the user. Never guess.
7. Never silently overwrite an existing file.

## Required workspace

The CDAD bootstrap contract is:

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

Tool-specific integration directories remain at their required locations.

## Bootstrap behavior

During initial bootstrap:

1. Obtain or confirm the design/source document.
2. Verify that it is complete enough to serve as a source.
3. Inspect `cdad/context/` for placeholders.
4. Map the source into the six governed context files.
5. Ask for missing information rather than inventing decisions.
6. Summarize the resulting context.
7. Obtain explicit human confirmation.
8. Write the confirmed context.
9. Preserve the source as `SOURCE-BRIEF.*`.
10. Ask the user to review.
11. Freeze only after explicit confirmation.

## Two confirmations

Do not collapse these into one:

### Confirmation A — source/design

Is the user's design document complete and ready to be used?

### Confirmation B — governed context

Do the generated six context files accurately represent the user's intended solution?

Both confirmations matter.

## Conflict policy

If a host project already contains:

- `AGENTS.md`
- `INDEX.md`
- `CHANGE-REQUEST.md`
- `CDAD-COMPLETION.md`
- `cdad/`
- `.claude/`
- `.kiro/`

inspect before changing.

Report conflicts explicitly.

Do not silently overwrite.

Preserve the host project's existing source structure.

## Governed regime

Before:

```text
cdad/.frozen
```

the bootstrap procedure may populate `cdad/context/`.

After:

```text
cdad/.frozen
```

do not directly modify governed context.

Architectural changes must go through:

```text
CHANGE-REQUEST.md
        ↓
cdad/proposals/
        ↓
cdad/adr/
        ↓
cdad/context/stack.md
```

## Change requests

Routine implementation does not require a change request.

Use `CHANGE-REQUEST.md` when a requested change affects a governed decision.

A proposal should identify:

- current decision
- requested change
- reason
- trigger
- scope
- impact
- risk
- alternatives
- affected map rows

## Protected context

Do not bypass the protection mechanism by:

- renaming governed files;
- creating duplicate copies outside the governed location;
- moving governed files;
- editing through an alternate path;
- disabling the guardrail to make a change.

If the requested change is legitimate, use the governed change process.

## Source preservation

`SOURCE-BRIEF.*` is the original source used to bootstrap the governed context.

Do not silently rewrite it after bootstrap.

If the user wants the source design changed, treat that as an explicit design change and report the consequences for governed context.

## Completion report

After bootstrap, report:

```text
CDAD Bootstrap completed

Created:
- ...

Preserved:
- ...

Conflicts:
- ...

Source:
- ...

Context confirmation:
- confirmed / pending

Freeze:
- executed / pending

Protection verification:
- passed / pending

CI gate:
- configured / pending

Human action required:
- ...
```

## Non-negotiable rules

- Never guess architecture.
- Never silently overwrite.
- Never silently move CDAD artifacts.
- Never claim a decision was approved when it was not.
- Never treat generated context as ratified without human confirmation.
- Never delete `AGENTS.md`.
- Never bypass governed protection after freeze.

### Bootstrap documentation vs. installed project layout

The CDAD Bootstrap repository and an installed CDAD workspace have different documentation locations.

In the **CDAD Bootstrap repository**, the bootstrap documentation remains at the repository root:

- `README-CDAD.md`
- `README-CDAD.es.md`
- `INSTALLATION.md`
- `INSTALLATION.es.md`
- `USAGE.md`
- `USAGE.es.md`
- `AGENTS.md`

When an agent installs/bootstraps CDAD into a **host project**, it MUST organize the installed CDAD workspace as follows:

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

If the host project uses Claude Code or Kiro, their adapter directories remain at the host-project root:

```text
.claude/
.kiro/
```

They MUST NOT be moved under `cdad/`.

The bootstrap repository's `README-CDAD.md`, `INSTALLATION.md`, and `USAGE.md` are **source/reference documentation for the bootstrap package**. Do not copy those files into the host project's root.

The **project-facing CDAD README MUST be installed as**:

```text
cdad/README.md
```

`cdad/README.md` is the operational README for CDAD as installed in that project. It should explain the installed CDAD workspace and its operation; it is not a reason to dump the bootstrap repository's documentation into the host project's root.

The agent MUST:

1. Clone/download the CDAD Bootstrap repository into a temporary/work location.
2. Read the bootstrap `AGENTS.md` and canonical `README-CDAD.md` before installing.
3. Preserve the host project's existing structure and files.
4. Create/organize the CDAD scaffold under `cdad/` as defined above.
5. Keep `AGENTS.md`, `CDAD-COMPLETION.md`, `CHANGE-REQUEST.md`, and `INDEX.md` at the host-project root.
6. Install the project-facing README at `cdad/README.md`.
7. Keep CDAD-owned `adr/`, `context/`, `docs/`, `proposals/`, and `scripts/` under `cdad/`.
8. Preserve the original design/source brief (`SOURCE-BRIEF.*`) in the host project according to the CDAD bootstrap procedure.
9. Never move, rename, duplicate, redistribute, or silently overwrite an existing host-project file.
10. If a target file already exists, stop and report the conflict rather than silently replacing it.
11. Do not automatically freeze the project. `cdad/scripts/cdad-freeze.sh` is run after human review/confirmation.

The bootstrap documentation stays at the root **of the bootstrap repository**. The installed operational documentation and CDAD-owned artifacts go under `cdad/` **inside the host project**.
