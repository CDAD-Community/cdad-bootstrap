# CDAD — GitHub Copilot integration

> **Known limitation:** GitHub Copilot's actual, documented discovery path
> for repository-wide custom instructions is `.github/copilot-instructions.md`
> — Copilot does not read `.copilot/copilot-instructions.md` automatically.
> This project deliberately keeps the file at `copilot/` instead, for
> consistency with the other adapter directories (`.claude/`, `.kiro/`)
> being named after the tool. That trade-off is a project decision, not a
> CDAD limitation: automatic loading does not happen at this path today: if
> you need Copilot to actually pick these instructions up on its own,
> mirror this file to `.github/copilot-instructions.md` as well.

This repository is governed by **CDAD (Context-Driven AI Development)**. The
full agent contract lives in `AGENTS.md` at the repository root — read it
before proposing or making any change. This file adds only what Copilot
needs beyond that; it is not a second copy of the methodology, and it
should never become one.

## Read first

- `AGENTS.md` — the portable CDAD contract: mission, required workspace,
  bootstrap behavior, governed regime, change process, non-negotiable
  rules.
- `cdad/context/constraints.md` — hard limits that apply to every change.
- `cdad/INDEX.md` — map of every file in this kit.

## What Copilot must not do

`cdad/context/`, `cdad/adr/`, `cdad/CHANGE-REQUEST.md`, and `SOURCE-BRIEF.*`
are governed paths owned by the Solution Designer. CDAD has no deterministic
write-block adapter for Copilot today — this is an instruction, not an
enforced guardrail, so treat it as binding anyway. To propose a change,
write a draft under `cdad/proposals/` and follow the change process in
`AGENTS.md`; never edit the governed paths directly, and never work around
this by renaming, duplicating, or editing them through another path.

## Procedures

CDAD's step-by-step procedures (bootstrap, propose a change, record an ADR,
audit context) are described at a high level in `AGENTS.md` — follow those
numbered steps directly. Copilot has no on-demand procedure loader
equivalent to a Claude Code skill, so there is no separate procedure file to
fetch here. When a step calls for judgment `AGENTS.md` doesn't resolve, ask
the Solution Designer rather than improvising.
