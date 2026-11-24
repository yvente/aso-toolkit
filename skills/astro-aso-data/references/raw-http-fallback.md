# Raw-HTTP fallback for Astro MCP

Use only when `mcp__astro__*` tools are not registered in the session and the user explicitly asks to proceed without restarting. The endpoint and settings come from `~/.zcode/cli/config.json` → `mcp.servers.astro` (default `http://127.0.0.1:8089/mcp`, Streamable HTTP, no auth, localhost-only, rate limit ~60 req/min).

Minimal Python handshake + call, no third-party deps:

```python
import json, urllib.request, urllib.error

BASE = 'http://127.0.0.1:8089/mcp'
HDRS = {'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream'}

def post(payload, session=None):
    h = dict(HDRS)
    if session: h['mcp-session-id'] = session
    req = urllib.request.Request(BASE, data=json.dumps(payload).encode(), headers=h, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.headers.get('mcp-session-id'), r.headers.get('content-type', ''), r.read().decode()
    except urllib.error.HTTPError as e:
        return None, (e.headers.get('content-type','') if e.headers else ''), e.read().decode()

def parse(ctype, body):
    # Responses may be JSON or SSE; SSE carries the payload in the last `data:` line.
    if 'text/event-stream' in ctype:
        data = [l[5:].strip() for l in body.splitlines() if l.startswith('data:')]
        return json.loads(data[-1]) if data else None
    return json.loads(body) if body.strip() else None

# 1) initialize -> keep the mcp-session-id response header
sid, ct, body = post({"jsonrpc":"2.0","id":1,"method":"initialize","params":{
    "protocolVersion":"2025-03-26","capabilities":{},
    "clientInfo":{"name":"manual-client","version":"0.1"}}})
# 2) initialized notification (same session id)
post({"jsonrpc":"2.0","method":"notifications/initialized"}, sid)
# 3) tools/list, then tools/call with the same session id
_, ct, body = post({"jsonrpc":"2.0","id":2,"method":"tools/list"}, sid)
tools = parse(ct, body)
_, ct, body = post({"jsonrpc":"2.0","id":3,"method":"tools/call","params":{
    "name":"get_app_keywords","arguments":{"appId":"<APP_STORE_ID>","store":"us","platform":"iphone"}}}, sid)
result = parse(ct, body)
text = '\n'.join(c.get('text','') for c in result['result']['content'] if c.get('type')=='text')
```

Gotchas learned the hard way:

- Each new process is a new MCP session: re-run initialize in every script; session IDs do not survive across processes reliably.
- `search_app_store` requires the parameter name `keyword` (not `term`/`query`).
- Result objects carry `appStoreId`, `ranking`, `bundleId`, `developer`, `ratingCount` — identify apps by `appStoreId` only (see SKILL.md identity rule).
- Stay under the rate limit when batching; sleep ~1s between heavy calls.
