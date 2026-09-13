# CDAD Bootstrap — Usage Guide

CDAD governs the context that guides AI-assisted development. The normal development loop is:

```text
Context → Decision → Proposal → Approval → Implementation → Verification
```

## The normal workflow

### 1. Start from governed context

Before making an implementation decision, the agent should read the applicable governed context.

At minimum, this includes the core rules and relevant context files.

The goal is not to load every document into every session. CDAD deliberately separates always-needed constraints from context that is required only for a specific task.

### 2. Work on implementation

Routine implementation belongs to the implementation layer.

The agent may modify source code, tests, pipelines, and infrastructure according to the project's rules.

Routine implementation does not require a `CHANGE-REQUEST.md`.

### 3. Detect an architectural change

If a requested change affects an architectural decision, technology choice, dependency rule, deployment topology, observability design, or another governed decision, do not silently modify the governed map.

Use:

```text
CHANGE-REQUEST.md
```

### 4. Propose the change

The agent creates a reviewable proposal under:

```text
cdad/proposals/
```

The proposal should explain:

- current decision
- requested change
- reason
- trigger
- scope
- impact
- risk
- alternatives
- affected architecture-map rows

### 5. Approve

The human reviews the proposal.

Approval is a governance decision, not an implementation detail.

### 6. Record the decision

The approved change becomes an ADR under:

```text
cdad/adr/
```

The architecture map under:

```text
cdad/context/stack.md
```

must reflect the accepted decision.

### 7. Verify

Run the relevant audit/check mechanisms.

The CI gate:

```text
cdad/scripts/cdad-check-stack.sh
```

must fail when the governed architecture and its map become inconsistent.

---

## The architecture map

`cdad/context/stack.md` provides six views:

1. stack
2. components
3. deployment
4. observability
5. dependency rules
6. map change log

Use the map as the first architectural orientation point.

If a stack entry has no ADR in its `Locked by` field, investigate it as an ungoverned decision.

---

## Change request example

A request should communicate intent rather than prescribe an implementation blindly.

Example:

```text
What needs to change?
Replace the current cache technology.

Why?
The current technology no longer meets the agreed operational constraints.

Trigger:
New deployment requirements.

Scope:
Caching layer and related observability.

Impact:
Architecture, deployment, configuration and operational documentation.

Risk:
Migration compatibility and cache invalidation behavior.

Priority:
High.
```

The agent should turn this into a proposal rather than directly editing the architecture map.

---

## Context layers

### L0 — governed context

```text
cdad/context/
```

Contains the current governed understanding of the solution.

### L1 — architecture decisions

```text
cdad/adr/
```

Contains accepted decisions and their rationale.

### L2 — documentation

```text
cdad/docs/
```

Contains human reference material and methodology documentation.

### L3 — implementation

```text
src/
tests/
pipelines/
IaC/
```

Contains the implementation governed by the upper layers.

---

## Freeze and the two-regime model

CDAD distinguishes between:

### Bootstrap regime

Before freeze:

- context can be populated by the bootstrap procedure;
- the design is still being confirmed;
- the context is not yet ratified.

### Governed regime

After:

```text
cdad/.frozen
```

the governed context is protected.

Architectural changes must follow the change-request/proposal/ADR process.

---

## Keeping context useful

Keep the always-loaded context small.

`constraints.md` should contain only constraints that genuinely need to be available continuously.

Put detailed explanations, methodology, migration material, and reference documentation under `cdad/docs/`.

Do not turn every instruction into a permanently loaded rule.

---

## Tool-specific adapters

CDAD provides adapters for supported ADEs.

- Claude Code uses `.claude/`.
- Kiro uses `.kiro/`.
- Codex uses `AGENTS.md` and applicable configuration.

Keep only the adapters you use.

**Never remove `AGENTS.md`.**

---

## Operational checklist

Before implementation:

- [ ] Read applicable governed context.
- [ ] Determine whether the task is routine or architectural.
- [ ] If architectural, create/process a change request.

During implementation:

- [ ] Keep implementation aligned with governed context.
- [ ] Do not silently modify governed decisions.
- [ ] Preserve host-project structure.

Before merge:

- [ ] Confirm required ADRs exist for architectural changes.
- [ ] Confirm the architecture map reflects accepted decisions.
- [ ] Run the stack check.
- [ ] Review the resulting diff.

---

## Guiding principle

> **Context is the Source of Truth.**

CDAD does not attempt to make AI incapable of changing software. It establishes a governed boundary around the decisions that define what the software is supposed to be.

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
