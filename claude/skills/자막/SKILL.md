---
name: 자막
description: YouTube 자막(VTT) 다운로드 자동화. 사용자가 “/자막”, “유튜브 자막”, “vtt 자막 받아줘”, “자막 파일 뽑아줘”처럼 요청할 때 사용.
---

# YouTube 자막 다운로드

- `scripts/get_yt_subs.sh`를 사용해 자막(VTT)을 현재 디렉터리에 저장하라.
- 수동 자막을 먼저 시도하고 실패하면 자동 자막으로 폴백한다.
- 기본 언어는 `en`이며, 두 번째 인자로 언어 코드를 받을 수 있다.
- 출력 파일은 `%(title)s.vtt` 형식으로 저장된다.

## 빠른 사용

```bash
./scripts/get_yt_subs.sh "https://www.youtube.com/watch?v=..."
./scripts/get_yt_subs.sh "https://www.youtube.com/watch?v=..." ko
```

## 주의

- `yt-dlp`가 필요하다. 없으면 설치 후 진행하라.
