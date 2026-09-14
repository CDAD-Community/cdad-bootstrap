#!/usr/bin/env python3
"""CDAD - L0/L1 context protection (PreToolUse hook).

permissions.deny already blocks the Write/Edit tools for the unconditional
machinery paths. This hook covers two more things static config can't
express: shell commands (sed -i, tee, redirection, mv) reaching the same
files without going through a file tool, and the two-regime condition on
cdad/context/ and cdad/adr/ - writable pre-freeze, denied once cdad/.frozen
exists (ADR-008). A static permissions.deny entry can't test for a file's
existence, so those two paths are deliberately absent from settings.json and
live here instead.

Exit 2 plus permissionDecision:deny blocks the call deterministically.
Any unexpected input exits 0 so a broken hook never blocks a session.
"""

import json
import os
import re
import sys

FROZEN_MARKER = "cdad/.frozen"

REGIME_PATHS = re.compile(r"cdad/(context|adr)/")
ROOT_FILES = re.compile(r"CHANGE-REQUEST\.md|SOURCE-BRIEF\.")
MUTATING_SHELL = re.compile(
    r"\b(sed\s+-i|tee|mv|cp|rm|truncate|dd|install)\b"
    r"|>>?\s*\S*(cdad/|CHANGE-REQUEST\.md|SOURCE-BRIEF\.)"
)

REASON = (
    "CDAD governance: cdad/context/, cdad/adr/, CHANGE-REQUEST.md, and "
    "SOURCE-BRIEF.* are owned by the Solution Designer. Write your draft to "
    "cdad/proposals/ instead - that directory is yours. Use the "
    "cdad-propose-change or cdad-bootstrap skill."
)


def is_frozen() -> bool:
    return os.path.exists(FROZEN_MARKER)


def is_protected(target: str) -> bool:
    # cdad/proposals/ is the one directory an agent may always write to -
    # SOURCE-BRIEF.* and CHANGE-REQUEST.md are only protected outside it
    # (e.g. cdad-bootstrap staging cdad/proposals/bootstrap/SOURCE-BRIEF.md).
    if "cdad/proposals/" in target:
        return False
    if REGIME_PATHS.search(target):
        return is_frozen()
    return bool(ROOT_FILES.search(target))


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except Exception:
        return 0

    tool = event.get("tool_name", "")
    tool_input = event.get("tool_input") or {}
    target = ""

    if tool in ("Write", "Edit", "NotebookEdit"):
        target = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
    elif tool == "Bash":
        command = tool_input.get("command", "")
        # Only flag commands that could mutate. Reads stay allowed.
        if MUTATING_SHELL.search(command):
            target = command

    if target and is_protected(target):
        print(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": REASON,
                    }
                }
            )
        )
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
