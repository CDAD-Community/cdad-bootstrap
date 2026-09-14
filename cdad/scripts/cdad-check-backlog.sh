#!/usr/bin/env bash
# CDAD - backlog structural integrity gate.
#
# backlog.md is not architecture (see AGENTS.md "Backlog governance") but it
# is still a governed artifact: Epic/Story identifiers must stay unique and
# traceable, and status values must stay inside the agreed vocabulary so
# both agents and humans can rely on them. This makes that check
# deterministic instead of a visual scan.
#
# What this does NOT enforce: whether an Epic/Story addition or removal went
# through CHANGE-REQUEST.md. That distinction (structural change vs. routine
# status update) requires judgment this script cannot make - it stays an
# instruction-plane rule in AGENTS.md, not a control-plane one here.
#
# Usage:
#   cdad/scripts/cdad-check-backlog.sh [path-to-backlog.md]
#
# Exit 0 = pass, 1 = violation, 2 = cannot determine.

set -euo pipefail

BACKLOG="${1:-backlog.md}"

if [ ! -f "$BACKLOG" ]; then
  echo "cdad-check-backlog: $BACKLOG not found." >&2
  exit 2
fi

EPIC_STATUSES="Proposed|Planned|In Progress|Completed|Cancelled"
STORY_STATUSES="Proposed|Ready|In Progress|Blocked|Done|Cancelled"
FAIL=0

# --- duplicate Epic IDs ---
DUP_EPICS="$(grep -oE '^### EPIC-[0-9]+' "$BACKLOG" | sed 's/^### //' | sort | uniq -d || true)"
if [ -n "$DUP_EPICS" ]; then
  echo "cdad-check-backlog: FAILED - duplicate Epic IDs:" >&2
  echo "$DUP_EPICS" | sed 's/^/  /' >&2
  FAIL=1
fi

# --- duplicate Story IDs (unique project-wide, not just per-Epic) ---
DUP_STORIES="$(grep -oE '^##### STORY-[0-9]+' "$BACKLOG" | sed 's/^##### //' | sort | uniq -d || true)"
if [ -n "$DUP_STORIES" ]; then
  echo "cdad-check-backlog: FAILED - duplicate Story IDs:" >&2
  echo "$DUP_STORIES" | sed 's/^/  /' >&2
  FAIL=1
fi

# --- Epic status vocabulary ---
BAD_EPIC_STATUS="$(grep -A2 '^### EPIC-' "$BACKLOG" | grep -E '^\*\*Status:\*\*' | grep -vE "^\*\*Status:\*\* ($EPIC_STATUSES)[[:space:]]*\$" || true)"
if [ -n "$BAD_EPIC_STATUS" ]; then
  echo "cdad-check-backlog: FAILED - Epic status outside {$EPIC_STATUSES}:" >&2
  echo "$BAD_EPIC_STATUS" | sed 's/^/  /' >&2
  FAIL=1
fi

# --- Story status vocabulary ---
BAD_STORY_STATUS="$(grep -A2 '^##### STORY-' "$BACKLOG" | grep -E '^[[:space:]]*- \*\*Status:\*\*' | grep -vE "^[[:space:]]*- \*\*Status:\*\* ($STORY_STATUSES)[[:space:]]*\$" || true)"
if [ -n "$BAD_STORY_STATUS" ]; then
  echo "cdad-check-backlog: FAILED - Story status outside {$STORY_STATUSES}:" >&2
  echo "$BAD_STORY_STATUS" | sed 's/^/  /' >&2
  FAIL=1
fi

# --- Epics with zero Stories (warning only - a freshly proposed Epic is legitimate) ---
EMPTY_EPICS="$(awk '
  /^### EPIC-/     { if (epic != "" && count == 0) print epic; epic=$0; count=0; next }
  /^##### STORY-/  { count++ }
  /^## /           { if (epic != "" && count == 0) print epic; epic=""; count=0 }
  END              { if (epic != "" && count == 0) print epic }
' "$BACKLOG" || true)"
if [ -n "$EMPTY_EPICS" ]; then
  echo "cdad-check-backlog: WARNING - Epics with no Stories yet:"
  echo "$EMPTY_EPICS" | sed 's/^/  /'
fi

if [ "$FAIL" -ne 0 ]; then
  cat >&2 <<MSG

cdad-check-backlog: FAILED

Structural integrity violations found above. An Epic ID must be unique, a
Story ID must be unique project-wide, and status values must stay inside
the agreed vocabulary so tooling and agents can rely on them without
re-parsing free text.
MSG
  exit 1
fi

echo "cdad-check-backlog: OK"
