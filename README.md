# CryptoGuard

**Per-crypto-transaction deterministic validator for AI trading agents.**

Powered by [WaveGuard](https://github.com/gpartin/WaveGuardClient) physics engine. Scan any token (by name, ticker, or contract address) and get a single deterministic verdict: **PROCEED / CAUTION / BLOCK**.

**Version**: 0.3.0
**Live API**: `https://gpartin--cryptoguard-api-fastapi-app.modal.run`
**Free tier**: 5 calls/day (no payment or signup required)
**MCP**: 5 tools via stdio or HTTP

## Install

```bash
pip install CryptoGuardClient
```

## Quick Start

```python
from cryptoguard import CryptoGuardClient

client = CryptoGuardClient()

# Validate a trade (primary use case)
result = client.validate_trade("bitcoin", action="buy", amount_usd=1000)
print(result["verdict"])  # PROCEED / CAUTION / BLOCK

# Scan a token
scan = client.scan("solana")
print(scan["risk_level"])

# Rug pull check
rug = client.rug_check("solana", "0xabc123...")
print(rug["risk_score"])

# Search tokens
tokens = client.search("pepe")
for t in tokens:
    print(t["coin_id"], t["name"])

# Check free tier remaining
print(client.free_tier())
```

## Primary Endpoint: Validate Trade

```bash
curl -X POST https://gpartin--cryptoguard-api-fastapi-app.modal.run/v1/validate-trade \
  -H "Content-Type: application/json" \
  -d '{"token": "solana", "action": "buy", "amount_usd": 500}'
```

First 5 calls/day are free. After that, x402 payment ($0.05/call) required.

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
| GET | `/mcp/tools` | Free | List MCP tools |
| GET | `/v1/free-tier` | Free | Check remaining free calls |
| GET | `/v1/search?q=...` | Free | Search tokens by name |
| GET | `/v1/dex/search?q=...` | Free | Search DEX pairs |
| GET | `/v1/pricing` | Free | Pricing details |
| GET | `/v1/stats` | Free | Service statistics |
| GET | `/health` | Free | Health check |

## MCP Integration (Claude Desktop / AI Agents)

CryptoGuard is an MCP server with 5 tools. Connect via stdio or HTTP.

### Option 1: uvx (recommended)

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

### Option 2: pip install

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

### Option 3: Remote HTTP (no install)

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

### MCP Tools

| Tool | Description |
|------|-------------|
| `cryptoguard_validate_trade` | Validate a trade → PROCEED/CAUTION/BLOCK |
| `cryptoguard_scan_token` | Anomaly scan via WaveGuard physics engine |
| `cryptoguard_rug_check` | DEX pair rug pull risk assessment |
| `cryptoguard_search` | Search tokens by name/symbol/address |
| `cryptoguard_health` | Service health check |

## How It Works

1. **Resolves** token input — CoinGecko ID, ticker symbol, or contract address (7 chains)
2. **Fetches** live market data from CoinGecko + DexScreener
3. **Builds baseline** from tier-matched peers (microcaps vs microcaps)
4. **Normalizes** to 7 ratio-based features (scale-invariant)
5. **Runs WaveGuard** physics-based anomaly detection (chi-field wave simulation)
6. **Multi-check pipeline**: peer scan + rug pull + history + CEX/DEX spread + concentration risk
7. **Returns verdict**: PROCEED / CAUTION / BLOCK

## Key Features (v0.3.0)

- **Free tier**: 5 calls/day per IP, no payment or signup required
- **Deterministic verdicts**: PROCEED/CAUTION/BLOCK with engine identification
- **MCP server**: 5 tools for AI agent integration (stdio + HTTP)
- **Python SDK**: `pip install CryptoGuardClient` with typed exceptions
- **Contract address resolution**: Auto-resolved across 7 chains
- **Batch validation**: Up to 20 trades in one call
- **Rug pull detection**: DexScreener-powered risk scoring
- **x402 payments**: USDC micropayments after free tier ($0.05/call)

## Pricing

| Tier | Cost | Limit |
|------|------|-------|
| **Free** | $0 | 5 calls/day per IP |
| **Paid** | $0.05/call | Unlimited (x402 USDC) |

Check remaining free calls: `GET /v1/free-tier` or `client.free_tier()`

### x402 Payment Protocol

After free tier, CryptoGuard uses [x402](https://github.com/coinbase/x402) for USDC micropayments.

1. Call paid endpoint without payment → HTTP 402 with payment requirements
2. x402 client signs USDC payment, retries with `PAYMENT-SIGNATURE` header
3. CryptoGuard verifies + settles → returns response

**Networks**: Base, Ethereum, Polygon, Arbitrum, Optimism

## Architecture

```
AI Agent / User
    |
    v
CryptoGuard API (Modal, CPU-only, stateless)
    |-- MCP endpoint (JSON-RPC 2.0, 5 tools)
    |-- Free tier (5 calls/day per IP)
    |-- x402 payment (USDC micropayments)
    |-- Token Resolution (contract -> CoinGecko ID, 7 chains)
    |-- CoinGecko API (market data, cached)
    |-- DexScreener API (DEX pairs, rug pull data)
    +-- WaveGuard API ($0.01/scan)
        +-- Physics engine: chi-field wave simulation (GPU)
```

## License

MIT
