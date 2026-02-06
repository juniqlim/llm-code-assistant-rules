# LLM Code Assistant Rules

LLM 기반 코드 어시스턴트(Claude Code, Codex CLI, Gemini CLI 등)에 적용할 수 있는 규칙 모음입니다.

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

### 한글번역
- 번역 요구시 원문 핵심 단어를 (원문) 형태로 병기
- 필요한 부연설명을 생략하지 않음

### 웹 콘텐츠 가져오기
- WebFetch 실패 시 대안 → [web-fetch-fallback.md](web-fetch-fallback.md)

## 구조

```
├── claude/CLAUDE.md          # Claude Code 규칙
├── codex/AGENTS.md           # Codex CLI 규칙
├── gemini/gemini.md          # Gemini CLI 규칙
├── web-fetch-fallback.md     # WebFetch 실패 시 대안
└── README.md
```

## 사용법

### Claude Code
```bash
ln -sf ~/develop/code/juniqlim/llm-code-assistant-rules/claude/CLAUDE.md ~/.claude/CLAUDE.md
```

### Codex CLI
```bash
ln -sf ~/develop/code/juniqlim/llm-code-assistant-rules/codex/AGENTS.md ~/codex/AGENTS.md
```

### Gemini CLI
`~/.gemini/GEMINI.md`에서 규칙 파일을 참조하도록 설정합니다.

## 기여
피드백과 제안 환영합니다. Issue나 PR을 남겨주세요.
