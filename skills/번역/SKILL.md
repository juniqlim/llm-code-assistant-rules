---
name: 번역
description: URL의 웹 페이지를 가져와서 한국어 마크다운 파일로 저장
---

# 웹 페이지 → 한국어 마크다운 변환

1. URL의 웹 페이지 내용을 가져온다 (WebFetch 실패 시 `curl -sL "https://web.archive.org/web/2025/URL"` 사용)
2. 본문을 한국어로 번역한다
3. `/tmp/` 에 `영문-제목.md` 파일로 즉시 저장한다 (원문의 영문 제목을 소문자로, 단어는 -로 연결, 번역 완료 후 바로 Write 도구 사용)
