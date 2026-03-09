---
name: recap
description: Recover prior Codex conversation context for the current project. Use when the user asks to recap what they were doing, restore context after a reset or clear, or inspect a recent Codex session by index or session ID prefix.
---

# Recap

Use this skill to recover context from recent Codex sessions for the same project directory.
The script finds prior sessions under `~/.codex/sessions`, excludes the current newest session, and extracts recent user requests.

## Workflow

1. Resolve the session root.
   - Default: `~/.codex/sessions`
   - Override only if the user explicitly points to another session directory.
2. Resolve the project directory.
   - Default: current working directory.
   - Override only if the user explicitly wants a different project path.
3. If the user did not specify a session, list recent prior sessions:
   - `python3 /Users/juniq/.codex/skills/recap/scripts/recap.py list`
   - Show the output and ask the user to pick an index or session ID prefix.
4. If the user specified a number or session prefix, show that session directly:
   - `python3 /Users/juniq/.codex/skills/recap/scripts/recap.py show 1`
   - `python3 /Users/juniq/.codex/skills/recap/scripts/recap.py show 019cd0ab`
5. Summarize the extracted messages concisely:
   - 무엇을 하고 있었는지
   - 마지막으로 무엇을 요청했는지
   - 현재 상태 (완료/진행중/불명)

## Notes

- The script reads `session_meta.payload.cwd` first and falls back to `turn_context.payload.cwd`.
- It extracts user messages from `response_item` records and compacted history.
- It filters obvious noise such as interrupted requests and injected environment blocks.
