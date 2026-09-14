# CDAD Index

Every file in this kit: what it is, who owns it, and when it enters an agent's
context. If you read one file to orient yourself, read this one.

---

## Start here

| I want to... | Go to |
|---|---|
| Populate CDAD for the first time in this project | drop your solution doc at the project root, any name (optional), then run the `cdad-bootstrap` skill |
| Ratify a freshly-bootstrapped context so it becomes read-only | `cdad/scripts/cdad-freeze.sh` |
| Change the stack, architecture, any directive, or an Epic/Story | `CHANGE-REQUEST.md`, at the project root |
| See the development line — Epics, Stories, current focus | `backlog.md`, at the project root |
| Check whether an L3 change (infra, a manifest) contradicts ratified architecture | `.claude/skills/cdad-drift-response/SKILL.md`, or wait for the `CDAD DRIFT SIGNAL` warning |
| See what this system is, in one screen | `cdad/context/stack.md` |
| Understand why CDAD works this way | `cdad/docs/DOCS.md` (Methodology) |
| Set this up in my project | `README.md` |
| Run it on Kiro, Codex, or Copilot | `cdad/docs/DOCS.md` (Portability) |
| See which adapter I get for my ADE | `.claude/skills/cdad-bootstrap/SKILL.md` (step 0) or `README.md` → *ADE adapters* |

---

## Governed context — you own it, agents cannot write it once frozen

Pre-freeze (`cdad/.frozen` absent), `cdad/context/` and `cdad/adr/` are the one
exception: `cdad-bootstrap` writes them directly. See `cdad/.frozen` under
*Enforcement* below.

| File | Layer | Contains | Loads |
|---|---|---|---|
| `CHANGE-REQUEST.md` (project root) | — | Your standing request desk. The only input door | never |
| `SOURCE-BRIEF.*` (project root) | — | Your original design document, if one existed. Written once by `cdad-bootstrap`, then locked — not present if the context came entirely from conversation | never |
| `cdad/context/stack.md` | L0 | **The map**: stack table, components, topology, observability, dependency rules, drift signals, change log | on demand |
| `cdad/context/architecture.md` | L0 | Architecture in prose, module responsibilities | on demand |
| `cdad/context/constraints.md` | L0 | Hard limits. Kept short because it is always loaded | **always** |
| `cdad/context/principles.md` | L0 | Design principles in force | on demand |
| `cdad/context/solution-vision.md` | L0 | Purpose and non-goals | on demand |
| `cdad/context/glossary.md` | L0 | Terms whose meaning here differs from the usual | on demand |
| `cdad/adr/ADR-*.md` | L1 | Accepted decisions and their rationale | on demand |
| `cdad/adr/ADR-TEMPLATE.md` | L1 | Blank ADR | never |

## Development line — governed like architecture, but not L0

`backlog.md` (project root) is Epics, Stories, current focus, and next
work. Structural changes (new/removed Epic or Story, material scope or
acceptance-criteria change) go through `CHANGE-REQUEST.md` like an
architectural decision. Story status and focus updates during
already-approved implementation are direct edits — see *Backlog governance*
in `AGENTS.md`. Precedence: L0 → ADR → `backlog.md` → implementation; a
Story never overrides governed context.

## Staging — agents write here

| File | Contains | Loads |
|---|---|---|
| `cdad/proposals/` | Agent drafts awaiting your review. Delete when resolved | never |

## Instructions — how agents behave

A project has exactly one adapter, matching the ADE that executed its
bootstrap — see `.claude/skills/cdad-bootstrap/SKILL.md` (step 0). The rows
below marked *(Claude Code adapter)* or *(Kiro adapter)* are mutually
exclusive with each other in an installed project; both are shown here
because this source repository is the catalog, not an installed project.

| File | Contains | Loads |
|---|---|---|
| `AGENTS.md` | Portable core rules. Read natively by Kiro, Codex, and Copilot | **always** |
| `.claude/CLAUDE.md` *(Claude Code adapter)* | Imports `AGENTS.md`, adds skill routing | **always** |
| `.claude/rules/implementation.md` *(Claude Code adapter)* | Rules for `src/`, `tests/`, `lib/` | on matching files |
| `.claude/rules/infrastructure.md` *(Claude Code adapter)* | Rules for `infra/`, `deploy/`, CI | on matching files |
| `.kiro/steering/cdad-implementation.md` *(Kiro adapter)* | Kiro mirror of the above | on matching files |
| `.kiro/steering/cdad-infrastructure.md` *(Kiro adapter)* | Kiro mirror of the above | on matching files |
| `.github/copilot-instructions.md` *(Copilot adapter)* | Points Copilot at `AGENTS.md` and `cdad/` as the canonical source; no duplicated methodology | repository-wide, per GitHub Copilot |

## Procedures — load only when invoked

| File | Invoked when |
|---|---|
| `.claude/skills/cdad-bootstrap/SKILL.md` | first time populating `cdad/context/`, pre-freeze, right after cloning the kit |
| `.claude/skills/cdad-propose-change/SKILL.md` | processing a change request — architecture, context, conflict, or a development-line (Epic/Story) change |
| `.claude/skills/cdad-adr/SKILL.md` | a change was approved and needs recording (architecture/context changes only — a backlog-only change does not get an ADR) |
| `.claude/skills/cdad-audit/SKILL.md` | checking whether context still matches the code, or whether `backlog.md` is reconciled with defined Epics/Stories — also the scheduled sweep counterpart to the drift detector below |
| `.claude/skills/cdad-drift-response/SKILL.md` | a `CDAD DRIFT SIGNAL` fired, `cdad-audit` found a divergence, or you're asking whether an L3 change contradicts ratified architecture |

## Enforcement — costs zero context

| File | Does |
|---|---|
| `cdad/.frozen` | The regime marker. Absent = pre-freeze, `cdad/context/`/`cdad/adr/` are agent-writable. Present = governed, they're denied. Human-written only, via `cdad-freeze.sh`; versioned, not ignored |
| `cdad/scripts/cdad-freeze.sh` | Run by the Solution Designer to ratify: validates L0 has real content, then writes `cdad/.frozen` |
| `.claude/settings.json` | Denies writes to governance machinery unconditionally; registers both hooks below |
| `.claude/hooks/protect-l0.py` | `PreToolUse`. Regime-aware: blocks `cdad/context/`/`cdad/adr/`/`SOURCE-BRIEF.*` only once frozen; blocks machinery paths always, via shell too. Exit 2 |
| `.claude/hooks/detect-drift.py` | `PostToolUse`, governed regime only. Warns (never blocks) when a write matches the `cdad-drift-signals` block in `stack.md`. Deduplicated per session |
| `.kiro/permissions.yaml` | Kiro's declarative equivalent of the machinery-path deny (1.0+) |
| `.kiro/hooks/detect-drift.json` | Kiro mirror of `detect-drift.py` — same script, different trigger wiring |
| `cdad/scripts/cdad-check-stack.sh` | CI gate: an ADR without a map update fails the build; also checks referential integrity of ADR citations and warns if the drift-signals block is missing |
| `cdad/scripts/cdad-check-adapter.sh` | Deterministic validation of the ADE-adapter matrix: given a target ADE, asserts the installed files match exactly what that ADE should have and nothing else |
| `cdad/scripts/cdad-check-backlog.sh` | CI gate: fails on duplicate Epic/Story IDs or a status value outside the agreed vocabulary in `backlog.md`; warns on an Epic with no Stories yet |

## Human documentation — never loaded by any agent

| File | Contains |
|---|---|
| `INDEX.md` | This file |
| `README.md` | What CDAD is, setup, tool support |
| `cdad/docs/DOCS.md` | Governance model, layers, enforcement planes, Claude Code vs Kiro vs Codex, upgrading from CDAD v1 |

---

## The one flow that matters

```
CHANGE-REQUEST.md  ->  cdad/proposals/  ->  cdad/adr/ + cdad/context/stack.md
     you state intent      agent drafts           you approve and apply
     always writable       agent writable         blocked for agents
```

Everything else in this kit exists to make that flow cheap to run and hard to
skip.

---

## What loads on every single session

Only these. Everything else is on demand or never.

- `.claude/CLAUDE.md` (or `AGENTS.md` on Kiro, Codex, and Copilot)
- `AGENTS.md`
- `cdad/context/constraints.md`

If `/context` shows anything else from `cdad/`, something is importing more than
it should.
