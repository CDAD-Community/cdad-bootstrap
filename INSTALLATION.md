# CDAD Bootstrap — Installation Guide

This document contains the detailed installation procedures for CDAD Bootstrap.

The repository README remains the canonical entry point. This guide expands the installation details without removing the Quick Start from the README.

## Installation modes

CDAD supports two initial installation modes:

1. **Manual installation** — a human copies and integrates the CDAD bootstrap into an existing project.
2. **Agent-assisted installation** — an ADE/AI coding agent reads the CDAD documentation and performs the bootstrap under explicit rules.

In both modes, the final objective is the same: establish the CDAD workspace contract, populate governed context, obtain human confirmation, and freeze the context before normal governed development.

---

## Prerequisites

- A project repository.
- Git.
- Bash for the CI gate and shell scripts.
- Python 3 for the protection hook.
- Claude Code, Kiro, Codex, GitHub Copilot, or another ADE capable of following the CDAD bootstrap procedure.
- A completed design/source document is recommended but not mandatory.

The design document may be Markdown, text, Word, PDF, or another common format.

---

## Manual installation

### 1. Inspect the host project

Before copying CDAD, inspect the project root.

Identify:

- existing `AGENTS.md`
- existing `README-CDAD.md` / `README-CDAD.es.md`
- existing `cdad/` (and, inside it, `INDEX.md`, `CHANGE-REQUEST.md`, `CDAD-COMPLETION.md`, `backlog.md`)
- existing `.claude/`
- existing `.kiro/`
- existing `.github/copilot-instructions.md`
- existing `.gitignore`
- source/design documents
- files or directories with names that CDAD requires

**Do not overwrite existing files silently.**

If a required CDAD filename already exists, stop and resolve the conflict deliberately.

### 2. Install the CDAD scaffolding

The resulting workspace must contain:

```text
/
├── AGENTS.md
├── README-CDAD.md
├── README-CDAD.es.md
├── SOURCE-BRIEF.*                # if a source document existed
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

Only ADE discovery/integration files, the two CDAD READMEs, `AGENTS.md`,
and `SOURCE-BRIEF.*` belong at the project root — see *Workspace hygiene*
in `README-CDAD.md`. `INDEX.md`, `CHANGE-REQUEST.md`, `CDAD-COMPLETION.md`,
and `backlog.md` are generated directly under `cdad/`, never at the root.

Install only the ADE-specific adapter matching the ADE you actually use — `.claude/` for Claude Code, `.kiro/` for Kiro, or `.github/copilot-instructions.md` for GitHub Copilot (Codex takes no extra adapter file). Do not copy the others "just in case"; the source repository ships every adapter as a catalog, not as a package to install whole. See the ADE adapter matrix in the README.

### 3. Preserve the source design

If the project contains a design document and it is the source used for bootstrap, preserve it as:

```text
SOURCE-BRIEF.*
```

Do not silently modify the original source.

The purpose of `SOURCE-BRIEF.*` is to retain the original human-authored design that was used to populate the governed context.

### 4. Merge `.gitignore`

If the host project already has a `.gitignore`, merge CDAD's required entries into it.

Do not replace the host project's `.gitignore`.

The protection hook may generate `__pycache__/`; ensure the relevant generated files remain ignored.

### 5. Populate the context

Preferred method:

```text
bootstrap CDAD
```

or:

```text
set up CDAD
```

Do not begin by manually inventing the six context files if the bootstrap procedure is available.

If you deliberately choose manual authoring, start with:

```text
cdad/context/stack.md
```

and explicitly mark unknown decisions rather than guessing.

### 6. Review

The human owner reviews:

- architecture
- technology stack
- requirements
- constraints
- principles
- solution vision
- glossary
- stack map

The context is not ratified merely because files were generated.

### 7. Freeze

When the context is complete and confirmed:

```bash
./cdad/scripts/cdad-freeze.sh
```

The freeze operation establishes the governed regime and creates:

```text
cdad/.frozen
```

From that point, governed context is protected against direct agent writes according to the installed enforcement adapters.

### 8. Verify the guardrail

Ask the agent to modify:

```text
cdad/context/stack.md
```

The applicable enforcement mechanism should block the write.

A model saying “I should not do that” is not equivalent to deterministic enforcement.

### 9. Install the CI gate

Wire:

```text
cdad/scripts/cdad-check-stack.sh
```

into CI against the project's default branch.

The goal is to ensure that governed architectural changes and the architecture map remain synchronized.

---

## Agent-assisted installation

An agent should treat this repository as an executable documentation contract, not as a collection of files to copy blindly.

### Agent procedure

1. Read `README-CDAD.md`.
2. Read `AGENTS.md`.
3. Detect the ADE actually executing this bootstrap and resolve exactly one adapter for it. If more than one ADE looks possible and the executing one can't be established with confidence, stop and ask — never guess, and never install more than one native adapter.
4. Inspect the host project.
5. Identify the host project's design/source document.
6. If there is no document, proceed through conversation.
7. If there are multiple candidates, ask the user.
8. Never guess which source document is authoritative.
9. Never overwrite an existing same-name file silently.
10. Create the CDAD workspace contract: the portable core plus only the resolved adapter, explicitly excluding the others.
11. Map the confirmed source into the governed context.
12. Check for defined Epics/Stories (a requirements doc, issue tracker, or prior conversation). If found, reconcile them into `cdad/backlog.md`; if none exist, say so explicitly rather than inventing them.
13. Ask the user to confirm the generated context.
14. Preserve the source as `SOURCE-BRIEF.*`.
15. Freeze only after explicit human confirmation.
16. Verify protection.
17. Report the final state.

### Required agent report

After installation, the agent should report:

- detected ADE and resolved adapter
- adapters explicitly excluded
- whether native adapter support exists for this ADE
- files created
- files preserved
- conflicts found
- files intentionally skipped
- source document used
- whether context was confirmed
- whether `cdad/backlog.md` is defined and reconciled with any known Epics/Stories
- whether freeze was executed
- whether protection was verified
- whether CI gate was connected
- any remaining human action

---

## Existing projects and upgrades

If CDAD is being added to an existing project, preserve the host architecture and source tree.

CDAD is not a license to reorganize the host project.

If a host file conflicts with a CDAD-required file:

1. identify the conflict;
2. explain the role of both files;
3. ask for a decision;
4. resolve explicitly;
5. record the resolution when it affects governed architecture.

### Two-regime upgrade

For projects created before the two-regime freeze model:

```bash
./cdad/scripts/cdad-freeze.sh
```

Run this after verifying that `cdad/context/` contains real context and no template placeholders.

---

## Installation checklist

- [ ] Host project inspected.
- [ ] Executing ADE detected and exactly one adapter resolved (asked, not guessed, if ambiguous).
- [ ] Only the resolved adapter installed; the others explicitly excluded.
- [ ] Required CDAD files identified.
- [ ] Existing files protected from silent overwrite.
- [ ] CDAD scaffolding created.
- [ ] `SOURCE-BRIEF.*` preserved when applicable.
- [ ] `.gitignore` merged.
- [ ] Context populated.
- [ ] `cdad/backlog.md` present; known Epics/Stories reconciled or explicitly absent.
- [ ] Human review completed.
- [ ] Context explicitly confirmed.
- [ ] `cdad/.frozen` created.
- [ ] Protected write tested.
- [ ] CI gate connected.
- [ ] Installation reported.

---

## Next step

After installation, continue with [USAGE.md](USAGE.md).

### Deployment target: bootstrap repository vs. host project

The documentation files in this bootstrap repository stay at the **bootstrap repository root**.

When an agent deploys CDAD into a host project, it MUST reorganize the installed workspace so that CDAD-owned runtime content is under `cdad/`:

```text
/
├── AGENTS.md
├── README-CDAD.md
├── README-CDAD.es.md
├── SOURCE-BRIEF.*                # if a source document existed
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

Whichever single adapter was resolved — `.claude/` (Claude Code), `.kiro/` (Kiro), or `.github/copilot-instructions.md` (GitHub Copilot) — remains at the host-project root. Only that one is installed, never more than one.

`README-CDAD.md` and `README-CDAD.es.md` ARE copied into the host-project
root — they are the human-facing CDAD entry points and must stay
discoverable there. `INSTALLATION.md` and `USAGE.md` (and their `.es.md`
pairs) are **bootstrap-repository reference documentation only** — do not
copy those two into the host project. The installed, project-facing CDAD
README belongs at `cdad/README.md`.

The agent must preserve existing host-project files, must not silently overwrite conflicts, and must not run the freeze step automatically. Human review and confirmation precede freezing.
