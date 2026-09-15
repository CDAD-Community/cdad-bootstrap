# CDAD Bootstrap

> **When context doesn't govern AI, AI governs the solution.**

The official starter kit for **Context-Driven AI Development (CDAD)** — governed context for AI-assisted software development.

**Context is the Source of Truth.**

Works with Claude Code, Kiro, Copilot and Codex · CC BY 4.0

🌐 **Languages**
- 🇺🇸 English (canonical)
- 🇪🇸 [Español](README-CDAD.es.md)

---

## Quick navigation

- [Usage flow](#usage-flow)
- [ADE adapters](#ade-adapters)
- [Mandatory CDAD workspace scaffolding](#mandatory-cdad-workspace-scaffolding)
- [Workspace hygiene](#workspace-hygiene)
- [The problem](#the-problem)
- [The two files you will always touch](#the-two-files-you-will-always-touch)
- [The map](#the-map)
- [Changing something](#changing-something)
- [Human Promotion Boundary](#human-promotion-boundary)
- [Backlog](#backlog)
- [Keeping the map honest](#keeping-the-map-honest)
- [Design principle](#design-principle)
- [Structure](#structure)
- [Context layers](#context-layers)
- [Getting started](#getting-started)
- [Tool support](#tool-support)
- [What you maintain](#what-you-maintain)
- [Requirements](#requirements)
- [Evolution](#evolution)
- [License](#license)

---

## Usage flow

### 1. Bootstrap the governed context

**Step 1 — Start with your design, if you have one.**

Leave your design document at the project root. Any name and any common format is acceptable: `.md`, `.txt`, Word, PDF, or equivalent.

There is no filename convention to follow. The document should be finished rather than a draft and should describe, as applicable:

- idea and goal
- vision
- requirements
- proposed architecture
- technology stack
- constraints
- development rules

Ideally, review the design with an LLM before bootstrapping to identify inconsistencies.

If you do not have a design document yet, skip this step. The agent can define the context with you through conversation.

**Step 2 — Tell your ADE/AI coding agent to bootstrap CDAD.**

For example:

> `clone CDAD Bootstrap and bootstrap the project`

The agent may be Claude Code, Kiro, Codex, Cursor, or another ADE capable of following the CDAD bootstrap procedure.

The bootstrap process:

1. Downloads/clones CDAD Bootstrap into the project — the source distribution is a catalog of every adapter, not something to install whole.
2. Detects the ADE actually executing the bootstrap and resolves the one adapter that matches it. If more than one ADE looks possible and the executing one can't be established with confidence, it asks instead of guessing — see [ADE adapters](#ade-adapters).
3. Installs the portable CDAD core plus only the resolved adapter, explicitly excluding the others.
4. Checks whether `cdad/context/` still contains template placeholders.
5. Checks the project root for the design/source document.
6. If there is no document, or there is more than one candidate, asks instead of guessing.
7. If a document exists, asks you to confirm that it is complete and not a draft before using it.
8. If you say it is not complete, stops and waits for you to finish it.
9. Reads the confirmed source and maps it into the six governed context files.
10. Asks directly for information that the source does not answer.
11. Summarizes the resulting context and asks for a separate explicit confirmation that the six files accurately represent the design.
12. Only after confirmation, writes the completed context files.
13. Preserves your original source document as `SOURCE-BRIEF.*` at the project root when one was provided.
14. Tells you to review the result and run `cdad/scripts/cdad-freeze.sh` to ratify it.

Before the project is frozen, there is nothing ratified yet to protect, so the agent may write `cdad/context/` directly during this one-time bootstrap.

Freezing is a **human act**. It validates that the context no longer contains template placeholders and creates the `cdad/.frozen` marker. That marker switches the project into the governed regime, where governed paths become protected from direct agent writes.

See `.claude/skills/cdad-bootstrap/SKILL.md` for the detailed procedure.

From that point onward, the agent reads the governed context first before making implementation decisions.

The idea is simple:

> You and the agent define what you want to build and how it should be built; you confirm it; CDAD turns that agreed design into governed context; then AI develops under that context.

For the detailed procedures, see [cdad/INSTALLATION.md](cdad/INSTALLATION.md) and [cdad/USAGE.md](cdad/USAGE.md).

### 2. Manual installation

CDAD can also be installed manually by a human.

At minimum, the project must receive the CDAD workspace scaffolding defined below. Copy the shipped CDAD files/directories into the project root, preserve the required locations, merge the supplied `.gitignore` rather than overwriting an existing one, and then complete the governed context before freezing it.

See [cdad/INSTALLATION.md](cdad/INSTALLATION.md#manual-installation) for the complete manual procedure.

### 3. Agent-assisted installation

An ADE can install CDAD from this repository when the user provides the repository URL or asks the agent to bootstrap CDAD.

The agent should:

1. Read this README first.
2. Identify the CDAD bootstrap contract and required workspace structure.
3. Inspect the host project before changing anything.
4. Detect source/design documents without guessing.
5. Report conflicts instead of overwriting them.
6. Create the required scaffolding.
7. Populate governed context through the bootstrap workflow.
8. Obtain explicit user confirmation before ratifying the context.
9. Run the freeze procedure when instructed.
10. Report exactly what was created, preserved, skipped, or requires human action.

See [AGENTS.md](AGENTS.md) for the agent-oriented contract.

---

## ADE adapters

CDAD ships a portable core plus one adapter per supported ADE. A target
project receives the portable core plus exactly the adapter matching the ADE
that is executing the bootstrap — never the whole catalog, never more than
one native adapter. The CDAD Bootstrap source distribution contains every
adapter because it is a catalog; installing all of them into a project is
not the intended flow.

**Portable core:** `AGENTS.md`, `README-CDAD.md`, `README-CDAD.es.md`, `SOURCE-BRIEF.*` (if a source document existed) at the project root, plus `cdad/` itself — carrying `INDEX.md`, `CHANGE-REQUEST.md`, `CDAD-COMPLETION.md`, `backlog.md`, `INSTALLATION.md`/`.es.md`, `USAGE.md`/`.es.md`, `context/`, `adr/`, `proposals/`, `docs/`, `scripts/`.

| Host ADE | Adapter | `.claude/` | `.kiro/` | `AGENTS.md` | `.copilot/copilot-instructions.md` |
| --- | --- | :---: | :---: | :---: | :---: |
| Claude Code | Claude | YES | NO | YES | NO |
| Kiro | Kiro | NO | YES | YES | NO |
| Codex | Portable/AGENTS | NO | NO | YES | NO |
| GitHub Copilot | Copilot | NO | NO | YES | YES |
| Other supported ADE | Explicit adapter only | only if mapped | only if mapped | per support | per support |
| Unknown ADE | Portable/unknown | NO | NO | do not guess | NO |

> **Known limitation:** GitHub Copilot's actual discovery path for
> repository-wide custom instructions is `.github/copilot-instructions.md`,
> per current GitHub documentation. CDAD deliberately keeps the file at
> `.copilot/copilot-instructions.md` instead, for naming consistency with
> `.claude/` and `.kiro/` — which means Copilot will not pick it up
> automatically at that path. Mirror it to `.github/copilot-instructions.md`
> as well if you need Copilot to load it on its own.

The adapter decision is based on the ADE actually executing the bootstrap —
never on the underlying model. A Claude model is not Claude Code; a GPT
model is not Codex; the Anthropic or OpenAI API alone is neither.

If the target project already shows files for more than one ADE (for
example a prior partial setup left both `.claude/` and `.kiro/`), the agent
does not pick one just because its files exist — it determines which ADE is
executing this bootstrap, or asks:

> Detected multiple possible ADE environments.
>
> CDAD requires selecting the ADE that is executing this bootstrap.
>
> Detected:
> - Claude Code
> - Kiro
>
> Please confirm which ADE is currently executing the CDAD bootstrap.

For an ADE with no native adapter, CDAD installs the portable core only and
reports plainly that no native adapter exists — it never invents one.

Re-running bootstrap never reintroduces an adapter a prior run explicitly
excluded, and never installs a second native adapter alongside the first.

Full algorithm: `.claude/skills/cdad-bootstrap/SKILL.md` (step 0). Validate
an installed project against this matrix with
`cdad/scripts/cdad-check-adapter.sh <claude|kiro|codex|copilot|unknown>`.

---

## Mandatory CDAD workspace scaffolding

When bootstrapping CDAD into a project, **the AI coding agent/ADE MUST create and preserve the following workspace structure exactly as defined below**:

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
    ├── INSTALLATION.md
    ├── INSTALLATION.es.md
    ├── USAGE.md
    ├── USAGE.es.md
    ├── adr/
    ├── context/
    ├── docs/
    ├── proposals/
    └── scripts/
```

### Scaffolding rules

- `AGENTS.md`, `README-CDAD.md`, `README-CDAD.es.md`, and `SOURCE-BRIEF.*` (when one exists) MUST remain at the project root — nothing else CDAD owns does.
- `INDEX.md`, `CHANGE-REQUEST.md`, `CDAD-COMPLETION.md`, and `backlog.md` MUST be generated directly under `cdad/` — never written to the project root and moved afterward.
- The CDAD bootstrap README MUST be installed as `cdad/README.md`.
- CDAD-owned directories (`adr/`, `context/`, `docs/`, `proposals/`, `scripts/`) MUST remain under `cdad/`.
- The agent MUST NOT move, rename, duplicate, or redistribute CDAD artifacts outside this structure.
- The agent MUST preserve the host project's existing source structure and must not silently overwrite an existing file with the same name. Conflicts MUST be reported and resolved explicitly.
- ADE-specific files required by the host tool — `.claude/`, `.kiro/`, or `.copilot/copilot-instructions.md` — remain at their required locations and do not change the CDAD workspace contract. Only the adapter matching the ADE executing the bootstrap is installed; see [ADE adapters](#ade-adapters).

This structure is a **CDAD bootstrap contract**, not merely a documentation convention.

---

## Workspace hygiene

**CDAD keeps governed development artifacts under `cdad/`. Only ADE
discovery/integration files and human-facing CDAD entry points remain at
the project root.**

The project root belongs to the user's project; `cdad/` belongs to CDAD
governance. Before this principle, CDAD's own governance files (`INDEX.md`,
`CHANGE-REQUEST.md`, `CDAD-COMPLETION.md`, `backlog.md`) sat directly at the
project root alongside the user's actual application — visual and cognitive
noise for both the developer and any agent scanning the root for what the
project actually is.

The test: *if I am a developer using CDAD, does the project root look like
my project, while `cdad/` clearly contains the CDAD governance machinery?*
The root should contain only:

- ADE discovery/integration files that genuinely require root/native placement (`.claude/`, `.kiro/`, `.copilot/copilot-instructions.md`, or `AGENTS.md` itself).
- CDAD's human-facing entry points (`README-CDAD.md`, `README-CDAD.es.md`, `SOURCE-BRIEF.*`).
- The user's own project files.

This is a structural change, not a cleanup step: the bootstrap process
generates these artifacts directly under `cdad/` — it never writes them to
the root and asks you to tidy up afterward, the way earlier versions asked
you to delete unused ADE adapters. See *ADE adapters* above for the same
selective-generation principle applied to tool integrations.

---

## The problem

AI accelerates implementation. Humans govern context and architecture.

The failure mode is not necessarily bad code — agents can write individually reasonable code. The deeper failure mode is **architectural drift**: a sequence of individually defensible changes that collectively moves the solution somewhere nobody decided to go.

Drift is often invisible at the commit level and becomes visible only at the architecture level — precisely the level that is least likely to be reviewed continuously.

CDAD makes architecture and its surrounding context explicit, protected, and machine-readable. Changing governed decisions becomes a deliberate act rather than an accidental side effect of implementation.

---

## The two files you will always touch

| File | What it is | When you touch it |
| --- | --- | --- |
| **`SOURCE-BRIEF.*`** (project root) | Your original design: vision, architecture, stack, constraints, in your own words | Once, before or during setup |
| **`cdad/CHANGE-REQUEST.md`** | The front door for a requested change | Whenever a governed decision or the development line needs to change |

`SOURCE-BRIEF.*` stays at the project root — the one CDAD artifact that is
purely yours to find quickly, never governance machinery. `CHANGE-REQUEST.md`
lives under `cdad/` with the rest of what it governs, but it is still the
single entry point you use constantly; it never gets harder to reach just
because it moved.

`cdad/context/stack.md` is the file you will read most often — the one-screen map of what the system is — but it is an output, not a file you should normally edit by hand. Approved changes reach it through `cdad/CHANGE-REQUEST.md`, never by silently editing the governed map.

---

## The map

`cdad/context/stack.md` answers **“what is this system?”** without opening the code.

It provides seven views:

| # | View | Answers |
| ---: | --- | --- |
| 1 | Stack at a glance | What are we built on, and which ADR locked it? |
| 2 | Component map | What talks to what, over which protocol? |
| 3 | Deployment topology | Where does each piece run? |
| 4 | Observability | If it breaks at 3am, what do I look at? |
| 5 | Dependency rules | Which module may call which? |
| 6 | Map change log | One row per accepted ADR |
| 7 | Drift signals | Which paths outside `cdad/` carry architectural weight, and what do they guard? |

The map uses Markdown plus Mermaid so it renders in GitHub and IDEs. There is no image to regenerate and no diagram tool to keep licensed. Most importantly, it diffs like code: a pull request can show exactly what changed in the architecture.

A stack-table row without an ADR in its **Locked by** column is itself a finding: a decision entered the system without passing through governance.

---

## Changing something

There is one entry point. You do not hunt for the right governed file.

```text
cdad/CHANGE-REQUEST.md  ->  cdad/proposals/  ->  you review + run one script  ->  cdad/adr/ + cdad/context/stack.md
      you state intent          agent drafts           the Human Promotion Boundary       governed/protected
      always writable           agent writable
```

Fill in the request block in `cdad/CHANGE-REQUEST.md` with what needs to change, why, trigger, scope, impact, risk, and priority.

Then ask the agent to process the change request.

The agent returns a complete proposal covering:

- current decision
- suggested change
- impact
- risk
- alternatives
- exact stack-map rows that change

You approve the proposal. The agent then stages a **promotion package** in `cdad/proposals/`: the ADR draft, the full text of every affected `cdad/context/` file, and an executable script:

```bash
bash cdad/proposals/apply-ADR-NNN-<slug>.sh
```

Review the proposal, the ADR, and the script, then run that one command yourself from the project root. The script lets you `view` the ADR text and the exact diff against current context, applies every affected file together only once you say `yes`, and is never executed by the agent — see [Human Promotion Boundary](#human-promotion-boundary).

**`cdad/proposals/` is the only directory under `cdad/` that an agent may write to as part of the governed change workflow.**

Routine implementation work does not need to enter this flow. If ordinary implementation repeatedly requires change requests, the constraints may be written too broadly and should be narrowed.

---

## Human Promotion Boundary

Preparing a governed change and promoting it are different acts, and CDAD
keeps them that way:

```text
PROPOSAL -> PROMOTION PACKAGE -> HUMAN REVIEW -> EXPLICIT HUMAN EXECUTION -> GOVERNED CHANGE
```

> **AI may prepare the change. AI may not autonomously promote the change.**

The agent can analyze impact, draft the proposal, draft the ADR, prepare the
affected `cdad/context/` files, and generate the promotion script. It cannot
execute that script, edit `cdad/adr/` or `cdad/context/` directly, or treat a
drafted proposal, ADR, or script as approval — each governed promotion needs
its own explicit decision from you, and approving one change never carries
over to the next.

The promotion script is a CDAD artifact in its own right, not a convenience
wrapper. It lives in `cdad/proposals/`, names the proposal and ADR it belongs
to in its header, asks for a final confirmation before it writes anything,
applies every file the change touches in one run, and fails clearly rather
than leaving the map half-updated. Full rule: `AGENTS.md` → *Human Promotion
Boundary*.

---

## Backlog

`cdad/backlog.md` is the development line: Epics, Stories, and the work
currently expected to be built. It answers "what exists, what's next,
what's blocked" — it is a planning artifact, not architecture, and never a
second source of truth beside `cdad/context/`.

```text
Governed Context / L0  ->  ADR  ->  cdad/backlog.md  ->  Implementation
```

A Story that contradicts governed context or an accepted ADR is a finding,
not a resolution — it never silently overrides the architecture.

**Governed the same way as everything else, with one routine carve-out:**

| Change | Path |
| --- | --- |
| New/removed Epic or Story, or a material scope/acceptance-criteria change | `cdad/CHANGE-REQUEST.md` → `cdad/proposals/` → Solution Designer decision |
| Story status, *Current Focus*, *Next Work*, *Blocked* updates during already-approved work | Direct edit — routine implementation, not a governed decision |

Before development work, the agent establishes the applicable Epic/Story
from `cdad/backlog.md`. If Epics/Stories are defined elsewhere but missing from
the backlog, that gap is reconciled through the normal change process — the
agent does not silently ignore them, and does not silently rewrite the
backlog to match either. If none are defined at all, the agent says so
explicitly rather than inventing business requirements.

`cdad/scripts/cdad-check-backlog.sh` deterministically checks structural
integrity — unique Epic/Story IDs, valid status values. Whether an
Epic/Story is real, current, and actually reflects the work being done is a
judgment call the `cdad-audit` skill makes, not something a script can
verify.

---

## Keeping the map honest

Four mechanisms, from weakest to strongest:

| Mechanism | What it does |
| --- | --- |
| `AGENTS.md` | States the rule: an ADR that does not declare its effect on the map is incomplete |
| Skill `cdad-adr` | Requires a before/after stack delta plus a change-log row |
| Skill `cdad-audit` | Verifies views against manifests, the real import graph, and alert rules |
| `cdad/scripts/cdad-check-stack.sh` | **Fails the build** when an ADR changes and the map does not |

The first three are instructions or procedures and therefore depend partly on model behavior. The fourth is deterministic enforcement.

---

## Design principle

Put each concern in the plane that can enforce it.

| Plane | Mechanism | Guarantee | Context cost |
| --- | --- | --- | --- |
| Control | `permissions.deny` + PreToolUse hook | Deterministic | Zero |
| Build | CI gate in `cdad/scripts/` | Deterministic, at merge | Zero |
| Instruction | `AGENTS.md`, `.claude/rules/` | Probabilistic | Tokens |
| Procedural | `.claude/skills/` | On demand | Zero until invoked |

**Anything enforceable in the control plane should not be expressed only as an instruction.**

For example, writing “AI must not modify architecture files” into the context window costs tokens every session and is only probabilistic. Blocking the write at the control plane holds deterministically and costs no model context.

Instructions remain necessary for work requiring judgment: whether a change is architectural, whether implementation contradicts context, or whether an abstraction is warranted.

The second principle follows: **the layer determines both who may edit and when it loads.** Only the rules and hard constraints should be loaded at session start; the broader knowledge base remains available on demand.

---

## Structure

```text
AGENTS.md                       # portable core rules
README-CDAD.md                  # this file — setup, tool support
README-CDAD.es.md               # Spanish mirror
SOURCE-BRIEF.*                  # original design, preserved after bootstrap
.gitignore                      # merge with the host project's existing file
│
cdad/                           # CDAD governance — everything below is generated here, not at root
├── README.md                   # project-facing operational README
├── INDEX.md                    # map of every file — start here
├── CHANGE-REQUEST.md           # front door for change intent
├── CDAD-COMPLETION.md          # durable bootstrap completion record
├── backlog.md                  # development line — Epics, Stories, current focus
├── INSTALLATION.md              # detailed setup procedures
├── INSTALLATION.es.md
├── USAGE.md                     # the normal development loop
├── USAGE.es.md
├── proposals/                  # agent drafts awaiting review
├── context/                    # L0 — governed context
│   ├── stack.md                # the seven-view architecture map
│   ├── architecture.md
│   ├── solution-vision.md
│   ├── principles.md
│   ├── constraints.md          # always-in-context constraints
│   └── glossary.md
├── adr/                        # L1 — accepted decisions
├── scripts/
│   ├── cdad-check-stack.sh     # CI gate
│   ├── cdad-check-adapter.sh   # validates the installed adapter matches the matrix
│   └── cdad-check-backlog.sh   # validates backlog.md structural integrity
└── docs/                       # human reference
    └── DOCS.md                # methodology, portability, migration
│
# below: the catalog of adapters this source ships — an installed project
# gets exactly ONE of these, resolved at bootstrap time (see ADE adapters)
│
.claude/                        # Claude Code adapter
├── CLAUDE.md
├── settings.json
├── hooks/protect-l0.py
├── rules/
└── skills/
    ├── cdad-bootstrap
    ├── cdad-propose-change
    ├── cdad-adr
    └── cdad-audit
│
.kiro/steering/                 # Kiro adapter
│
.copilot/copilot-instructions.md # GitHub Copilot adapter
```

### Why some files stay at the root

`.claude/`, `.kiro/`, and `.copilot/copilot-instructions.md` remain at the root because these tools discover their configuration at fixed locations. Moving them into `cdad/` can make the tools silently stop loading the intended rules and skills. Only the one matching your resolved adapter is actually installed — see [ADE adapters](#ade-adapters).

`AGENTS.md` remains at the root because Kiro, Codex, and Copilot read it by convention.

`README-CDAD.md`/`.es.md` remain at the root because they are the human-facing entry points — the first thing anyone opening the project should be able to find, not something buried under `cdad/`.

`SOURCE-BRIEF.*` remains at the root for the same reason: it is the Solution Designer's own original design, in their own words, and should stay as discoverable as the READMEs. Everything else CDAD owns — including `CHANGE-REQUEST.md`, now that it has one — lives under `cdad/`; see [Workspace hygiene](#workspace-hygiene).

---

## Context layers

| Layer | Contents | Policy | Loads |
| --- | --- | --- | --- |
| L0 | `cdad/context/` | Propose only | On demand, except `constraints.md` |
| L1 | `cdad/adr/` | Propose with review | On demand |
| L2 | `cdad/docs/` | Editable with review | Never automatically |
| L3 | `src/`, `tests/`, pipelines, IaC | Editable | As required |

---

## Getting started

1. Copy the portable core — `AGENTS.md`, `README-CDAD.md`, `README-CDAD.es.md`, and `cdad/` in full (including `cdad/docs/`, `cdad/scripts/`, and the `INDEX.md`/`CHANGE-REQUEST.md`/`CDAD-COMPLETION.md`/`backlog.md` already inside it) — into the project root, plus only the adapter matching your ADE: `.claude/` (including `.claude/CLAUDE.md`) for Claude Code, `.kiro/` for Kiro, `.copilot/copilot-instructions.md` for GitHub Copilot, or nothing extra for Codex. See [ADE adapters](#ade-adapters); do not copy the other adapters in "just in case."
2. Merge the kit's `.gitignore` into your existing `.gitignore`; do not overwrite an existing project file.
3. Run the `cdad-bootstrap` skill (for example, “bootstrap CDAD” or “set up CDAD”) instead of filling `cdad/context/` by hand — it performs step 1 above for you, deterministically.
4. If you prefer to author the context manually, start with `cdad/context/stack.md`. Leave a cell empty rather than guessing; an explicit unknown is preferable to an invented decision.
5. Adjust the `paths:` globs in `.claude/rules/` to match the host project's folder layout (Claude Code only).
6. Wire `cdad/scripts/cdad-check-stack.sh` and `cdad/scripts/cdad-check-backlog.sh` into CI against the default branch.
7. Run a session and inspect `/context`. Only the expected core rules and constraints should be loaded automatically.
8. Verify the guardrail: ask the agent to edit a protected context file such as `cdad/context/stack.md`. The write must be blocked by the applicable enforcement layer, not merely discouraged.
9. Verify the adapter: `cdad/scripts/cdad-check-adapter.sh <claude|kiro|codex|copilot>` confirms only the resolved adapter's files are present.
10. Review the completed context and run `cdad/scripts/cdad-freeze.sh` to ratify it.

### Upgrading to the two-regime model

If you are upgrading a project bootstrapped before the two-regime model existed, run:

```bash
./cdad/scripts/cdad-freeze.sh
```

immediately after the upgrade when `cdad/context/` already contains real content. Until the freeze marker exists, that context may remain agent-writable.

Full file map: [`cdad/INDEX.md`](cdad/INDEX.md) · Migration guidance: [`cdad/docs/DOCS.md#migrating-from-cdad-v1`](cdad/docs/DOCS.md#migrating-from-cdad-v1)

---

## Tool support

| Capability | Claude Code | Kiro | Codex | GitHub Copilot |
| --- | --- | --- | --- | --- |
| Portable core rules | via import | native | native | native (`AGENTS.md`) + `.github/copilot-instructions.md` pointer |
| Conditional loading | `paths:` | `inclusion: fileMatch` | nested `AGENTS.md` | none — repo-wide only |
| On-demand procedures | Skills | `inclusion: manual` | prompt | prompt |
| Deterministic write block | yes | `permissions.yaml` (1.0+) | config globs | no — CI gate only |
| Governed context + CI gate | yes | yes | yes | yes |

Claude Code supports the complete adapter set. Kiro's `permissions.yaml` covers unconditional machinery paths declaratively; regime-conditional paths rely on the shared hook plus CI gate where needed. Codex keeps the write protection model but has fewer fine-grained conditional-loading controls. GitHub Copilot reads repository-wide instructions from `.github/copilot-instructions.md` and agent instructions from `AGENTS.md`, per current GitHub documentation — note that CDAD's adapter file lives at `.copilot/copilot-instructions.md` instead, so it is not picked up automatically at Copilot's real path; see the note above. It gets no path-scoped loading and no deterministic write block beyond the CI gate — the Copilot adapter is intentionally thin and does not claim capabilities CDAD has not actually implemented for it.

Details and portability notes: [`cdad/docs/DOCS.md`](cdad/docs/DOCS.md#portability-claude-code-kiro-codex-copilot)

### Switching ADE later

Bootstrap already installs only the one adapter that matches your ADE — see
[ADE adapters](#ade-adapters). There is nothing to prune on day one. If the
project later moves to a different ADE (not merely adds a second one you use
occasionally), remove the old adapter and re-run bootstrap so the new one is
installed following the same rules a fresh install would follow:

```bash
# Moving to Claude Code
rm -rf .kiro
# then bootstrap resolves and installs .claude/

# Moving to Kiro
rm -rf .claude
# then bootstrap resolves and installs .kiro/

# Moving to Codex or Copilot
rm -rf .claude .kiro
# Copilot also needs .copilot/copilot-instructions.md; bootstrap installs it
```

**Never delete `AGENTS.md`.** It contains the portable core rules. Claude Code imports it; Kiro, Codex, and Copilot read it natively.

Deleting `.claude/` removes its local enforcement layer. On Kiro, `permissions.yaml` provides unconditional protection where supported; regime-conditional paths may rely on the shared hook and CI gate. On Codex or Copilot, use nested `AGENTS.md` files when you need scoped rules:

```text
AGENTS.md
src/AGENTS.md
infra/AGENTS.md
```

---

## What you maintain

- `cdad/context/` and `cdad/adr/`: applied through the governed process and not directly written by an agent once frozen.
- `cdad/backlog.md`: Epics/Stories change through `cdad/CHANGE-REQUEST.md` like an architectural decision; status and focus updates during routine implementation are direct edits.
- `cdad/CHANGE-REQUEST.md`: your entry point whenever a governed decision or the committed development line needs to change.
- `SOURCE-BRIEF.*`: written once during bootstrap and preserved as the original source, at the project root.
- Your resolved adapter (`.claude/`, `.kiro/`, or `.copilot/copilot-instructions.md`) and `cdad/scripts/`: CDAD runtime/integration assets that normally require little change beyond path configuration.

---

## Requirements

Claude Code, Kiro, Codex, or GitHub Copilot.

The protection hook (Claude Code) needs `python3`, present by default on Linux and macOS. The CI gate needs `git` and `bash`.

---

## Evolution

CDAD is an evolving methodology focused on the governance of context in AI-assisted development. Future work may extend it across software solutions, cloud and infrastructure, agentic systems, documentation, and knowledge governance — while preserving the core principle:

> **Context is the Source of Truth.**

Related: [CDAD Framework](https://github.com/mgriott/context-driven-ai-development) — methodology, whitepapers, principles, and governance model.

Community: [CDAD Community (ES)](https://cdad-community.github.io/es/) · [cdad-docs](https://github.com/CDAD-Community/cdad-docs)

---

## License

Creative Commons Attribution 4.0 International (CC BY 4.0).

You are free to share, adapt, and build upon this work, including commercially, provided appropriate attribution is given.

**Attribution:** Copyright © 2026 Moisés Griott. Maintained by **CDAD Community**.

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

---

**CDAD Community** · Context-Driven AI Development
