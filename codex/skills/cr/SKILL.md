---
name: cr
description: Copy the user's last request or prompt to the system clipboard. Use when the user asks to copy their recent query text.
allowed-tools: Bash
---

1. Find the previous user message in the current conversation (not the current copy request).
2. Copy it with `pbcopy` using a heredoc:
   - `cat <<'EOF' | pbcopy`
   - `<previous-user-message>`
   - `EOF`
3. Confirm exactly what was copied.
