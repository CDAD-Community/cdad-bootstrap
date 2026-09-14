---
name: cdad-bootstrap
description: Detect the host ADE, install only its CDAD adapter, then populate cdad/context/ for the first time in a new project. Use when the user says to set up CDAD, bootstrap CDAD, initialize CDAD, or has just cloned CDAD Bootstrap into a project and cdad/context/ still holds template placeholders. Checks the project root for an existing solution document, confirms with the Solution Designer that it is finished rather than a draft, asks for whatever it does not answer, and drafts the six context files plus a permanent SOURCE-BRIEF at the project root for review before anything is written.
---

# Bootstrap the governed context

`cdad/context/` ships as a template — angle-bracket placeholders and empty
table rows, not real answers. This skill turns those placeholders into the
project's actual context, confirmed by the Solution Designer before anything
is written.

## 0. Detect the host ADE and resolve the adapter

Do this before touching the filesystem, and before step 1. Two separate
questions: which ADE is executing this bootstrap, and which adapter does
that resolve to.

CDAD Bootstrap ships a portable core (`AGENTS.md`, `INDEX.md`, `backlog.md`,
`CHANGE-REQUEST.md`, `CDAD-COMPLETION.md`, `cdad/`) plus one adapter per
supported ADE. The source repository carries every adapter — it is a
catalog, not a package to install whole. A target project receives the
portable core plus exactly the adapter matching the ADE actually executing
the bootstrap, never the whole catalog.

| Host ADE | Adapter | `.claude/` | `.kiro/` | `AGENTS.md` | `.github/copilot-instructions.md` |
|---|---|---|---|---|---|
| Claude Code | Claude | YES | NO | YES | NO |
| Kiro | Kiro | NO | YES | YES | NO |
| Codex | Portable/AGENTS | NO | NO | YES | NO |
| GitHub Copilot | Copilot | NO | NO | YES | YES |
| Other supported ADE | Explicit adapter only | only if mapped | only if mapped | per support | per support |
| Unknown ADE | Portable/unknown | NO | NO | do not guess | NO |

**Detect from the execution environment, never from the model.** A Claude
model is not Claude Code; a GPT model is not Codex; the API alone is
neither. The signal is which CLI/IDE is actually running this bootstrap
session — for Claude Code that is self-evident from the runtime you are in.

**Be conservative when more than one ADE looks possible** — for example the
target repo already has both `.claude/` and `.kiro/` from a prior partial
setup. Do not pick one merely because its files exist; that tells you what
was installed before, not what is executing now. If the executing ADE
cannot be established with confidence, stop and ask, in this shape:

> Detected multiple possible ADE environments.
>
> CDAD requires selecting the ADE that is executing this bootstrap.
>
> Detected:
> - Claude Code
> - Kiro
>
> Please confirm which ADE is currently executing the CDAD bootstrap.

Never install more than one native adapter merely because more than one is
present in the source or already exists in the target repo.

**Unknown ADE.** If the executing ADE has no row above and none has been
explicitly mapped for it, install the portable core only. Do not invent an
adapter. Report plainly that no native adapter exists for it, and that it
falls back to `AGENTS.md` where it is capable of reading that natively.

**Re-running bootstrap.** Before writing anything, check what is already
installed. If an adapter is present, that is the resolved adapter — do not
switch it without the user saying so, and do not add a second one. If a
prior bootstrap deliberately excluded an adapter, a re-run must not
reintroduce it.

Once resolved, note the detected ADE, the resolved adapter, the files this
will install, and the adapters this will exclude — this becomes part of the
report after step 6. Then continue to step 1.

## 1. Establish the regime

Two independent questions. Cross them before doing anything.

| `cdad/context/` has real content? | `cdad/.frozen` exists? | Action |
|---|---|---|
| No | No | Normal case. Proceed to step 2. |
| No | Yes | Anomaly — freeze validates content before writing the marker, so this should be impossible. Stop. Report the inconsistency. Do not guess which side is right. |
| Yes | Yes | Normal governed state. Bootstrap does not apply. Offer `cdad-audit` instead. |
| Yes | No | **Migration case.** Say exactly: "cdad/context/ is populated but cdad/.frozen is absent. If this project was already governed before this version of CDAD, run cdad/scripts/cdad-freeze.sh now rather than treating this as a fresh bootstrap." Stop. Do not offer to overwrite it. |

"Real content" means not placeholders like `<layered / hexagonal / ...>` or
empty table rows.

## 2. Look for an existing solution document

Look at the project root only — not subdirectories, not the rest of the repo.
Anything there that isn't part of the kit itself (`INDEX.md`, `AGENTS.md`,
`CHANGE-REQUEST.md`, `SOURCE-BRIEF.*`, `.claude/`, `.kiro/`, `cdad/`) and isn't
ordinary project scaffolding (`package.json`, `.gitignore`, a pre-existing
`README.md`, `LICENSE`, and the like) is a candidate solution document. The
Solution Designer does not have to name it anything in particular or tell the
agent it exists — a `.md`, `.txt`, Word, or PDF file sitting there is enough.

- **Exactly one candidate:** confirm it in one line — "Using `<name>` as the
  source document?" — rather than assuming silently, then use it.
- **No candidate at the root:** ask directly whether a document exists
  elsewhere — another path, an external doc, or paste it into chat.
- **More than one candidate:** ask which one. Do not guess between them.
- **A `SOURCE-BRIEF.*` already at the root:** this project was already
  bootstrapped. Stop and offer the `cdad-audit` skill instead (same as step 1).

Do not scan subdirectories or the rest of the repository speculatively looking
for "the" document — the root check above is the only place this skill looks
without being told, same as Claude Code checking a fixed location for
`AGENTS.md` instead of searching for it. Beyond that, ask.

Wherever it comes from, once it is processed a copy becomes `SOURCE-BRIEF.*` at
the project root (step 6) — permanent, not archived away into `cdad/docs/` —
so the reasoning behind the context stays visible and traceable right where
`CHANGE-REQUEST.md` already lives, not tucked inside `cdad/`.

## 3. Confirm the document is finished — or stop

If a document exists, do not start mapping it yet. Ask the Solution Designer
directly: is this finished — the real decisions, not a draft you're still
thinking through?

- **Confirmed finished:** move to step 4.
- **Still a draft, unsure, or "sort of":** stop here. Say plainly that
  `cdad-bootstrap` needs a finished document to work from, and that patching a
  draft with interview questions is not the same thing as the Solution
  Designer actually deciding it. Suggest reviewing it with an LLM for
  inconsistencies first if they haven't already. Do not proceed to step 4.
  They come back and run this skill again once it's ready.
- **No document exists at all:** this gate doesn't apply — skip straight to
  step 4. The interview itself is how the design gets defined this time.

This is a different confirmation from step 5. This one is about whether the
Solution Designer's *own* thinking is settled. Step 5 is about whether the
*derived* context files accurately capture it. Conflating them lets an
unfinished design slip through disguised as a completed bootstrap.

## 4. Ask what is still missing

Read the confirmed document and map its content onto the six files below. For
anything it does not answer, add it to the question list — do not infer or
invent an answer from adjacent context.

Group questions by file, not by field — six short rounds, not forty
one-line questions. Only ask about what the document actually left open.

| File | Ask for |
|---|---|
| `solution-vision.md` | The problem, who it's for, what success looks like, what it deliberately will not become |
| `architecture.md` | Architectural style, modules and boundaries, integration strategy, data ownership, deployment topology, known deviations |
| `stack.md` | Language, runtime, framework, compute model, datastores, messaging, identity, secrets, IaC, CI/CD, observability, testing |
| `constraints.md` | Cloud provider, compute model, IaC, runtime/language version, datastore, comms style, data residency, compliance, budget ceilings, explicit out-of-scope |
| `principles.md` | Design principles that would actually cause a PR to be rejected, and the trade-off each one accepts |
| `glossary.md` | Domain terms whose meaning here differs from the everyday meaning |

The fewer answers exist going in, the more of this step runs. That is
expected, not a failure state — a project with a thin source document just
needs more of the conversation to happen here instead.

If an answer is genuinely not decided yet, leave it empty rather than filling
it with a plausible guess — say so explicitly. An empty cell is a decision not
yet made; a guessed one is architecture invented by the agent, which is the
exact failure CDAD exists to prevent.

## 5. Confirm before drafting

Summarize what will go into each of the six files — not the full file text,
enough to review in one pass — and get explicit confirmation from the
Solution Designer before writing anything. Silence is not confirmation.

## 6. Write the context, then stop

The project is pre-freeze, so these paths are writable. Write directly the six
files under `cdad/context/`, using the exact target filenames (`stack.md`,
`architecture.md`, `constraints.md`, `principles.md`, `solution-vision.md`,
`glossary.md`).

If a source document existed (step 2), also write it at the project root as
`SOURCE-BRIEF`, keeping the original file extension, unmodified and not
paraphrased.

The accepted-decisions folder is writable in this same window: if
`ADR-001-context-governance.md` is not already there, write it too.

Then stop, without touching the freeze marker. End with a note telling the
Solution Designer to review and then run the freeze script to ratify.

## After bootstrap

Report, then point out three things.

**Report** (from step 0): detected ADE, resolved adapter, files installed,
adapters explicitly excluded, and whether native support exists for this
ADE. Give this report in chat, and also append it to `CDAD-COMPLETION.md`
at the project root, following the exact shape in `AGENTS.md` → *Completion
report* — that file is the durable record; chat output alone is lost once
the session ends. Append, don't overwrite, if the file already has an entry
from a prior bootstrap or re-run.

Before stopping, check `backlog.md`: if the source document or the
conversation surfaced Epics or Stories, ask whether they should be recorded
there now (via `cdad-propose-change`, form 4, same as any other backlog
change) — do not silently leave them out, and do not invent ones that
weren't actually stated. If nothing like that came up, say so plainly and
move on; an empty backlog is a valid state, not a gap to fill by guessing.

Point out three things:

- `stack.md`'s "Locked by" column should reference `ADR-001` for now; later
  decisions get their own ADR through the normal change flow.
- If a `SOURCE-BRIEF.*` was created, it now sits permanently at the project
  root next to `CHANGE-REQUEST.md` — the original design intent, kept for
  anyone who later asks why the context says what it says.
- Run `/context` to confirm only the resolved adapter's always-loaded file
  (`.claude/CLAUDE.md` for Claude Code, `AGENTS.md` itself for Kiro/Codex/
  Copilot), `AGENTS.md`, and `constraints.md` load — the same check the
  README asks for after any setup.
