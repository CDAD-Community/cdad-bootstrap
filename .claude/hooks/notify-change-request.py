#!/usr/bin/env python3
"""CDAD - pending change-request notice (UserPromptSubmit hook).

CHANGE-REQUEST.md is edited by the Solution Designer directly, outside any
Claude Code tool call (the file is in permissions.deny, so the agent cannot
write it either). No PreToolUse/PostToolUse hook can see that edit - it
happens outside the tool loop entirely. This hook is the workaround: it
re-reads the file on every user turn and, if the request block has real
content the agent has not already flagged this session, adds one line of
context saying so.

It never analyzes the request, never drafts a proposal, and never invokes
cdad-propose-change - it only makes sure a filled-in request does not go
unnoticed until the Solution Designer happens to say "process the change
request." Acting on it remains a human-triggered decision, same as today.

Dedup state lives outside the repo (system temp), keyed by session id, so a
session is reminded once per distinct request content - never inside the
repo, never committed, never re-nagging every turn.

Exit 0 always. A broken hook must never block a prompt from being submitted.
"""

import hashlib
import json
import os
import re
import sys
import tempfile

CHANGE_REQUEST = "CHANGE-REQUEST.md"

SECTION_RE = re.compile(
    r"##\s*CDAD Request\s*\n(.*?)(?=\n###|\n---|\Z)", re.DOTALL
)
FENCE_RE = re.compile(r"```text\s*\n(.*?)```", re.DOTALL)
PLACEHOLDER_RE = re.compile(r"TODO|PLACEHOLDER|REPLACE ME|<[a-zA-Z][^>]*>")


def extract_request_block(text: str) -> str:
    section = SECTION_RE.search(text)
    if not section:
        return ""
    fence = FENCE_RE.search(section.group(1))
    return fence.group(1).strip() if fence else ""


def has_pending_request(block: str) -> bool:
    if not block:
        return False
    if PLACEHOLDER_RE.search(block):
        return False
    non_empty_lines = [l for l in block.splitlines() if l.strip()]
    return len(non_empty_lines) >= 3


def already_notified(session_id: str, content_hash: str) -> bool:
    state_path = os.path.join(
        tempfile.gettempdir(), f"cdad-change-request-{session_id}.json"
    )
    try:
        with open(state_path, "r", encoding="utf-8") as f:
            seen = set(json.load(f))
    except (OSError, ValueError):
        seen = set()

    if content_hash in seen:
        return True

    seen.add(content_hash)
    try:
        with open(state_path, "w", encoding="utf-8") as f:
            json.dump(sorted(seen), f)
    except OSError:
        pass
    return False


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except Exception:
        return 0

    try:
        with open(CHANGE_REQUEST, "r", encoding="utf-8") as f:
            text = f.read()
    except OSError:
        return 0

    block = extract_request_block(text)
    if not has_pending_request(block):
        return 0

    session_id = event.get("session_id", "unknown")
    content_hash = hashlib.sha256(block.encode("utf-8")).hexdigest()[:16]

    if already_notified(session_id, content_hash):
        return 0

    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": (
                        "CDAD: CHANGE-REQUEST.md currently has a filled-in, "
                        "unprocessed request. If the Solution Designer has not "
                        "asked you to work on it, you may mention it exists, "
                        "but do not read it in depth, analyze it, or draft a "
                        "proposal unless explicitly told to process it."
                    ),
                }
            }
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
