---
name: 노트푸시
description: 현재 대화 내용을 note 리포지토리에 마크다운으로 저장하고 git push
---

# 노트 저장 및 푸시

1. 사용자가 지정한 내용(또는 직전 번역/정리한 내용)을 `/Users/juniq/develop/code/juniqlim/note/` 하위 폴더에 .md 파일로 저장
   - 프로그래밍 관련 → `programming/` 하위
   - 에이전틱 코딩 관련 → `ai-agent/` 하위
   - 투자 관련 → `investment/` 하위
   - 파일명: `영문-제목.md` 형식 (날짜 없이, 소문자 사용, 단어는 -로 연결)
   - 내용 상단에 제목 포함
2. git add, commit, push 실행:
   ```bash
   cd /Users/juniq/develop/code/juniqlim/note && git add -A && git commit -m "Add: 파일명" && git push
   ```
3. 작업에 사용된 임시 파일이 있다면 삭제한다.
