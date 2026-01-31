---
name: 노트푸시
description: 현재 대화 내용을 note 리포지토리에 마크다운으로 저장하고 git push
---

# 노트 저장 및 푸시

1. 사용자가 지정한 내용(또는 직전 번역/정리한 내용)을 `/Users/juniq/develop/code/juniqlim/note/` 하위 폴더에 .md 파일로 저장
   - 프로그래밍 관련 → `programming/`
   - 투자 관련 → `investment/`
   - 파일명: `제목.md` 형식 (날짜 없이)
   - 내용 상단에 제목 포함
2. git add, commit, push 실행:
   ```
   cd /Users/juniq/develop/code/juniqlim/note && git add -A && git commit -m "Add: 파일명" && git push
   ```
3. 원본 파일(`/tmp/`에 있던 파일)을 삭제한다
