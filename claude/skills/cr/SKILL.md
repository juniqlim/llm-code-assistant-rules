---
name: cr
description: 사용자의 마지막 요청/프롬프트를 시스템 클립보드에 복사
disable-model-invocation: true
allowed-tools: Bash(echo * | pbcopy)
---

대화에서 사용자의 가장 최근 메시지(프롬프트)를 찾아 pbcopy로 시스템 클립보드에 복사하세요.

사용법: echo '<메시지>' | pbcopy

복사 후 복사된 내용을 확인해 주세요.
