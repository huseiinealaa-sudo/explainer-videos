#!/usr/bin/env python3
"""PreToolUse hook of the video-critic agent: its only writable place is its memory folder.

The critic has Write and Edit so it can keep .claude/agent-memory/video-critic/MEMORY.md
itself (see .claude/agents/video-critic.md). This hook blocks every write, edit or notebook
edit whose target resolves (symlinks and ".." included) outside that folder: exit code 2
denies the tool call and the message on stderr goes back to the agent.
"""
import json
import os
import sys
from pathlib import Path

MEMORY_DIR = Path(".claude") / "agent-memory" / "video-critic"


def allowed(target, project_dir):
    root = (Path(project_dir) / MEMORY_DIR).resolve()
    path = Path(target)
    if not path.is_absolute():
        path = Path(project_dir) / path
    return path.resolve().is_relative_to(root)


def main():
    data = json.load(sys.stdin)
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd()
    tool_input = data.get("tool_input") or {}
    target = tool_input.get("file_path") or tool_input.get("notebook_path")
    if target and allowed(target, project_dir):
        return 0
    print(f"Blocked: video-critic is read-only; it may write only inside {MEMORY_DIR}/ "
          f"(asked: {target or 'no path'})", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
