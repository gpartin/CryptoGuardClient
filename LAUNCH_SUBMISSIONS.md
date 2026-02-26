# CryptoGuard Launch Submissions

## 1. awesome-mcp-servers PR

**Status**: ✅ SUBMITTED — PR #2440
**URL**: https://github.com/punkpeye/awesome-mcp-servers/pull/2440
**Date**: 2026-02-26
**Category**: Finance & Fintech

**Entry added:**

```markdown
- [gpartin/CryptoGuardClient](https://github.com/gpartin/CryptoGuardClient) 🐍 ☁️ - Per-transaction deterministic crypto validator for AI trading agents. Validate trades (PROCEED/CAUTION/BLOCK), scan tokens, detect rug pulls — powered by WaveGuard physics engine. 5 free calls/day, x402 USDC payments. `pip install CryptoGuardClient`
```

**PR Title:** `Add CryptoGuard - per-transaction crypto validator MCP server`

**PR Body:**

## CryptoGuard MCP Server

**Repository**: https://github.com/gpartin/CryptoGuardClient
**Install**: `pip install CryptoGuardClient`
**Category**: Finance & Fintech

### What it does

CryptoGuard is a per-transaction deterministic crypto validator for AI trading agents. It provides:

- **Trade Validation**: Validate trades with PROCEED / CAUTION / BLOCK verdicts
- **Token Scanning**: Deep token analysis (honeypot detection, liquidity analysis, holder distribution)
- **Rug Pull Detection**: Purpose-built rug pull checks with risk scoring
- **Token Search**: Search tokens across multiple DEXes

### MCP Integration

5 tools exposed via MCP (stdio + streamable HTTP):
- `cryptoguard_validate_trade` - Validate a trade decision
- `cryptoguard_scan_token` - Deep token analysis
- `cryptoguard_rug_check` - Rug pull detection
- `cryptoguard_search` - Token search
- `cryptoguard_health` - Health check

### Pricing

- **5 free calls/day** (no API key needed)
- Pay-per-call via x402 USDC payments (Base L2)
- Powered by WaveGuard physics engine

### Checklist

- [x] Public repository
- [x] README with install instructions
- [x] MCP server with stdio transport
- [x] `smithery.yaml` present
- [x] `server.json` present

---

## 2. Smithery

**Status**: ⏳ PENDING — requires manual web submission
**URL**: https://smithery.ai
**Action**: Go to smithery.ai → submit repo URL `https://github.com/gpartin/CryptoGuardClient`
**Config**: `smithery.yaml` already configured in repo root

---

## 3. Glama

**Status**: ⏳ PENDING — requires manual web submission
**URL**: https://glama.ai/mcp/servers
**Action**: Click "Add Server" → submit repo URL `https://github.com/gpartin/CryptoGuardClient`
**Config**: `server.json` already configured in repo root

---

## 4. PyPI

**Status**: ⏳ PENDING — trusted publisher not configured
**GitHub Release**: ✅ v0.3.0 created (https://github.com/gpartin/CryptoGuardClient/releases/tag/v0.3.0)
**Workflow**: `.github/workflows/publish.yml` triggered but failed (no trusted publisher)

**To complete:**
1. Go to https://pypi.org/manage/account/publishing/
2. Add new pending publisher:
   - **PyPI project name**: `CryptoGuardClient`
   - **Owner**: `gpartin`
   - **Repository**: `CryptoGuardClient`
   - **Workflow name**: `publish.yml`
   - **Environment**: `pypi`
3. Re-run the failed workflow:
   ```
   gh run rerun <run-id> --repo gpartin/CryptoGuardClient
   ```
   Or delete and recreate the v0.3.0 release to trigger a fresh run.

---

## 5. x402 Ecosystem PR

**Status**: ✅ SUBMITTED — PR #1358
**URL**: https://github.com/anthropics/x402/pull/1358
**Date**: 2026-02-26
**Branch**: `add-cryptoguard-ecosystem` in `gpartin/x402`
**Commit**: `b58bd0b` (GPG signed)

Added CryptoGuard to the x402 ecosystem directory.

---

## 6. Show HN Post

**Title:** `Show HN: CryptoGuard – Per-transaction crypto validator for AI trading agents (MCP + API)`

**Body:**

Hi HN,

I built a per-transaction deterministic crypto validator designed for AI trading agents. Before your agent executes a trade, it validates the decision through physics-based analysis and returns PROCEED / CAUTION / BLOCK.

**Why this exists:**
AI trading agents make decisions fast but can't evaluate token safety. CryptoGuard sits between the decision and execution — checking liquidity, holder concentration, honeypot risk, contract age, and dozens of other signals in one call.

**What it does:**
- **Trade Validation**: Send token + action + amount → get PROCEED/CAUTION/BLOCK + risk scores
- **Token Scanning**: Deep analysis (honeypot detection, liquidity depth, holder distribution, contract age)
- **Rug Pull Detection**: Purpose-built detector for pump-and-dump, honeypot, and abandonment patterns
- **Token Search**: Search across DEXes by name or address

**How it works:**
The engine runs on WaveGuard physics — data is encoded onto a lattice and propagated through coupled wave equations. Anomalous token patterns scatter differently from healthy ones. Deterministic: same input always produces same output.

**Integration options:**
1. **MCP tool** for Claude/AI agents (stdio or HTTP)
2. **Python SDK**: `pip install CryptoGuardClient`
3. **REST API**: Direct HTTP calls

**Pricing:**
- 5 free calls/day (no API key needed)
- Pay-per-call via x402 USDC payments (Base L2)
- No subscriptions, no monthly fees

```python
from cryptoguard import CryptoGuardClient
client = CryptoGuardClient()
result = client.validate_trade("SOL_ADDRESS", "buy", 500)
print(result["verdict"])  # PROCEED / CAUTION / BLOCK
```

GitHub: https://github.com/gpartin/CryptoGuardClient
API: https://gpartin--cryptoguard-api-fastapi-app.modal.run

---

## 7. Reddit r/CryptoCurrency Post

**Title:** `Built a per-transaction crypto validator for AI trading bots — checks tokens before your bot trades`

**Body:**

If you're running trading bots (especially on Solana/Base), here's a validator that checks every token before execution:

```python
from cryptoguard import CryptoGuardClient
client = CryptoGuardClient()

# Before your bot buys
result = client.validate_trade("TOKEN_ADDRESS", "buy", 500)
if result["verdict"] == "BLOCK":
    print(f"Blocked: {result['reasons']}")
    # Skip this trade
```

**What it checks:**
- Honeypot detection (can you actually sell?)
- Liquidity depth (enough to exit your position?)
- Holder concentration (whale risk?)
- Contract age (too new = risky)
- Rug pull patterns (pump-and-dump, abandonment)
- Overall risk score with PROCEED / CAUTION / BLOCK verdict

**Key features:**
- Deterministic (same input = same output, no ML randomness)
- 5 free calls/day, no API key needed
- Pay-per-call after that (USDC on Base, no subscriptions)
- Works as MCP tool if you're using Claude for trading analysis

Not financial advice, but it catches the obvious scams before your bot can YOLO into them.

`pip install CryptoGuardClient`
GitHub: https://github.com/gpartin/CryptoGuardClient

---

## 8. Reddit r/MCP Post

**Title:** `CryptoGuard MCP Server — Give Claude crypto trade validation with 5 tools`

**Body:**

Published a crypto validation MCP server. 5 tools for AI trading agent integration.

**Setup (30 seconds):**

```json
{
  "mcpServers": {
    "cryptoguard": {
      "command": "uvx",
      "args": ["CryptoGuardClient"]
    }
  }
}
```

**Then ask Claude:**
> "Should I buy this token: [address]? Check if it's safe first."

Claude calls `cryptoguard_validate_trade` and gets back PROCEED/CAUTION/BLOCK with risk scores.

**Five tools:**
- `cryptoguard_validate_trade` — Full trade validation with verdict
- `cryptoguard_scan_token` — Deep token analysis (honeypot, liquidity, holders)
- `cryptoguard_rug_check` — Rug pull detection with risk scoring
- `cryptoguard_search` — Find tokens across DEXes
- `cryptoguard_health` — API status

**Powered by WaveGuard physics engine** — deterministic, no ML, same input always gives same output.

Free tier: 5 calls/day, no API key. Pay-per-call via x402 USDC payments after.

PyPI: `pip install CryptoGuardClient`
GitHub: https://github.com/gpartin/CryptoGuardClient

---

## 9. Reddit r/algotrading Post

**Title:** `Per-transaction crypto validator API for algo trading bots — PROCEED/CAUTION/BLOCK verdicts`

**Body:**

Built a validator that sits between your trading bot's decision engine and execution layer. Before executing a trade, it validates the token:

**Flow:**
```
Bot decides to buy TOKEN_X
  → CryptoGuard.validate_trade(TOKEN_X, "buy", 500)
  → Returns: {verdict: "CAUTION", risk_score: 0.65, reasons: ["low liquidity", "high holder concentration"]}
  → Bot adjusts position size or skips
```

**What it analyzes per call:**
- Honeypot risk (can you exit the position?)
- Liquidity depth vs your intended position size
- Holder concentration (top 10 holders %)
- Contract age and deployment patterns
- Historical rug pull pattern matching

**API endpoints:**
| Endpoint | Purpose |
|----------|---------|
| `/validate` | Full trade validation |
| `/scan/{address}` | Deep token analysis |
| `/rug-check/{address}` | Rug pull detection |
| `/search?q=` | Token search |
| `/health` | API status |

**Integration:**
- Python SDK: `pip install CryptoGuardClient`
- REST API: Direct HTTP calls to Modal endpoint
- MCP: Plug into Claude for AI-assisted analysis

5 free calls/day. Pay-per-call after (USDC, Base L2).

GitHub: https://github.com/gpartin/CryptoGuardClient
