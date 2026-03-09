#!/usr/bin/env python3
"""Inspect recent Codex sessions for the current project."""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


IGNORE_PREFIXES = (
    "[Request interrupted",
    "<",
    "Base directory for this skill",
    "# AGENTS.md instructions",
)


@dataclass
class SessionInfo:
    path: Path
    session_id: str
    mtime: float
    cwd: str
    first_user_message: str
    user_messages: list[str]


def should_keep_message(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return False
    return not any(stripped.startswith(prefix) for prefix in IGNORE_PREFIXES)


def flatten_message_text(content: object) -> str:
    if isinstance(content, str):
        return content.strip()
    if not isinstance(content, list):
        return ""

    parts: list[str] = []
    for item in content:
        if not isinstance(item, dict):
            continue
        text = item.get("text")
        if isinstance(text, str):
            parts.append(text.strip())
    return " ".join(part for part in parts if part).strip()


def extract_user_message(message: object) -> str | None:
    if not isinstance(message, dict):
        return None
    if message.get("type") != "message" or message.get("role") != "user":
        return None

    text = flatten_message_text(message.get("content"))
    if should_keep_message(text):
        return text
    return None


def collect_user_messages(session_path: Path) -> list[str]:
    messages: list[str] = []

    with session_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue

            record_type = record.get("type")
            payload = record.get("payload")

            if record_type == "response_item" and isinstance(payload, dict):
                text = extract_user_message(payload)
                if text:
                    messages.append(text)
                continue

            if record_type == "compacted" and isinstance(payload, dict):
                history = payload.get("replacement_history")
                if not isinstance(history, list):
                    continue
                for message in history:
                    text = extract_user_message(message)
                    if text:
                        messages.append(text)

    return messages


def get_session_cwd(session_path: Path) -> str | None:
    with session_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue

            payload = record.get("payload")
            if not isinstance(payload, dict):
                continue

            record_type = record.get("type")
            if record_type == "session_meta":
                cwd = payload.get("cwd")
                if isinstance(cwd, str) and cwd:
                    return cwd

            if record_type == "turn_context":
                cwd = payload.get("cwd")
                if isinstance(cwd, str) and cwd:
                    return cwd

    return None


def iter_session_paths(root: Path) -> list[Path]:
    return sorted(root.glob("**/*.jsonl"), key=lambda path: path.stat().st_mtime, reverse=True)


def build_session_info(session_path: Path) -> SessionInfo | None:
    cwd = get_session_cwd(session_path)
    if not cwd:
        return None

    messages = collect_user_messages(session_path)
    first_user_message = messages[0] if messages else ""
    return SessionInfo(
        path=session_path,
        session_id=session_path.stem,
        mtime=session_path.stat().st_mtime,
        cwd=cwd,
        first_user_message=first_user_message,
        user_messages=messages,
    )


def find_candidate_sessions(root: Path, cwd: str, limit: int | None = None) -> list[SessionInfo]:
    matches: list[SessionInfo] = []
    for session_path in iter_session_paths(root):
        info = build_session_info(session_path)
        if not info or info.cwd != cwd:
            continue
        matches.append(info)

    if matches:
        matches = matches[1:]

    if limit is not None:
        return matches[:limit]
    return matches


def format_timestamp(epoch_seconds: float) -> str:
    return datetime.fromtimestamp(epoch_seconds).strftime("%m/%d %H:%M")


def shorten(text: str, width: int = 80) -> str:
    clean = " ".join(text.split())
    if len(clean) <= width:
        return clean
    return clean[: width - 3] + "..."


def summarize_session(session: SessionInfo) -> str:
    if not session.user_messages:
        return "(no user message found)"

    first = shorten(session.user_messages[0], width=48)
    last = shorten(session.user_messages[-1], width=48)
    if first == last:
        return first
    return f"{first} / 마지막: {last}"


def render_list(sessions: list[SessionInfo]) -> str:
    if not sessions:
        return "No matching prior sessions found."

    lines: list[str] = []
    for index, session in enumerate(sessions, start=1):
        preview = summarize_session(session)
        lines.append(f"{index}. [{format_timestamp(session.mtime)}] {preview}")
        lines.append(f"   ID: {session.session_id}")
    return "\n".join(lines)


def resolve_selection(sessions: list[SessionInfo], value: str) -> SessionInfo:
    if value.isdigit():
        index = int(value)
        if index < 1 or index > len(sessions):
            raise ValueError(f"Selection {value} is out of range")
        return sessions[index - 1]

    matches = [session for session in sessions if session.session_id.startswith(value)]
    if not matches:
        raise ValueError(f"No session matches prefix {value}")
    if len(matches) > 1:
        raise ValueError(f"Session prefix {value} is ambiguous")
    return matches[0]


def render_session(session: SessionInfo) -> str:
    lines = [
        f"SESSION: {session.session_id}",
        f"WHEN: {format_timestamp(session.mtime)}",
        f"CWD: {session.cwd}",
        "",
    ]

    for message in session.user_messages[-3:]:
        lines.append(f"USER: {message[:500]}")
        lines.append("")

    return "\n".join(lines).rstrip()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="List and inspect recent Codex sessions")
    parser.add_argument(
        "--sessions-root",
        default="~/.codex/sessions",
        help="Root directory that contains Codex session JSONL files",
    )
    parser.add_argument(
        "--cwd",
        default=os.getcwd(),
        help="Filter sessions by working directory",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Maximum number of sessions to display in list mode",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("list", help="List recent prior sessions for the current project")

    show_parser = subparsers.add_parser("show", help="Show extracted user messages for one session")
    show_parser.add_argument("selection", help="1-based list index or session ID prefix")

    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = Path(args.sessions_root).expanduser()
    cwd = str(Path(args.cwd).expanduser())

    try:
        sessions = find_candidate_sessions(root, cwd, limit=args.limit if args.command == "list" else None)
    except OSError as exc:
        print(str(exc))
        return 1

    if args.command == "list":
        print(render_list(sessions))
        return 0

    try:
        session = resolve_selection(sessions, args.selection)
    except ValueError as exc:
        print(str(exc))
        return 2

    print(render_session(session))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
