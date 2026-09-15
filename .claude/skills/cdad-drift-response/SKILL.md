---
name: cdad-drift-response
description: Use when a CDAD DRIFT SIGNAL is emitted, when cdad-audit reports a divergence, or when the user asks whether a change under src/, infra/, or a dependency manifest contradicts ratified architecture. Produces a proposal under cdad/proposals/ plus a promotion script the human runs to ratify it.
---

# CDAD drift response

Something outside the governed paths may have made the ratified context stale.
Determine whether it did, and if so, prepare the ratification.

This skill is the single response path for drift, whichever way it was found:
the PostToolUse detector, a `cdad-audit` sweep, or a direct question.

## Step 1 — Assess

Read the changed file and compare it against `cdad/context/stack.md`,
`cdad/context/architecture.md`, `cdad/context/constraints.md`, and any ADR under
`cdad/adr/` whose subject covers the change.

Three outcomes:

- **No contradiction.** Say so in one line and stop. Do not write a proposal.
  A proposal for a non-issue is noise that trains the reader to ignore the next
  one.
- **Fast track.** The decision is ratified in principle; only a detail moved —
  a version bump, an added service that fits an existing dependency rule.
- **Full track.** A ratified decision is being replaced. Alternatives and
  rejection reasons matter.

## Step 2 — Draft

Write to `cdad/proposals/PROPOSAL-<short-kebab-summary>.md`. No numbers:
numbering belongs to ADRs, which are the permanent record, and choosing an ADR
number would mean reserving ratified identity for your own draft.

`cdad/proposals/` is the only writable path under `cdad/`.

**Fast track** — minimum viable delta:

- What changed: file, before, after
- Which L0 statement or ADR it contradicts, quoted with file and line
- What the map should say instead
- The exact change-log row for `stack.md`

**Full track** — follow `cdad/adr/ADR-TEMPLATE.md`: context, decision,
alternatives considered with why each loses, consequences, risks.

Status line: `Status: Requires Architect approval`. Only the human accepts.

## Step 3 — Stage the promotion package, never execute it

If the proposal is accepted (or once you know it will need to be — ask if
unclear), stage the same promotion package the `cdad-adr` skill produces,
using the same shape it defines:

- `cdad/proposals/ADR-DRAFT-<slug>.md` — the ADR, following
  `cdad/adr/ADR-TEMPLATE.md` for the full track, or the fast-track minimum
  delta promoted into the same template shape
- `cdad/proposals/context-<basename>.md` for every affected file (`stack.md`
  at minimum, changelog row included)
- `cdad/proposals/apply-ADR-NNN-<slug>.sh` — the executable promotion script,
  with the required header, the `view`/`yes`/`no` review loop, one `mv`/`cp`
  per staged file, and a final `bash cdad/scripts/cdad-check-stack.sh`

State the ADR number as a suggestion — the next free one — and say it is the
human's to confirm. Then deliver the same "🟡 Change ready for review" message
`cdad-adr` uses: where the script is, what it will change, that review comes
first, the exact command to run it, and that you have not promoted anything.

## Hard rule

You draft and stage. The human promotes by running the script themselves.
Running the promotion yourself — or applying its changes by any other means —
would make you the ratifier of your own assertion, which is the exact failure
CDAD exists to prevent.
