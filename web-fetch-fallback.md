# WebFetch 실패 시 대안

WebFetch 실패 시 아래 순서로 시도한다.

## 1. Python urllib로 가져오기

```bash
python3 -c "
import urllib.request, re, html
req = urllib.request.Request('URL', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    body = resp.read().decode('utf-8')
    text = re.sub(r'<[^>]+>', '', body)
    print(html.unescape(text))
"
```

## 2. 사이트별 API 활용

### X/Twitter

```bash
curl -sL "https://publish.twitter.com/oembed?url=트윗URL"
```
