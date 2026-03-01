---
name: recap
description: /clear 후 이전 대화 맥락을 빠르게 복구한다. 같은 프로젝트의 최근 세션에서 마지막 3문답을 읽어 요약한다.
---

# 이전 대화 맥락 복구

## 프로젝트 세션 디렉토리 특정
`~/.claude/projects/` 하위에서 현재 작업 디렉토리에 대응하는 폴더를 찾는다.
경로의 `/`를 `-`로 치환한 패턴 (예: `-Users-juniq-develop-code-project`)

## 세션 선택
아래 스크립트로 최근 세션 5개의 첫 번째 user 메시지를 목록으로 보여준다 (현재 세션 = 가장 최근 파일은 제외):

```bash
python3 << 'PYEOF'
import json, glob, os

project_dir = "PROJECT_DIR_PLACEHOLDER"
files = sorted(glob.glob(os.path.join(project_dir, "*.jsonl")), key=os.path.getmtime, reverse=True)

# 가장 최근 파일(현재 세션) 제외
for i, f in enumerate(files[1:6], 1):
    fname = os.path.basename(f)
    sid = fname.replace(".jsonl", "")
    mtime = os.path.getmtime(f)
    from datetime import datetime
    ts = datetime.fromtimestamp(mtime).strftime("%m/%d %H:%M")
    first_msg = ""
    with open(f) as fh:
        for line in fh:
            obj = json.loads(line)
            if obj.get("type") == "user":
                content = obj.get("message", {}).get("content", "")
                if isinstance(content, list):
                    content = " ".join(c.get("text","") for c in content if isinstance(c, dict) and c.get("type") == "text")
                content = content.strip()
                if content and not content.startswith("[Request interrupted") and not content.startswith("<"):
                    first_msg = content[:80]
                    break
    print(f"{i}. [{ts}] {first_msg}")
    print(f"   ID: {sid}")
PYEOF
```

- 인자 없이 `/recap` 실행 시 → 위 목록을 보여주고 AskUserQuestion으로 선택하게 한다.
- `/recap 1` 또는 `/recap <세션ID앞8자리>` → 해당 세션을 바로 선택한다.

## 맥락 추출
선택된 세션의 JSONL에서 마지막 user 메시지 3개를 추출한다:

```bash
python3 << 'PYEOF'
import json

target = "TARGET_JSONL_PATH"
users = []
with open(target) as f:
    for line in f:
        obj = json.loads(line)
        if obj.get("type") == "user":
            content = obj.get("message", {}).get("content", "")
            if isinstance(content, list):
                content = " ".join(c.get("text","") for c in content if isinstance(c, dict) and c.get("type") == "text")
            content = content.strip()
            if content and not content.startswith("[Request interrupted") and not content.startswith("<"):
                users.append(content[:500])

for msg in users[-3:]:
    print("USER:", msg)
    print()
PYEOF
```

## 요약
추출한 내용을 바탕으로 간결하게 요약한다:
- 무엇을 하고 있었는지
- 마지막으로 무엇을 요청했는지
- 현재 상태 (완료/진행중)
