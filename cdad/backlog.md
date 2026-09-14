# Project Backlog

> The project's living development line — Epics, Stories, and the work
> currently expected to be built. This is a development-planning artifact,
> not architecture: see *Precedence* below. It answers "what exists, what's
> next, what's blocked" — not "how may it be built" or "what decisions are
> authoritative."

**Last verified:** `YYYY-MM-DD` — run the `cdad-audit` skill to reconcile against defined requirements.

---

## Development Line

<what phase, release, or milestone this backlog currently represents — one or two sentences. Leave empty rather than inventing one.>

## Precedence

```text
Governed Context / L0
        v
ADR / governed decisions
        v
This backlog
        v
Implementation work
```

If a Story appears to contradict governed context or an accepted ADR, that
is a finding, not a resolution. Raise it through `cdad/CHANGE-REQUEST.md` —
a Story never silently overrides architecture.

---

## Epics

No Epics are currently defined.

If defined Epics or Stories exist elsewhere (a requirements doc, an issue
tracker, prior conversation) but are not yet reflected here, that is a gap
to close through the normal change process — not something to invent
around. See `AGENTS.md` → *Backlog governance*.

### Example

The block below shows the expected shape. It is illustrative only — replace
it with real Epics once the development line is defined; do not treat
`EPIC-000`/`STORY-000` as a real entry.

```markdown
### EPIC-000 — Example epic

**Status:** Proposed
**Goal:** <what this epic delivers and why>

#### Stories

##### STORY-000 — Example story

- **Status:** Proposed
- **Priority:** Medium
- **Description:** <what this story delivers>
- **Acceptance Criteria:**
  - <criterion>
  - <criterion>
- **Dependencies:** None
- **Notes:** <optional>
```

---

## General Development Work

Work tracked here that is not tied to a specific Story.

- None

## Current Focus

What is actively being worked on right now.

- None

## Next Work

What comes after Current Focus.

- None

## Blocked

- None

---
Governance: adding or removing an Epic/Story, or materially changing its
scope or acceptance criteria, goes through `cdad/CHANGE-REQUEST.md` ->
`cdad/proposals/` -> Solution Designer decision — the same funnel as an
architecture change. Updating a Story's status, or the *Current Focus* /
*Next Work* / *Blocked* lists, as part of already-approved implementation
work does not need a change request. See `AGENTS.md` → *Backlog governance*
for the full rule and precedence relative to L0/ADRs.
