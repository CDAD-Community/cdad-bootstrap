#!/usr/bin/env python3
"""CDAD - L0/L1 context protection (PreToolUse hook).

permissions.deny already blocks the Write/Edit tools for the unconditional
machinery paths. This hook covers what static config can't express: shell
commands (sed -i, tee, redirection, mv, rm, ...) reaching those same
machinery paths and the two protected governance files - cdad/CHANGE-REQUEST.md
(moved under cdad/ in v2.1) and SOURCE-BRIEF.* (stays at the project root,
the one human-facing exception) - without going through a file tool, and the
two-regime condition on cdad/context/ and cdad/adr/ - writable pre-freeze,
denied once cdad/.frozen exists. A static permissions.deny entry can't test
for a file's existence, so those two paths are deliberately absent from
settings.json and live here instead.

ROOT_FILES matches by filename substring, not by directory prefix, so it
keeps protecting CHANGE-REQUEST.md and SOURCE-BRIEF.* correctly regardless
of which directory each lives in - the v2.1 relocation of CHANGE-REQUEST.md
under cdad/ needed no logic change here, only settings.json's static glob.

Machinery (.claude/settings.json, .claude/hooks/) has no regime exception
and no Write/Edit fallback here either: permissions.deny already blocks the
tool path, so this hook's job for machinery is exclusively the shell path -
an agent must never be able to disarm its own protection via sed/rm/tee/
redirection just because that happens to route through Bash instead of Edit.

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
MACHINERY = re.compile(r"\.claude/settings\.json|\.claude/hooks/")
MUTATING_SHELL = re.compile(
    r"\b(sed\s+-i|tee|mv|cp|rm|truncate|dd|install)\b"
    r"|>>?\s*\S*(cdad/|CHANGE-REQUEST\.md|SOURCE-BRIEF\."
    r"|\.claude/settings\.json|\.claude/hooks/)"
)
# An agent may always write drafts into cdad/proposals/ (see is_protected),
# but it must never be the one to execute the promotion script it staged
# there - that is the Human Promotion Boundary (AGENTS.md). Kept as its own
# pattern, checked ahead of the cdad/proposals/ exemption in is_protected(),
# so that exemption keeps allowing every other mutating command inside
# cdad/proposals/ (mv/rm/cp cleanup of stale drafts).
PROMOTION_SCRIPT_EXEC = re.compile(
    r"\b(?:bash|sh|\.)\s+\S*cdad/proposals/apply-[A-Za-z0-9._-]+\.sh\b"
)

REASON = (
    "CDAD governance: cdad/context/, cdad/adr/, cdad/CHANGE-REQUEST.md, "
    "SOURCE-BRIEF.*, and the .claude/ governance machinery itself are "
    "owned by the Solution Designer. Write your draft to cdad/proposals/ "
    "instead - that directory is yours. Use the cdad-propose-change or "
    "cdad-bootstrap skill."
)


def is_frozen() -> bool:
    return os.path.exists(FROZEN_MARKER)


def is_protected(target: str) -> bool:
    if MACHINERY.search(target):
        return True
    if PROMOTION_SCRIPT_EXEC.search(target):
        return True
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
        # Only flag commands that could mutate, or that execute a staged
        # promotion script. Reads stay allowed.
        if MUTATING_SHELL.search(command) or PROMOTION_SCRIPT_EXEC.search(command):
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
