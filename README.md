# LLM Code Assistant Rules

LLM 기반 코드 어시스턴트(Claude Code, Cursor, Copilot 등)에 적용할 수 있는 규칙 모음입니다.

> **원칙: 목표로 가는 최단경로를 탐색하고 최단경로로 목표에 도달한다.**

## 주요 규칙

### 코드 작성
- TDD: 구현 전 테스트 코드 먼저 작성
- 단위 테스트 우선, 불가능할 때만 통합 테스트
- 단위/통합 테스트 파일 분리
- 테스트 실패 시 원인 파악 전까지 진행하지 않음

### 계획/문제 해결
- 단계별 검증: 각 단계를 실제로 검증한 후 다음 단계 진행
- 실행 불가능한 검증이 필요하면 작업 중단 후 알림
- 같은 행동 3번 반복 시 멈추고 현재 상태 점검

## 사용법

### Claude Code
`~/.claude/CLAUDE.md`에 복사하거나 심볼릭 링크 생성:
```bash
ln -sf ~/llm-code-assistant-rules/claude/CLAUDE.md ~/.claude/CLAUDE.md
```

### Codex CLI
레포의 `codex/AGENTS.md`를 Codex 작업 디렉터리에 복사하거나 심볼릭 링크 생성:
```bash
ln -sf /path/to/codex/AGENTS.md /Users/juniq/codex/AGENTS.md
```

### 기타 도구
각 도구의 시스템 프롬프트 또는 설정 파일에 규칙 내용을 추가하세요.

## 기여
피드백과 제안 환영합니다. Issue나 PR을 남겨주세요.
