# Proposals — staging area

Agent-writable. This is the only place under `cdad/` an agent may create files.

A proposal here is a **draft, not a decision**. Nothing in this directory
governs anything. It exists so the agent can hand you a complete, reviewable
artifact without ever touching `cdad/context/` or `cdad/adr/`.

## Flow

```
cdad/CHANGE-REQUEST.md  →  cdad/proposals/  →  cdad/adr/ + cdad/context/
                                                or cdad/backlog.md (dev-line changes)
   you write intent         agent drafts        you apply, after approval
   (always writable)        (agent writable)
```

A development-line proposal (new/removed Epic or Story, or a material scope
change — `cdad-propose-change` form 4) is applied to `cdad/backlog.md`, not
`cdad/adr/`, unless it also happens to touch governed context. Routine Story
status updates never pass through here at all — they're direct edits.

## Lifecycle

| State | Meaning |
|---|---|
| `PROPOSAL-<slug>.md` | awaiting your review |
| `bootstrap/` | the `cdad-bootstrap` skill's one-time draft of all six `cdad/context/` files, plus `SOURCE-BRIEF.*` if a source document existed — the one case where a batch of files lands here instead of a single proposal |
| deleted | rejected, or promoted to an ADR / applied to context |

Delete proposals once resolved. A directory full of stale drafts is the same
failure as stale context: it makes the current state ambiguous.

## Naming

`PROPOSAL-<short-kebab-summary>.md` — no numbers. Numbering belongs to ADRs,
which are the permanent record. A proposal that never gets accepted should not
consume a number.
