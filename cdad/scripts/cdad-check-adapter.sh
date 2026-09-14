#!/usr/bin/env bash
# CDAD - ADE adapter validation gate.
#
# CDAD ships a portable core plus one adapter per supported ADE. A target
# project should have exactly the adapter matching its ADE installed, and
# none of the others. This makes that check deterministic instead of a
# visual scan of the file tree.
#
# Usage:
#   cdad/scripts/cdad-check-adapter.sh <claude|kiro|codex|copilot|unknown>
#
# Exit 0 = matches the matrix, 1 = violation, 2 = bad usage.

set -euo pipefail

ADE="${1:-}"

usage() {
  echo "usage: cdad-check-adapter.sh <claude|kiro|codex|copilot|unknown>" >&2
  exit 2
}

[ -n "$ADE" ] || usage

case "$ADE" in
  claude)  EXPECT_CLAUDE=yes; EXPECT_KIRO=no;  EXPECT_COPILOT=no;  EXPECT_AGENTS=yes ;;
  kiro)    EXPECT_CLAUDE=no;  EXPECT_KIRO=yes; EXPECT_COPILOT=no;  EXPECT_AGENTS=yes ;;
  codex)   EXPECT_CLAUDE=no;  EXPECT_KIRO=no;  EXPECT_COPILOT=no;  EXPECT_AGENTS=yes ;;
  copilot) EXPECT_CLAUDE=no;  EXPECT_KIRO=no;  EXPECT_COPILOT=yes; EXPECT_AGENTS=yes ;;
  unknown) EXPECT_CLAUDE=no;  EXPECT_KIRO=no;  EXPECT_COPILOT=no;  EXPECT_AGENTS=skip ;;
  *) usage ;;
esac

FAIL=0

check() {
  label="$1"; path="$2"; expect="$3"

  if [ "$expect" = skip ]; then
    return 0
  fi

  if [ -e "$path" ]; then
    present=yes
  else
    present=no
  fi

  if [ "$present" != "$expect" ]; then
    echo "cdad-check-adapter: FAILED - $label: expected $expect, found $present ($path)" >&2
    FAIL=1
  fi
}

check ".claude/"                        ".claude"                          "$EXPECT_CLAUDE"
check ".kiro/"                           ".kiro"                           "$EXPECT_KIRO"
check ".copilot/copilot-instructions.md"  ".copilot/copilot-instructions.md" "$EXPECT_COPILOT"
check "AGENTS.md"                        "AGENTS.md"                       "$EXPECT_AGENTS"

if [ "$FAIL" -ne 0 ]; then
  cat >&2 <<MSG

cdad-check-adapter: workspace does not match the '$ADE' adapter matrix.

A project installs the portable core plus exactly one adapter - never the
whole catalog, never more than one native adapter. See 'ADE adapters' in
README.md or step 0 of the cdad-bootstrap skill.
MSG
  exit 1
fi

echo "cdad-check-adapter: OK - workspace matches the '$ADE' adapter matrix."
