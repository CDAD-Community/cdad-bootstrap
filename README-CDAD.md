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
- [Mandatory CDAD workspace scaffolding](#mandatory-cdad-workspace-scaffolding)
- [The problem](#the-problem)
- [Two files you will always touch](#two-files-you-will-always-touch)
- [The map](#the-map)
- [Changing something](#changing-something)
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

1. Downloads/clones CDAD Bootstrap into the project.
2. Checks whether `cdad/context/` still contains template placeholders.
3. Checks the project root for the design/source document.
4. If there is no document, or there is more than one candidate, asks instead of guessing.
5. If a document exists, asks you to confirm that it is complete and not a draft before using it.
6. If you say it is not complete, stops and waits for you to finish it.
7. Reads the confirmed source and maps it into the six governed context files.
8. Asks directly for information that the source does not answer.
9. Summarizes the resulting context and asks for a separate explicit confirmation that the six files accurately represent the design.
10. Only after confirmation, writes the completed context files.
11. Preserves your original source document as `SOURCE-BRIEF.*` at the project root when one was provided.
12. Tells you to review the result and run `cdad/scripts/cdad-freeze.sh` to ratify it.

Before the project is frozen, there is nothing ratified yet to protect, so the agent may write `cdad/context/` directly during this one-time bootstrap.

Freezing is a **human act**. It validates that the context no longer contains template placeholders and creates the `cdad/.frozen` marker. That marker switches the project into the governed regime, where governed paths become protected from direct agent writes.

See `.claude/skills/cdad-bootstrap/SKILL.md` for the detailed procedure.

From that point onward, the agent reads the governed context first before making implementation decisions.

The idea is simple:

> You and the agent define what you want to build and how it should be built; you confirm it; CDAD turns that agreed design into governed context; then AI develops under that context.

For the detailed procedures, see [INSTALLATION.md](INSTALLATION.md) and [USAGE.md](USAGE.md).

### 2. Manual installation

CDAD can also be installed manually by a human.

At minimum, the project must receive the CDAD workspace scaffolding defined below. Copy the shipped CDAD files/directories into the project root, preserve the required locations, merge the supplied `.gitignore` rather than overwriting an existing one, and then complete the governed context before freezing it.

See [INSTALLATION.md](INSTALLATION.md#manual-installation) for the complete manual procedure.

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

## Mandatory CDAD workspace scaffolding

When bootstrapping CDAD into a project, **the AI coding agent/ADE MUST create and preserve the following workspace structure exactly as defined below**:

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

### Scaffolding rules

- `AGENTS.md`, `CDAD-COMPLETION.md`, `CHANGE-REQUEST.md`, and `INDEX.md` MUST remain at the project root.
- The CDAD bootstrap README MUST be installed as `cdad/README.md`.
- CDAD-owned directories (`adr/`, `context/`, `docs/`, `proposals/`, `scripts/`) MUST remain under `cdad/`.
- The agent MUST NOT move, rename, duplicate, or redistribute CDAD artifacts outside this structure.
- The agent MUST preserve the host project's existing source structure and must not silently overwrite an existing file with the same name. Conflicts MUST be reported and resolved explicitly.
- ADE-specific files required by the host tool, such as `.claude/` or `.kiro/`, remain at their required locations and do not change the CDAD workspace contract.

This structure is a **CDAD bootstrap contract**, not merely a documentation convention.

---

## The problem

AI accelerates implementation. Humans govern context and architecture.

The failure mode is not necessarily bad code — agents can write individually reasonable code. The deeper failure mode is **architectural drift**: a sequence of individually defensible changes that collectively moves the solution somewhere nobody decided to go.

Drift is often invisible at the commit level and becomes visible only at the architecture level — precisely the level that is least likely to be reviewed continuously.

CDAD makes architecture and its surrounding context explicit, protected, and machine-readable. Changing governed decisions becomes a deliberate act rather than an accidental side effect of implementation.

---

## Two files you will always touch

Everything else in this kit is supporting machinery. These two live at the project root, not inside `cdad/`, so they remain easy to find:

| File | What it is | When you touch it |
| --- | --- | --- |
| **`SOURCE-BRIEF.*`** | Your original design: vision, architecture, stack, constraints, in your own words | Once, before or during setup |
| **`CHANGE-REQUEST.md`** | The front door for a requested change | Whenever a governed decision needs to change |

`cdad/context/stack.md` is the file you will read most often — the one-screen map of what the system is — but it is an output, not a file you should normally edit by hand. Approved changes reach it through `CHANGE-REQUEST.md`, never by silently editing the governed map.

---

## The map

`cdad/context/stack.md` answers **“what is this system?”** without opening the code.

It provides six views:

| # | View | Answers |
| ---: | --- | --- |
| 1 | Stack at a glance | What are we built on, and which ADR locked it? |
| 2 | Component map | What talks to what, over which protocol? |
| 3 | Deployment topology | Where does each piece run? |
| 4 | Observability | If it breaks at 3am, what do I look at? |
| 5 | Dependency rules | Which module may call which? |
| 6 | Map change log | One row per accepted ADR |

The map uses Markdown plus Mermaid so it renders in GitHub and IDEs. There is no image to regenerate and no diagram tool to keep licensed. Most importantly, it diffs like code: a pull request can show exactly what changed in the architecture.

A stack-table row without an ADR in its **Locked by** column is itself a finding: a decision entered the system without passing through governance.

---

## Changing something

There is one entry point. You do not hunt for the right governed file.

```text
CHANGE-REQUEST.md  ->  cdad/proposals/  ->  cdad/adr/ + cdad/context/stack.md
      you state intent      agent drafts           you approve and apply
      always writable       agent writable         governed/protected
```

Fill in the request block in `CHANGE-REQUEST.md` at the project root with what needs to change, why, trigger, scope, impact, risk, and priority.

Then ask the agent to process the change request.

The agent returns a complete proposal covering:

- current decision
- suggested change
- impact
- risk
- alternatives
- exact stack-map rows that change

You approve the proposal. The agent drafts the ADR. The approved change is then applied through the governed process.

**`cdad/proposals/` is the only directory under `cdad/` that an agent may write to as part of the governed change workflow.**

Routine implementation work does not need to enter this flow. If ordinary implementation repeatedly requires change requests, the constraints may be written too broadly and should be narrowed.

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
INDEX.md                        # map of every file — start here
AGENTS.md                       # portable core rules
CHANGE-REQUEST.md               # front door for change intent
SOURCE-BRIEF.*                  # original design, preserved after bootstrap
.gitignore                      # merge with the host project's existing file
│
cdad/
├── proposals/                  # agent drafts awaiting review
├── context/                    # L0 — governed context
│   ├── stack.md                # the six-view architecture map
│   ├── architecture.md
│   ├── solution-vision.md
│   ├── principles.md
│   ├── constraints.md          # always-in-context constraints
│   └── glossary.md
├── adr/                        # L1 — accepted decisions
├── scripts/
│   └── cdad-check-stack.sh     # CI gate
└── docs/                       # human reference
    └── DOCS.md                # methodology, portability, migration
│
.claude/
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
.kiro/steering/                 # Kiro steering/rules
```

### Why some files stay at the root

`.claude/` and `.kiro/` remain at the root because these tools discover their configuration at fixed locations. Moving them into `cdad/` can make the tools silently stop loading the intended rules and skills.

`AGENTS.md` remains at the root because Kiro and Codex read it by convention.

`CHANGE-REQUEST.md` and `SOURCE-BRIEF.*` remain at the root for human discoverability: they are the two files the Solution Designer needs to find quickly.

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

1. Copy `INDEX.md`, `AGENTS.md`, `CHANGE-REQUEST.md`, `.claude/` (including `.claude/CLAUDE.md`), `cdad/` (including `cdad/docs/` and `cdad/scripts/`), and `.kiro/` if you use Kiro into the project root.
2. Merge the kit's `.gitignore` into your existing `.gitignore`; do not overwrite an existing project file.
3. Run the `cdad-bootstrap` skill (for example, “bootstrap CDAD” or “set up CDAD”) instead of filling `cdad/context/` by hand.
4. If you prefer to author the context manually, start with `cdad/context/stack.md`. Leave a cell empty rather than guessing; an explicit unknown is preferable to an invented decision.
5. Adjust the `paths:` globs in `.claude/rules/` to match the host project's folder layout.
6. Wire `cdad/scripts/cdad-check-stack.sh` into CI against the default branch.
7. Run a session and inspect `/context`. Only the expected core rules and constraints should be loaded automatically.
8. Verify the guardrail: ask the agent to edit a protected context file such as `cdad/context/stack.md`. The write must be blocked by the applicable enforcement layer, not merely discouraged.
9. Review the completed context and run `cdad/scripts/cdad-freeze.sh` to ratify it.

### Upgrading to the two-regime model

If you are upgrading a project bootstrapped before the two-regime model existed, run:

```bash
./cdad/scripts/cdad-freeze.sh
```

immediately after the upgrade when `cdad/context/` already contains real content. Until the freeze marker exists, that context may remain agent-writable.

Full file map: [`INDEX.md`](INDEX.md) · Migration guidance: [`cdad/docs/DOCS.md#migrating-from-cdad-v1`](cdad/docs/DOCS.md#migrating-from-cdad-v1)

---

## Tool support

| Capability | Claude Code | Kiro | Codex |
| --- | --- | --- | --- |
| Portable core rules | via import | native | native |
| Conditional loading | `paths:` | `inclusion: fileMatch` | nested `AGENTS.md` |
| On-demand procedures | Skills | `inclusion: manual` | prompt |
| Deterministic write block | yes | `permissions.yaml` (1.0+) | config globs |
| Governed context + CI gate | yes | yes | yes |

Claude Code supports the complete adapter set. Kiro's `permissions.yaml` covers unconditional machinery paths declaratively; regime-conditional paths rely on the shared hook plus CI gate where needed. Codex keeps the write protection model but has fewer fine-grained conditional-loading controls.

Details and portability notes: [`cdad/docs/DOCS.md`](cdad/docs/DOCS.md#portability-claude-code-kiro-codex)

### Delete what you don't use

The kit ships with adapters for the supported tools. Keeping adapters nobody reads creates duplication and increases drift. **Prune unused adapters on day one.**

| You use | Keep | Delete |
| --- | --- | --- |
| Claude Code only | `AGENTS.md`, `.claude/` | `.kiro/` |
| Kiro only | `AGENTS.md`, `.kiro/` | `.claude/` |
| Codex only | `AGENTS.md` | `.claude/`, `.kiro/` |
| More than one | everything | nothing |

```bash
# Claude Code only
rm -rf .kiro

# Kiro only
rm -rf .claude

# Codex only
rm -rf .claude .kiro
```

**Never delete `AGENTS.md`.** It contains the portable core rules. Claude Code imports it; Kiro and Codex read it natively.

Deleting `.claude/` removes its local enforcement layer. On Kiro, `permissions.yaml` provides unconditional protection where supported; regime-conditional paths may rely on the shared hook and CI gate. On Codex, use nested `AGENTS.md` files when you need scoped rules:

```text
AGENTS.md
src/AGENTS.md
infra/AGENTS.md
```

---

## What you maintain

- `cdad/context/` and `cdad/adr/`: applied through the governed process and not directly written by an agent once frozen.
- `CHANGE-REQUEST.md`: your entry point whenever a governed decision needs to change.
- `SOURCE-BRIEF.*`: written once during bootstrap and preserved as the original source.
- `.claude/`, `.kiro/`, and `cdad/scripts/`: CDAD runtime/integration assets that normally require little change beyond path configuration.

---

## Requirements

Claude Code, Kiro, or Codex.

The protection hook needs `python3`, present by default on Linux and macOS. The CI gate needs `git` and `bash`.

---

## Evolution

CDAD is an evolving methodology focused on the governance of context in AI-assisted development. Future work may extend it across software solutions, cloud and infrastructure, agentic systems, documentation, and knowledge governance — while preserving the core principle:

> **Context is the Source of Truth.**

Related: [CDAD Framework](https://github.com/mgriott/context-driven-ai-development) — methodology, whitepapers, principles, and governance model.

---

## License

Creative Commons Attribution 4.0 International (CC BY 4.0).

You are free to share, adapt, and build upon this work, including commercially, provided appropriate attribution is given.

**Attribution:** Copyright © 2026 Moisés Griott. Maintained by **CDAD Community**.

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

---

**CDAD Community** · Context-Driven AI Development
