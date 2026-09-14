# CDAD — Reference Docs

This document is for humans. It is deliberately outside the agent's context
window: an agent does not need to understand CDAD to comply with it, and every
token spent explaining the methodology is a token not spent on the problem.

Three topics, one file — methodology, tool portability, and upgrading from v1.
None of it loads automatically in any tool, so merging costs nothing and saves
a file.

- [Methodology](#methodology) — the model itself: layers, enforcement planes, the change flow
- [Portability: Claude Code, Kiro, Codex, Copilot](#portability-claude-code-kiro-codex-copilot) — what each tool enforces and how to adapt
- [Migrating from CDAD v1](#migrating-from-cdad-v1) — file mapping and upgrade steps

---

## Methodology

> When context doesn't govern AI, AI governs the solution.

### The premise

AI accelerates implementation. Humans govern context and architecture.

The failure mode CDAD addresses is not bad code — agents write reasonable code.
It is **architectural drift**: a sequence of individually defensible changes that
collectively move the solution somewhere nobody decided to go. Drift is invisible
at the commit level and only visible at the architecture level, which is exactly
the level nobody is reviewing.

### Context layers

| Layer | Contents | Policy | Who edits |
|---|---|---|---|
| L0 | `cdad/context/` — the map, vision, architecture, principles, constraints | propose only | Solution Designer |
| L1 | `cdad/adr/` — accepted decisions | propose with review | Solution Designer |
| L2 | `docs/` — diagrams, specifications | editable with review | anyone |
| L3 | `src/`, `tests/`, pipelines, infrastructure code | editable | agents and humans |

The layer determines two things: **who may edit** and **when it loads into
context**. Earlier versions of CDAD only defined the first, which is what made
the model expensive — every layer loaded on every session regardless of
relevance.

### The three enforcement planes

CDAD's guarantees do not come from asking the agent nicely. They come from
putting each concern in the plane that can actually enforce it.

| Plane | Mechanism | Guarantee | Cost per session |
|---|---|---|---|
| Control | `permissions.deny`, PreToolUse hook | Deterministic | Zero context |
| Build | `cdad/scripts/cdad-check-stack.sh` in CI | Deterministic, after the fact | Zero context |
| Instruction | `AGENTS.md`, `.claude/rules/` | Probabilistic | Tokens |
| Procedural | `.claude/skills/` | On demand | Zero until invoked |

The rule: **anything that can be enforced in the control plane must not be
written as an instruction.** An instruction is a request the model may decline
under pressure; a deny rule is not. Writing "AI must not modify L0 files" into
context is strictly worse than blocking the write — it costs tokens every
session and holds only probabilistically.

Instructions remain necessary for everything that requires judgment: whether a
change is architectural, whether code contradicts context, whether an
abstraction is warranted. No permission rule can decide those.

The drift detector (`detect-drift.py`, see [Drift detection](#drift-detection))
lives in the control plane too — a deterministic hook, zero tokens per
session — but its output is advisory, not a block. It is not a fifth plane; it
extends the control plane's reach from paths to decisions without making L3
governed territory, since L3 stays free by design.

### What lives where

| Concern | Location | Loads |
|---|---|---|
| Non-negotiable behavioral rules | `AGENTS.md`, imported by `.claude/CLAUDE.md` | always |
| Hard project constraints | `cdad/context/constraints.md`, imported by `.claude/CLAUDE.md` | always |
| Rules for one area of the codebase | `.claude/rules/*.md` with `paths:` | when touching matching files |
| Proposal, ADR, audit procedures | `.claude/skills/*/SKILL.md` | when invoked |
| The stack and architecture map | `cdad/context/stack.md` | when the task needs it |
| Architecture prose, vision, principles | `cdad/context/` | when the task needs them |
| Accepted decisions | `cdad/adr/` | when the task needs them |
| Change requests | `cdad/CHANGE-REQUEST.md` | never |
| Agent drafts awaiting review | `cdad/proposals/` | never |
| This document | `cdad/docs/` | never |

### The change flow

Governance fails when the compliant path is harder than the workaround. CDAD
therefore has exactly one entry point for change, and it is a plain markdown
file that is always in the same place.

```
cdad/CHANGE-REQUEST.md  ->  cdad/proposals/  ->  cdad/adr/ + cdad/context/
     Designer states          agent drafts         Designer applies
     intent, 4 lines          a full proposal      after approval
```

The asymmetry is the mechanism: `cdad/proposals/` is the only directory under
`cdad/` an agent can write to. An agent that wants to change the architecture
has exactly one move available — write a reviewable draft. There is no path
where it edits the architecture and no path where it silently skips review,
because the alternative is blocked at the permission layer rather than
discouraged in prose.

This also removes the friction that kills governance models in practice. The
Designer does not need to remember which of six files to edit, or how to format
an ADR. They write four lines in one known location.

### Governance model

**Human approval required for:** architectural direction, paradigm, module
boundaries, integration strategy, deployment strategy, data model, frameworks,
runtimes, cloud platform and managed services, and any change to L0.

**Agents may:** read and analyze context, detect inconsistencies, propose
changes, and generate implementation aligned with the governed context.

**The golden rule:** an agent may suggest, analyze, and accelerate. It may not
redefine architecture without explicit approval from the Solution Designer.

### Two regimes

`cdad/context/`, `cdad/adr/`, and `SOURCE-BRIEF.*` are not protected
unconditionally — they are protected only once something has actually been
ratified. Enforcement is split into two regimes, discriminated by
the marker file `cdad/.frozen`:

| Regime | Condition | Those paths |
|---|---|---|
| Pre-freeze | `cdad/.frozen` absent | writable by the agent |
| Governed | `cdad/.frozen` present | denied |

This exists because the alternative — one unconditional deny — is wrong at the
moment a project is created, when the six context files are still template
placeholders and there is nothing ratified to protect yet. `cdad-bootstrap`
writes them directly in this window; the Solution Designer then runs
`cdad/scripts/cdad-freeze.sh`, which refuses to ratify placeholder content and
writes the marker only once L0 is real. From that point the project is
governed and those paths are read-only for agents again.

Governance machinery — `AGENTS.md`, `.claude/settings.json`, `.claude/hooks/`,
`cdad/CHANGE-REQUEST.md`, the Kiro equivalents, and the marker itself — has no
regime exception. It is denied in both regimes, always: an agent never drafts
its own directives or its own enforcement.

### The map

`cdad/context/stack.md` is the one page that answers "what is this system" in a
single screen: the stack table, the component map, the deployment topology, the
observability view, the dependency rules, and the change log. It is written in Markdown and Mermaid, so it renders in
GitHub and any IDE without an image to regenerate and without a diagram tool to
keep licensed.

It is governed at L0 and updated in the same change as the ADR that approves the
architectural decision. Three mechanisms hold that line, in descending strength:

1. **CI gate** — `cdad/scripts/cdad-check-stack.sh` fails the build when an ADR
   changes and the map does not.
2. **ADR procedure** — the `cdad-adr` skill requires a stack map delta section
   with before/after rows; an ADR without one is incomplete.
3. **Audit** — the `cdad-audit` skill checks each map claim against dependency
   manifests, the real import graph, and deployment definitions.

A row in "Stack at a glance" with no ADR in its "Locked by" column is a finding
in its own right: a decision that entered the system without passing through
governance.

### Context freshness

A stale context file is worse than a missing one — it produces confident,
consistent, wrong behavior across every agent in the project.

Context freshness is therefore an operational responsibility, not a
documentation chore. Run the `cdad-audit` skill before releases and after large
merges. When implementation and context diverge, the Solution Designer decides
which one is wrong; the agent is not permitted to assume the code is right.

### Drift detection

The control plane above protects paths, L3 is free by design, and a change
there can contradict a ratified decision without touching any denied path —
editing `docker-compose.yml` can silently override a datastore decision locked
in `stack.md`. Drift detection extends the control plane from paths to
decisions without making L3 governed territory.

**One engine, two triggers.** A `cdad-drift-signals` block declared inside
`cdad/context/stack.md` (L0, human-edited only) names the paths outside the
governed tree that carry architectural weight. A single skill,
`cdad-drift-response`, is the only path from a detected divergence to a
proposal draft — it never runs unratified.

1. **Write-time.** `detect-drift.py`, a `PostToolUse` hook, compares each
   write against the signals block and warns through stderr — advisory, never
   blocking, deduplicated per session so a category warns once per session
   rather than once ever.
2. **Sweep.** `cdad-audit` reads the same signals block and sweeps every
   matching file, not just what changed this session, then hands any
   divergence to `cdad-drift-response` instead of drafting in its own format.

Operates only under the governed regime — pre-freeze there is nothing ratified
yet to contradict. Shell mutations of L3 are not detected by the hook (its
`tool_input` is a command string, not a path); the CI gate is the net for
that case, same as it is for the regime-conditional write block above.

### Backlog governance

`cdad/backlog.md` is the development line: Epics, Stories, current focus,
and next work. It is a development-planning artifact, not architecture, and
it must never become a second source of truth beside `cdad/context/`.

**Precedence:**

```
Governed Context / L0
        v
ADR / governed decisions
        v
cdad/backlog.md
        v
Implementation work
```

A Story that contradicts governed context or an accepted ADR is a finding,
not a resolution. It is surfaced through the normal change process, the same
way architectural drift is — a Story never silently overrides architecture.

**Two kinds of backlog change, two very different bars:**

| Change | Governed how |
|---|---|
| New/removed Epic or Story, or a material scope/acceptance-criteria change | `cdad/CHANGE-REQUEST.md` → `cdad/proposals/` → Solution Designer decision (`cdad-propose-change`, form 4) |
| Story status, *Current Focus*, *Next Work*, *Blocked* updates during already-approved implementation | Direct edit — routine implementation, not a governed decision |

This mirrors the routine-implementation carve-out CDAD already applies to
architecture ("routine implementation does not require a change request") —
extended to development-line tracking instead of invented as a separate
rule. The distinction between "material" and "routine" requires judgment a
hook cannot make deterministically, so — deliberately, unlike `cdad/context/`
and `cdad/adr/` — `cdad/backlog.md` is **not** in `permissions.deny` or
blocked by `protect-l0.py`. Its protection is instruction-plane (`AGENTS.md`,
the `cdad-propose-change` and `cdad-audit` skills) plus one deterministic
backstop: `cdad/scripts/cdad-check-backlog.sh` fails the build on duplicate
Epic/Story IDs or a status value outside the agreed vocabulary, and warns on
an Epic with no Stories yet. What it cannot check — whether an Epic/Story is
real, current, and actually reflects the work being done, or whether a
structural change actually went through `cdad/CHANGE-REQUEST.md` — is the
`cdad-audit` *Backlog reconciliation* pass's job, not the script's.

**Reconciling existing Epics/Stories.** When Epics or Stories are already
defined somewhere (a requirements doc, an issue tracker, prior conversation)
but not yet reflected in `cdad/backlog.md`, that is a gap to close through
`cdad-propose-change`, not something to silently ignore or silently rewrite
the backlog to match. When none are defined at all, say so explicitly and
ask whether the development line should be defined — never invent business
Epics/Stories and present them as user-defined requirements; a proposed one
stays labeled `Status: Proposed` until accepted.

**Why not just another ADR-governed file?** An ADR records a decision that,
once made, rarely changes shape again. A Story is expected to move through
statuses constantly as normal work happens — routing every status flip
through `cdad/CHANGE-REQUEST.md` would make the backlog too expensive to keep
current, and a stale backlog is worse than no backlog (same failure mode as
stale context). The bar is calibrated to what actually needs a human
decision: *what* the project commits to building, not *how far along* it is.

### Operational boundary

CDAD does not slow implementation down. It prevents accidental architectural
change. Everything under L3 stays fully editable, and the majority of day-to-day
work never touches the governance path at all.

If CDAD is producing friction on routine work, the constraints are written too
broadly — narrow them rather than working around them.

---

## Portability: Claude Code, Kiro, Codex, Copilot

CDAD v2 separates **content** from **mechanism**. The governed context under
`cdad/` is plain markdown and is fully portable. What differs per tool is how
that content is loaded and how the L0 protection is enforced.

Nothing in `cdad/` needs to change to move between tools. Only the adapter does.
A project installs exactly one adapter, resolved at bootstrap time from the
ADE actually executing it — see the ADE adapter matrix in `README.md` and in
`.claude/skills/cdad-bootstrap/SKILL.md` (step 0).

### Compatibility matrix

| Capability | Claude Code | Kiro | Codex | GitHub Copilot |
|---|---|---|---|---|
| Always-loaded instructions | `.claude/CLAUDE.md` | `AGENTS.md`, or steering `inclusion: always` | `AGENTS.md` | `AGENTS.md` + `.github/copilot-instructions.md` |
| Reads `AGENTS.md` natively | no — imports it | yes | yes | yes |
| Path-scoped rules | `.claude/rules/` + `paths:` | `.kiro/steering/` + `inclusion: fileMatch` | nested `AGENTS.md` only | none documented |
| On-demand procedures | Skills | steering `inclusion: manual` / `auto` | prompt or custom command | prompt |
| Declarative file-write blocking | `permissions.deny` | not equivalent | `[permissions.*.filesystem]` globs | not equivalent |
| Programmatic pre-tool block | PreToolUse hook | agent hooks (different model) | hooks / sandbox | none documented |
| Governed context in `cdad/` | works | works | works | works |
| CI gate (`cdad/scripts/`) | works | works | works | works |

**Short version:** Claude Code runs everything. Kiro runs everything except the
deterministic write block, which it approximates. Codex runs the content and the
write block, but loses conditional loading — its instruction file is
all-or-nothing. GitHub Copilot is the thinnest adapter: content and the CI
gate work, with neither conditional loading nor a deterministic write block —
CDAD does not claim Copilot capabilities beyond what current GitHub
documentation actually supports (`.github/copilot-instructions.md` for
repository-wide instructions, `AGENTS.md` for agent instructions).

### Claude Code

Native target. `.claude/CLAUDE.md` imports `AGENTS.md` and adds the
Claude-specific layer: skill routing and a note that permission denials are by
design.

Verify with `/context`: only `.claude/CLAUDE.md`, `AGENTS.md`, and
`constraints.md` should appear under memory files.

### Kiro

Kiro reads `AGENTS.md` from the workspace root automatically, so the portable
core loads with no adapter at all. Note that `AGENTS.md` in Kiro does not
support inclusion modes — it is always included.

The path-scoped rules are mirrored in `.kiro/steering/` using
`inclusion: fileMatch` with a `fileMatchPattern`. Kiro accepts one pattern per
file, so a rule covering several globs becomes several steering files.

Since Kiro IDE 1.0, declarative permissions exist in `.kiro/permissions.yaml`
(`deny` wins over `ask`/`allow`), covering the unconditional machinery paths —
`AGENTS.md`, `.claude/**`, `.kiro/settings|steering|hooks/**`,
`cdad/.frozen` — the same way `permissions.deny` does for Claude Code.

What `permissions.yaml` cannot express is the two-regime condition on
`cdad/context/` and `cdad/adr/`: whether they are writable depends on whether
`cdad/.frozen` exists, and a static config file has no way to test that. Those
two paths still fall back to the CI gate: `cdad/scripts/cdad-check-stack.sh`
plus a branch rule requiring review on `cdad/**` catches what reaches a pull
request. (The drift detector, `detect-drift.py`, is different: it is advisory
rather than a write block, so it mirrors cleanly to Kiro as
`.kiro/hooks/detect-drift.json` — see the Drift detection section.)

Known issue: global steering in `~/.kiro/steering/` has had reports of
`fileMatch` not triggering. Keep CDAD steering in the workspace, not global.

### Codex

Codex reads `AGENTS.md` from the global config directory, the project root, and
nested directories, with more local files taking priority. The portable core
loads with no adapter.

Two adjustments matter:

**Conditional loading does not exist.** Codex has no `paths:` equivalent. The
closest approximation is nested `AGENTS.md` files that apply when Codex works in
that subtree:

```
AGENTS.md              # portable core
src/AGENTS.md          # implementation rules
infra/AGENTS.md        # infrastructure rules
```

This is coarser than path globs but preserves the principle: rules load near the
code they govern rather than all at once.

**Size cap.** Codex caps project docs at `project_doc_max_bytes`, 32 KiB by
default. CDAD v2's core is far under that. CDAD v1 was not obviously safe.

**Write protection** is available through filesystem permission globs in
`~/.codex/config.toml`:

```toml
[permissions.cdad.filesystem]
"cdad/context/**" = "deny"
"cdad/adr/**" = "deny"
```

Combine with `sandbox_mode` and `writable_roots` for a harder boundary. Verify
against the current Codex config reference — this surface has been changing
quickly.

### GitHub Copilot

Copilot reads two files per current GitHub documentation: repository-wide
instructions from `.github/copilot-instructions.md`, and agent instructions
from `AGENTS.md`. The portable core loads through `AGENTS.md` with no other
adapter machinery beyond that single pointer file.

**Conditional loading does not exist.** `.github/copilot-instructions.md` is
repository-wide only — there is no documented path-scoped equivalent to
`paths:` or `inclusion: fileMatch`.

**Write protection** has no declarative or programmatic equivalent in the
Copilot adapter today. `cdad/scripts/cdad-check-stack.sh` plus a required
review on `cdad/**` is the only backstop, the same fallback Kiro uses for the
two regime-conditional paths.

The adapter file itself must stay thin: it points at `AGENTS.md` and `cdad/`
as the canonical source rather than restating CDAD methodology, so there is
never a second copy of the rules to drift out of sync with the first.

### If your team uses more than one ADE

Bootstrap itself always resolves to exactly one adapter per run — see the ADE
adapter matrix. If a team deliberately wants more than one adapter present at
once (some engineers on Claude Code, others on Copilot), add the extra
adapter by hand; bootstrap will not do this for you, and re-running it will
not add a second native adapter on its own either.

Keep `AGENTS.md` as the single source for the core rules. Never restate a rule
in `.claude/CLAUDE.md` or `.github/copilot-instructions.md` that already lives
in `AGENTS.md` — that duplication is exactly the defect v2 was built to
remove.

The path-scoped rule files are the one place duplication is unavoidable,
since `.claude/rules/` and `.kiro/steering/` use incompatible front matter. They
are short and change rarely.

### If you use only one

Bootstrap already installs only the adapter matching the ADE that executed
it — there is nothing to prune. If the project moves to a different ADE
later, see *Switching ADE later* in the README for the exact commands and
the caveats: deleting `.claude/` removes the deterministic enforcement
layer, and Codex/Copilot need nested `AGENTS.md` files to approximate
path-scoped rules.

`AGENTS.md` is never deleted — it is the core every tool reads.

---

## Migrating from CDAD v1

### What changed and why

v1 was correct as a methodology and expensive as an implementation. Every file
loaded on every session, whether relevant or not, and the same rules were
restated across four files.

| Problem in v1 | Fix in v2 |
|---|---|
| `AGENTS.md` ordered the agent to read 9 files at session start | Nothing is read at startup; content loads when relevant |
| L0 file list repeated 6 times across 4 files | Stated once, in `.claude/CLAUDE.md` |
| `Proposed Architecture Change` template duplicated in 3 files | One copy, in the `cdad-propose-change` skill |
| L0–L3 table in both `governance.md` and `project-context.md` | One copy, in the Methodology section above |
| 518 lines of methodology vs 263 lines of actual project context | Methodology moved out of the context window entirely |
| L0 protection written as prose the model may ignore | `permissions.deny` plus a PreToolUse hook |

Always-loaded context drops from roughly 826 lines to roughly 80.

### File mapping

| v1 | v2 |
|---|---|
| `cdad/AGENTS.md` | `.claude/CLAUDE.md` (rules) + this document's Methodology section (rationale) |
| `cdad/ai-rules.md` | `.claude/CLAUDE.md` + `.claude/skills/cdad-propose-change/` |
| `cdad/governance.md` | Methodology section above |
| `cdad/guardrails.md` | `.claude/settings.json` + `.claude/rules/` |
| `cdad/project-context.md` | Methodology section above |
| `cdad/context/*` | unchanged in purpose; trimmed and marked read-only |
| *(new)* | `cdad/context/stack.md` — the visual stack and architecture map |
| *(new)* | `cdad/CHANGE-REQUEST.md` — the single entry point for changes (root in v2, moved under `cdad/` in v2.1) |
| *(new)* | `cdad/proposals/` — agent-writable staging area |
| *(new)* | `cdad/INDEX.md` — map of every file (root in v2, moved under `cdad/` in v2.1) |
| *(new)* | `SOURCE-BRIEF.*` (project root) — the original design document, preserved by `cdad-bootstrap` |
| *(new, v2.1)* | `cdad/backlog.md` — the development line: Epics, Stories, current focus |
| *(new, v2.1)* | `cdad/CDAD-COMPLETION.md` — durable bootstrap completion record |
| `cdad/adr/*` | unchanged; template added |

### Steps

1. Copy `.claude/` (includes `.claude/CLAUDE.md`) and `cdad/` (includes
   `cdad/docs/`) into your project root.
2. Port your real content into the files under `cdad/context/`. Copy from your
   v1 files; the governed content itself did not change.
3. Fill in `cdad/context/stack.md`. This file is new in v2 and has no v1
   equivalent. Set the "Locked by" column to the ADR that made each decision;
   blanks are findings, not omissions.
4. Delete `cdad/AGENTS.md`, `ai-rules.md`, `governance.md`, `guardrails.md`, and
   `project-context.md`.
5. Adjust the `paths:` globs in `.claude/rules/` to match your folder layout.
   They ship with `src/`, `tests/`, `infra/`, `deploy/`.
6. Start a session and run `/context`. Confirm `.claude/CLAUDE.md` appears under
   memory files and that nothing from `cdad/docs/` or `.claude/skills/` is
   loaded.
7. Wire `cdad/scripts/cdad-check-stack.sh` into CI against your default branch.
8. Verify the protection holds: ask the agent to edit
   `cdad/context/architecture.md`. It must be blocked, not merely reluctant.

### If you use other agents too

v2 ships this way already: `AGENTS.md` holds the portable core and
`.claude/CLAUDE.md` imports it. Kiro and Codex read `AGENTS.md` natively, so
they pick up the core with no adapter. See the Portability section above for
what each tool does and does not enforce.

If you only ever use Claude Code, you can inline `AGENTS.md` into
`.claude/CLAUDE.md` and delete it — but the indirection costs nothing and keeps
the door open.

### Verifying the token saving

Run `/context` before and after. The `Memory files` section shows what loaded
and what it costs. If you still see files from `cdad/` other than
`constraints.md`, something is importing more than it should.

