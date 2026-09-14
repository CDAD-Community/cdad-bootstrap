---
name: cdad-propose-change
description: Produce a CDAD change proposal instead of applying a change directly. Use when the user says to process the change request, when an architectural change is required, when a governed context file under cdad/context/ is wrong or outdated, when implementation code conflicts with the governed context, or when cdad/backlog.md needs an Epic/Story added, removed, or materially changed. Triggers on any request to change architecture, paradigm, module boundaries, frameworks, cloud services, or infrastructure tooling, on any request to change the committed development line, and whenever a permission denial points at cdad/context/, cdad/adr/, or cdad/CHANGE-REQUEST.md.
---

# CDAD change proposal

Governed context is owned by the Solution Designer. You produce proposals; a
human decides. Do not implement the change, do not partially apply it, and do
not create the ADR yourself.

## Where the request comes from

If the user says "process the change request", read `cdad/CHANGE-REQUEST.md`
first. It holds the Solution Designer's stated intent. If
the request block is empty or unchanged from the template, say so and stop —
do not invent one.

The request block may be filled in tersely or as a raw paragraph pasted
straight from the Solution Designer's own document — both are valid input.
Read a pasted excerpt for what it actually decides; do not ask them to
compress it into the template's fields first.

Otherwise the request is whatever the user just described.

## Where the output goes

Write the proposal to `cdad/proposals/PROPOSAL-<short-kebab-summary>.md`. That
directory is the only place under `cdad/` you may write.

Do not edit `cdad/CHANGE-REQUEST.md` — not to clear it, not to mark it
processed, not to tidy it. It is the Solution Designer's desk.

## Before writing

Read what the change actually touches: `cdad/context/stack.md` always, plus the
relevant context files and any ADR the affected stack rows point to in their
"Locked by" column. A proposal that ignores the decision it overturns is not a
proposal.

If the request is about the development line instead — a new Epic/Story, or
a material change to one's scope or acceptance criteria — read `cdad/backlog.md`
first, and check whether it contradicts governed context or an accepted
ADR before drafting (see backlog *Precedence* in `AGENTS.md`). Routine Story
status updates during already-approved work are not a change request at
all; redirect those back to direct editing, not a proposal.

## Forms

Pick the one that matches the situation.

## 1. Architecture change

Use when the solution needs a different architectural direction, style,
paradigm, module boundary, integration strategy, deployment strategy, framework,
runtime, datastore, or cloud service.

```text
Proposed Architecture Change

Current decision:
Suggested change:
Reason:
Impact:
Risk:
Affected files:
Alternatives considered:

Status: Requires Architect approval
```

## 2. Context change

Use when a file under `cdad/context/` is inaccurate, stale, or contradicts
reality — and the fix is to the document, not the code.

```text
Proposed Context Change

File:
Current statement:
Suggested change:
Reason:
Impact:
Risk:

Status: Requires Solution Designer approval
```

## 3. Context conflict

Use when implementation and governed context disagree and you cannot tell which
one is correct. Do not resolve it yourself and do not pick the code by default.

```text
Context Conflict Detected

Context file:
What the context says:
What the implementation does:
Where they diverge:
Possible resolutions:

Status: Requires human review
```

## 4. Development-line change

Use when `cdad/backlog.md` needs an Epic or Story added, removed, or materially
changed in scope or acceptance criteria. Not for routine status updates
during already-approved work — those are direct edits, not a proposal.

```text
Proposed Backlog Change

Kind: <new Epic / new Story / remove / material scope change>
Epic/Story ID: <EPIC-NNN / STORY-NNN, or "new" if not yet assigned>
Current state: <what cdad/backlog.md says today, or "none" if new>
Suggested change:
Reason:
Contradicts governed context or an ADR?: <no / yes — cite file:line>
Impact:
Risk:

Status: Requires Solution Designer approval
```

If the request would contradict governed context or an accepted ADR, say so
explicitly rather than quietly aligning the Story to the architecture — that
contradiction is exactly what the Solution Designer needs to see and decide.

## Quality bar

A proposal is only useful if it can be decided without a follow-up question.

- Name the specific decision being changed, not the general area.
- Impact means blast radius: which modules, which interfaces, which deployments.
- Risk means what breaks if this is wrong, and how it would be detected.
- List at least one alternative and say why it loses.
- If you cannot fill a field honestly, say so rather than inventing it.

## After writing

State the file path you wrote and summarize the proposal in two or three lines
in chat, so the decision can be made without opening the file. Then stop.

Once an architecture, context, or conflict proposal (forms 1-3) is approved,
the decision is recorded with the `cdad-adr` skill. A development-line
proposal (form 4) is not an architectural decision — once approved, the
Solution Designer applies it directly to `cdad/backlog.md`; it does not get an
ADR unless it also happens to touch governed context.
