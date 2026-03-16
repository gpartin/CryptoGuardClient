# CryptoGuard

**Crypto risk scanner that detected every major crash in backtesting — 27 days early, on average.**

Scan any token by name, ticker, or contract address. Get a deterministic verdict: **PROCEED / CAUTION / BLOCK**.

**Version**: 0.5.0 &nbsp;|&nbsp; **Live API**: [`https://gpartin--cryptoguard-api-fastapi-app.modal.run`](https://gpartin--cryptoguard-api-fastapi-app.modal.run/health) &nbsp;|&nbsp; **Free tier**: 5 calls/day &nbsp;|&nbsp; **MCP**: 5 tools

---

## Backtest Results

Tested against 7 historical crypto crashes (LUNA, FTX, Celsius, 3AC, UST, SOL/FTX, TITAN) and 4 calm-market control periods. Full methodology and data: [CryptoGuard backtest](https://github.com/gpartin/CryptoGuard/tree/main/backtest).

| Method | Recall | Avg Lead Time | False Positive Rate |
|--------|--------|---------------|---------------------|
| **CryptoGuard (WaveGuard engine)** | **100% (7/7)** | **27.4 days** | **6.1%** |
| Z-score baseline | 100% (7/7) | 28.4 days | 29.9% |
| Rolling volatility | 86% (6/7) | 15.5 days | 4.0% |

**5× fewer false alarms** than statistical baselines with the same recall.

### Example: FTX Collapse (November 2022)

On **October 16, 2022**, FTT was trading at $23.73. Z-score analysis saw nothing (score 1.20, PROCEED).

**CryptoGuard flagged CAUTION** (anomaly score 4.72). The next day it escalated to BLOCK.

**23 days later**, FTX collapsed. FTT fell 94%.

---

## Install

```bash
pip install CryptoGuardClient
```

## Quick Start

```python
from cryptoguard import CryptoGuardClient

client = CryptoGuardClient()

# Validate a trade — primary use case
result = client.validate_trade("bitcoin", action="buy", amount_usd=1000)
print(result["verdict"])  # PROCEED / CAUTION / BLOCK

# Scan a token
scan = client.scan("solana")
print(scan["risk_level"])

# Rug pull check
rug = client.rug_check("solana", "0xabc123...")
print(rug["risk_score"])

# Check free tier remaining
print(client.free_tier())
```

## Primary Endpoint

```bash
curl -X POST https://gpartin--cryptoguard-api-fastapi-app.modal.run/v1/validate-trade \
  -H "Content-Type: application/json" \
  -d '{"token": "solana", "action": "buy", "amount_usd": 500}'
```

First 5 calls/day are free. After that: **$0.05/call** via [x402](https://github.com/coinbase/x402) USDC, or via [RapidAPI](https://rapidapi.com/).

## MCP Integration (Claude Desktop / AI Agents)

CryptoGuard is an MCP server with 5 tools. Works with Claude Desktop, Cursor, or any MCP client.

### Option 1: Remote HTTP (no install)

```json
{
  "mcpServers": {
    "cryptoguard": {
      "url": "https://gpartin--cryptoguard-api-fastapi-app.modal.run/mcp",
      "transport": "http"
    }
  }
}
```

### Option 2: uvx

```json
{
  "mcpServers": {
    "cryptoguard": {
      "command": "uvx",
      "args": ["--from", "CryptoGuardClient", "cryptoguard-mcp"]
    }
  }
}
```

### Option 3: pip install

```json
{
  "mcpServers": {
    "cryptoguard": {
      "command": "python",
      "args": ["-m", "mcp_server.server"]
    }
  }
}
```

### MCP Tools

| Tool | Description |
|------|-------------|
| `cryptoguard_validate_trade` | Validate a trade → PROCEED / CAUTION / BLOCK |
| `cryptoguard_scan_token` | Anomaly scan for any token |
| `cryptoguard_rug_check` | DEX pair rug pull risk assessment |
| `cryptoguard_search` | Search tokens by name/symbol/address |
| `cryptoguard_health` | Service health check |

## All Endpoints

| Method | Endpoint | Price | Description |
|--------|----------|-------|-------------|
| POST | `/v1/validate-trade` | 5 free/day, then $0.05 | **Primary** — single verdict for AI agents |
| POST | `/v1/validate-trades` | 5 free/day, then $0.05 | Batch validate up to 20 trades |
| GET | `/v1/scan/{coin_id}` | 5 free/day, then $0.05 | Single token anomaly scan |
| POST | `/v1/portfolio/scan` | 5 free/day, then $0.05 | Portfolio batch scan (up to 50 tokens) |
| GET | `/v1/scan/{coin_id}/history` | 5 free/day, then $0.05 | Historical self-comparison |
| GET | `/v1/rug-check/{chain}/{pair_address}` | 5 free/day, then $0.05 | Rug pull risk assessment |
| GET | `/v1/dex/new-pairs` | 5 free/day, then $0.05 | New DEX pair discovery |
| POST | `/mcp` | Free | MCP endpoint (JSON-RPC 2.0) |
| GET | `/v1/free-tier` | Free | Check remaining free calls |
| GET | `/v1/search?q=...` | Free | Search tokens by name |
| GET | `/v1/pricing` | Free | Pricing details |

| GET | `/health` | Free | Health check |

## How It Works

1. **Resolves** token input — CoinGecko ID, ticker symbol, or contract address (7 chains)
2. **Fetches** live market data from CoinGecko + DexScreener
3. **Builds baseline** from tier-matched peers (microcaps vs microcaps, large caps vs large caps)
4. **Extracts** 10 time-series features per day (price ratios, volume dynamics, momentum, volatility)
5. **Runs anomaly detection** — GPU-accelerated WaveGuard engine scores each token against its peer baseline
6. **Multi-check pipeline**: peer scan + rug pull + history + CEX/DEX spread + concentration risk
7. **Returns verdict**: PROCEED / CAUTION / BLOCK with anomaly scores and top contributing features

<details>
<summary><strong>About the detection engine</strong></summary>

CryptoGuard's core scanner is powered by [WaveGuard](https://github.com/gpartin/WaveGuardClient), a general-purpose anomaly detection engine that uses GPU-accelerated wave simulations instead of machine learning. Your token's feature vector is encoded onto a 3D lattice and evolved through coupled wave equations. Normal data produces stable wave patterns; anomalous data produces divergent ones.

The advantage over statistical methods: WaveGuard captures non-linear interactions between features that simple threshold checks miss. This is why it flagged FTT 13 days before z-score analysis in backtesting.

No model training, no drift, no retraining. Deterministic for the same input.

</details>

## Key Features (v0.5.0)

- **Backtested**: 100% recall on 7 historical crashes with 27-day average lead time
- **Free tier**: 5 calls/day per IP, no signup required
- **2 payment options**: x402 USDC per-scan ($0.05) or RapidAPI plans
- **Deterministic**: Same input always produces same verdict
- **MCP server**: 5 tools for AI agent integration (stdio + HTTP)
- **Python SDK**: `pip install CryptoGuardClient` with typed exceptions
- **Contract resolution**: Accepts name, ticker, or contract address across 7 chains
- **Batch validation**: Up to 20 trades or 50 tokens per call
- **Rug pull detection**: DexScreener-powered liquidity and holder analysis

## Pricing

| Tier | Cost | Limit | Auth |
|------|------|-------|------|
| **Free** | $0 | 5 calls/day per IP | None |
| **Per-scan** | $0.05/call | Unlimited | [x402](https://github.com/coinbase/x402) USDC micropayment |
| **RapidAPI Basic** | $0/mo | 500K requests | [RapidAPI](https://rapidapi.com/) proxy key |
| **RapidAPI Pro** | $9.99/mo | 10K requests | [RapidAPI](https://rapidapi.com/) proxy key |
| **RapidAPI Ultra** | $29.99/mo | 100K requests | [RapidAPI](https://rapidapi.com/) proxy key |

## Architecture

```
AI Agent / User
    |
    v
CryptoGuard API (Modal, stateless)
    |-- MCP endpoint (5 tools, JSON-RPC 2.0)
    |-- Auth: RapidAPI → API key → x402 (USDC) → Free tier
    |-- Token resolution (name/ticker/address → CoinGecko ID, 7 chains)
    |-- Market data (CoinGecko + DexScreener, cached)
    +-- WaveGuard anomaly engine (GPU-accelerated)
```

## License

MIT
