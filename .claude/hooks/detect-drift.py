#!/usr/bin/env python3
"""CDAD - drift detection (PostToolUse hook).

L3 (src/, infra/, dependency manifests, ...) is free by design - it is not a
governed path - but a change there can silently override a decision that is
locked in cdad/context/stack.md. This hook is the write-time trigger of that
check: the cdad-audit skill is the sweep trigger for everything this hook
did not happen to see.

Reads the ```cdad-drift-signals fenced block from cdad/context/stack.md - one
`<glob> -> <what it guards>` line per signal - and warns on stderr when a
write matches a glob. Advisory only: it never blocks (always exits 0) and
only runs once the project is governed (cdad/.frozen present); pre-freeze
there is nothing ratified yet to contradict. A category warns once per
session - the dedup state lives outside the repo (system temp), never inside
it, so a session never leaves a trace in the working tree.

Shell mutations of L3 are invisible here (PostToolUse tool_input for Bash is
a command string, not a path) - cdad/scripts/cdad-check-stack.sh is the net
for that case, same as for the write block in protect-l0.py.
"""

import fnmatch
import json
import os
import re
import sys
import tempfile

FROZEN_MARKER = "cdad/.frozen"
STACK_MAP = "cdad/context/stack.md"

BLOCK_RE = re.compile(
    r"```cdad-drift-signals\r?\n(.*?)```", re.DOTALL
)
LINE_RE = re.compile(r"^\s*([^#\s][^\s]*)\s*->\s*(.+?)\s*$")


def is_frozen() -> bool:
    return os.path.exists(FROZEN_MARKER)


def load_signals():
    try:
        with open(STACK_MAP, "r", encoding="utf-8") as f:
            text = f.read()
    except OSError:
        return []

    match = BLOCK_RE.search(text)
    if not match:
        return []

    signals = []
    for line in match.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = LINE_RE.match(line)
        if m:
            signals.append((m.group(1), m.group(2)))
    return signals


def already_warned(session_id: str, glob: str) -> bool:
    state_path = os.path.join(
        tempfile.gettempdir(), f"cdad-drift-{session_id}.json"
    )
    try:
        with open(state_path, "r", encoding="utf-8") as f:
            warned = set(json.load(f))
    except (OSError, ValueError):
        warned = set()

    if glob in warned:
        return True

    warned.add(glob)
    try:
        with open(state_path, "w", encoding="utf-8") as f:
            json.dump(sorted(warned), f)
    except OSError:
        pass
    return False


def main() -> int:
    if not is_frozen():
        return 0

    try:
        event = json.load(sys.stdin)
    except Exception:
        return 0

    tool = event.get("tool_name", "")
    if tool not in ("Write", "Edit", "NotebookEdit"):
        return 0

    tool_input = event.get("tool_input") or {}
    target = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
    if not target:
        return 0

    session_id = event.get("session_id", "unknown")
    target = target.replace("\\", "/")

    for glob, guards in load_signals():
        if fnmatch.fnmatch(target, f"*{glob}") or fnmatch.fnmatch(target, glob):
            if already_warned(session_id, glob):
                continue
            print(
                f"CDAD DRIFT SIGNAL: {target} matches '{glob}', which guards "
                f"{guards}. Run the cdad-drift-response skill to assess "
                f"whether this contradicts the ratified context.",
                file=sys.stderr,
            )

    return 0


if __name__ == "__main__":
    sys.exit(main())
