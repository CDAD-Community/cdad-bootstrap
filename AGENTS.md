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
├── backlog.md
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

## Backlog governance

`backlog.md`, at the project root, is the development line: Epics, Stories,
and the work currently expected to be built. It is a development-planning
artifact, not architecture — never a second source of truth beside `cdad/`.

**Precedence:** Governed Context / L0 → ADR → this backlog → implementation.
A Story that contradicts governed context or an accepted ADR is a finding,
not a resolution — surface it through `CHANGE-REQUEST.md`; never let a
Story silently override architecture.

**What goes through `CHANGE-REQUEST.md` → `cdad/proposals/` → decision:**
adding or removing an Epic or Story, or materially changing its scope or
acceptance criteria — the same funnel as an architectural change.

**What does not:** updating a Story's status, or the *Current Focus* /
*Next Work* / *Blocked* lists, as part of already-approved implementation
work. Routine progress tracking is not a governed decision; do not force it
through the change-request flow, and do not use it as a backdoor to add or
remove Epics/Stories either — that distinction requires judgment, not a
loophole.

**Before development work, establish the applicable Epic/Story from
`backlog.md`.** If defined Epics/Stories exist elsewhere (a requirements
doc, an issue tracker, prior conversation) but are missing from the
backlog, reconcile them through the normal change process — do not
silently ignore them and do not silently rewrite the backlog to match.
Report the gap and offer the `cdad-propose-change` skill. If no Epics or
Stories are defined at all, say so explicitly and ask whether the
development line should be defined, or proceed only where the requested
work is genuinely independent of one. Never invent business Epics/Stories
and present them as user-defined requirements — proposed ones must stay
labeled `Status: Proposed` until accepted.

Structural integrity (unique IDs, valid status values) is checked
deterministically by `cdad/scripts/cdad-check-backlog.sh`; whether an
Epic/Story is real, current, and correctly linked to actual work is a
judgment call for the `cdad-audit` skill.

## Adapters vs. portable core

CDAD ships a portable core (this file, `INDEX.md`, `backlog.md`,
`CHANGE-REQUEST.md`, `CDAD-COMPLETION.md`, `cdad/`) plus one adapter per supported ADE: Claude
Code → `.claude/`, Kiro → `.kiro/`, Codex → `AGENTS.md` alone, GitHub
Copilot → `.github/copilot-instructions.md`. The CDAD Bootstrap source
carries every adapter as a catalog; a target project receives the portable
core plus exactly the one adapter matching the ADE that is executing the
bootstrap — never the whole catalog, never more than one native adapter.

Base the choice on the ADE actually executing the bootstrap, never on the
underlying model (a Claude model is not Claude Code; a GPT model is not
Codex) and never by guessing from adapter files that merely happen to exist
in the target repo. If the executing ADE cannot be established with
confidence, ask — do not guess. Full resolution table and procedure: the
`cdad-bootstrap` skill.

## Bootstrap behavior

During initial bootstrap:

1. Detect the ADE executing the bootstrap and resolve exactly one adapter for
   it (see *Adapters vs. portable core*) before touching the filesystem.
2. Obtain or confirm the design/source document.
3. Verify that it is complete enough to serve as a source.
4. Inspect `cdad/context/` for placeholders.
5. Map the source into the six governed context files.
6. Ask for missing information rather than inventing decisions.
7. Summarize the resulting context.
8. Obtain explicit human confirmation.
9. Write the confirmed context.
10. Preserve the source as `SOURCE-BRIEF.*`.
11. Ask the user to review.
12. Freeze only after explicit confirmation.

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
- `backlog.md`
- `INDEX.md`
- `CHANGE-REQUEST.md`
- `CDAD-COMPLETION.md`
- `cdad/`
- `.claude/`
- `.kiro/`
- `.github/copilot-instructions.md`

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

After bootstrap, report in chat **and** append this same report to
`CDAD-COMPLETION.md` at the project root — that file is the durable record;
chat output alone is lost once the session ends. Append, do not overwrite,
on a later re-run (ADE/adapter switch, migration, re-freeze).

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

Detected ADE:
- ...

Adapter installed:
- ...

Adapters excluded:
- ...

Native support:
- yes / no — ...

Backlog:
- defined / not yet defined — reconciled: yes / no / not applicable

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
- Never install an adapter for an ADE other than the one executing the bootstrap.
- Never infer the executing ADE from the underlying model or from adapter files that merely happen to exist; ask if it cannot be established with confidence.
- Never invent Epics or Stories and present them as user-defined requirements.
- Never let a Story in `backlog.md` silently override governed context or an accepted ADR.
- Never add or remove an Epic/Story, or materially change one, outside the `CHANGE-REQUEST.md` flow.

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
├── backlog.md
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

Install only the adapter matching the ADE executing the bootstrap (see *Adapters vs. portable core*). Whichever one it is, it remains at the host-project root, never moved under `cdad/`:

```text
.claude/                         # Claude Code
.kiro/                           # Kiro
.github/copilot-instructions.md  # GitHub Copilot
```

Codex takes no adapter file beyond `AGENTS.md` itself. Do not install the adapters for ADEs other than the one executing the bootstrap, even if the CDAD Bootstrap source contains them all.

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
4. Detect the ADE executing the bootstrap and resolve exactly one adapter for it; if it cannot be established with confidence, ask rather than guess.
5. Install the portable core plus only the resolved adapter, and explicitly exclude the others — the source repository is a catalog, not a package to install whole.
6. Create/organize the CDAD scaffold under `cdad/` as defined above.
7. Keep `AGENTS.md`, `backlog.md`, `CDAD-COMPLETION.md`, `CHANGE-REQUEST.md`, and `INDEX.md` at the host-project root.
8. Install the project-facing README at `cdad/README.md`.
9. Keep CDAD-owned `adr/`, `context/`, `docs/`, `proposals/`, and `scripts/` under `cdad/`.
10. Preserve the original design/source brief (`SOURCE-BRIEF.*`) in the host project according to the CDAD bootstrap procedure.
11. Never move, rename, duplicate, redistribute, or silently overwrite an existing host-project file.
12. If a target file already exists, stop and report the conflict rather than silently replacing it.
13. Do not automatically freeze the project. `cdad/scripts/cdad-freeze.sh` is run after human review/confirmation.
14. On re-run, never reintroduce an adapter that a prior bootstrap explicitly excluded, and never overwrite an existing adapter outside the normal conflict-reporting rule above.

The bootstrap documentation stays at the root **of the bootstrap repository**. The installed operational documentation and CDAD-owned artifacts go under `cdad/` **inside the host project**.
