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
- Claude Code, Kiro, Codex, or another ADE capable of following the CDAD bootstrap procedure.
- A completed design/source document is recommended but not mandatory.

The design document may be Markdown, text, Word, PDF, or another common format.

---

## Manual installation

### 1. Inspect the host project

Before copying CDAD, inspect the project root.

Identify:

- existing `AGENTS.md`
- existing `INDEX.md`
- existing `CHANGE-REQUEST.md`
- existing `.claude/`
- existing `.kiro/`
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

ADE-specific integration directories such as `.claude/` and `.kiro/` remain at the project root.

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
3. Inspect the host project.
4. Identify the host project's design/source document.
5. If there is no document, proceed through conversation.
6. If there are multiple candidates, ask the user.
7. Never guess which source document is authoritative.
8. Never overwrite an existing same-name file silently.
9. Create the CDAD workspace contract.
10. Map the confirmed source into the governed context.
11. Ask the user to confirm the generated context.
12. Preserve the source as `SOURCE-BRIEF.*`.
13. Freeze only after explicit human confirmation.
14. Verify protection.
15. Report the final state.

### Required agent report

After installation, the agent should report:

- files created
- files preserved
- conflicts found
- files intentionally skipped
- source document used
- whether context was confirmed
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
- [ ] Required CDAD files identified.
- [ ] Existing files protected from silent overwrite.
- [ ] CDAD scaffolding created.
- [ ] `SOURCE-BRIEF.*` preserved when applicable.
- [ ] `.gitignore` merged.
- [ ] Context populated.
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

For Claude Code and/or Kiro, `.claude/` and `.kiro/` remain at the host-project root.

Do not copy the bootstrap repository's `README-CDAD.md`, `INSTALLATION.md`, or `USAGE.md` into the host-project root. The installed, project-facing CDAD README belongs at `cdad/README.md`.

The agent must preserve existing host-project files, must not silently overwrite conflicts, and must not run the freeze step automatically. Human review and confirmation precede freezing.
