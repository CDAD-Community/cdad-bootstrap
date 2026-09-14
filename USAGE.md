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

Routine implementation does not require a `cdad/CHANGE-REQUEST.md`.

### 3. Detect an architectural change

If a requested change affects an architectural decision, technology choice, dependency rule, deployment topology, observability design, or another governed decision, do not silently modify the governed map.

Use:

```text
cdad/CHANGE-REQUEST.md
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

`cdad/context/stack.md` provides seven views:

1. stack
2. components
3. deployment
4. observability
5. dependency rules
6. map change log
7. drift signals — paths outside `cdad/` that carry architectural weight, watched by `detect-drift.py`

Use the map as the first architectural orientation point.

If a stack entry has no ADR in its `Locked by` field, investigate it as an ungoverned decision.

---

## The backlog

`cdad/backlog.md` is the development line: Epics, Stories, current focus, and
next work. It is a planning artifact, not architecture — precedence is
governed context → ADR → backlog → implementation, and a Story never
overrides an architectural decision.

Before development work, establish the applicable Epic/Story from the
backlog. Adding, removing, or materially changing one goes through
`cdad/CHANGE-REQUEST.md`, same as an architecture change. Updating a Story's
status or the Current Focus / Next Work / Blocked lists during
already-approved work is a direct edit, not a change request.

Run `cdad/scripts/cdad-check-backlog.sh` for structural integrity (unique
IDs, valid status values); run `cdad-audit` to reconcile the backlog against
what is actually defined and actually done.

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

CDAD provides one adapter per supported ADE. A project installs exactly the
one matching the ADE that executed its bootstrap — never more than one —
resolved automatically, not chosen by copying files around afterward.

- Claude Code uses `.claude/`.
- Kiro uses `.kiro/`.
- Codex uses `AGENTS.md` and applicable configuration, no extra adapter file.
- GitHub Copilot uses `.github/copilot-instructions.md` plus `AGENTS.md`.

**Never remove `AGENTS.md`.**

---

## Operational checklist

Before implementation:

- [ ] Read applicable governed context.
- [ ] Establish the applicable Epic/Story from `cdad/backlog.md`, if one exists.
- [ ] Determine whether the task is routine or architectural.
- [ ] If architectural, or a new/changed Epic/Story, create/process a change request.

During implementation:

- [ ] Keep implementation aligned with governed context.
- [ ] Do not silently modify governed decisions.
- [ ] Update the Story's status and Current Focus as work actually progresses.
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

Whichever single adapter was resolved — `.claude/`, `.kiro/`, or `.github/copilot-instructions.md` — remains at the host-project root. Only that one is installed.

`README-CDAD.md` and `README-CDAD.es.md` ARE copied into the host-project
root as the human-facing entry points. `INSTALLATION.md` and `USAGE.md`
(and their `.es.md` pairs) are bootstrap-repository reference documentation
only — do not copy those two. The installed, project-facing CDAD README
belongs at `cdad/README.md`.

The agent must preserve existing host-project files, must not silently overwrite conflicts, and must not run the freeze step automatically. Human review and confirmation precede freezing.
