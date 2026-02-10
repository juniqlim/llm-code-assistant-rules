# WebFetch 실패 시 대안

WebFetch 실패 시 아래 순서로 시도한다.

## 참고: CSR(Client-Side Rendering) 페이지

React, Vue, Next.js 등 모던 웹앱 대부분은 CSR이라 urllib/WebFetch로는 빈 HTML 껍데기만 온다. 대응 방법:

1. **API 직접 호출** (권장) - 브라우저 개발자도구 Network 탭에서 데이터 API URL을 찾아 호출. CSR 페이지도 데이터는 결국 API에서 가져오므로, URL만 알면 해결되는 경우가 많다.
2. **헤드리스 브라우저** (Selenium, Playwright) - JS를 실제 실행. 범용적이지만 무겁고 느림.

urllib 결과가 거의 비어있으면 CSR을 의심하고, API 직접 호출을 시도할 것.

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

단일 트윗:
```bash
curl -sL "https://publish.twitter.com/oembed?url=트윗URL"
```

타래(thread) 전체 읽기 - UnrollNow (로그인 불필요, SSR이라 urllib로 파싱 가능):
```bash
python3 -c "
import urllib.request, re, html
url = 'https://unrollnow.com/status/트윗ID'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    body = resp.read().decode('utf-8')
    for m in re.findall(r'<(?:article|section)[^>]*>(.*?)</(?:article|section)>', body, re.DOTALL):
        text = html.unescape(re.sub(r'<[^>]+>', ' ', m)).strip()
        if len(text) > 10:
            print(text)
"
```

### 네이버 증권 (모바일)

CSR이라 urllib로는 빈 껍데기만 옴. API 직접 호출 필요.

- 국내주식: `https://api.stock.naver.com/stock/{종목코드}/basic` (예: 005930)
- 해외주식: `https://api.stock.naver.com/stock/{로이터코드}/basic` (예: NFLX.O)

```bash
python3 -c "
import urllib.request, json
url = 'https://api.stock.naver.com/stock/NFLX.O/basic'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    print(json.dumps(data, indent=2, ensure_ascii=False))
"
```

### Stockrow (재무 데이터)

CSR + GraphQL(Apollo Client) 사이트. urllib로는 빈 껍데기만 옴.

- GraphQL 엔드포인트: `https://stockrow.com/graphql`
- **Origin/Referer 헤더 필수** (없으면 403)
- 일부 데이터는 유료 구독 필요 (`‡‡‡‡‡`로 마스킹됨)

주요 쿼리:
- `GetKeystats($shortcode)` - financials, revenueTable, epsTable, targetPrice, annualGrowth 등
- `GetDescriptor($shortcode)` - businessProfile, sectorName, industryName

```bash
python3 << 'PYEOF'
import urllib.request, json

def gql(query, variables={}):
    data = json.dumps({"query": query, "variables": variables}).encode('utf-8')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Content-Type': 'application/json',
        'Origin': 'https://stockrow.com',
        'Referer': 'https://stockrow.com/',
    }
    req = urllib.request.Request('https://stockrow.com/graphql', data=data, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

# 종목코드(shortcode)만 바꿔서 사용
result = gql(
    "query GetKeystats($shortcode: String!) { keystats(shortcode: $shortcode) { financials revenueTable epsTable targetPrice recommendationRating annualGrowth } }",
    {"shortcode": "NFLX"}
)
print(json.dumps(result, indent=2, ensure_ascii=False))
PYEOF
```
