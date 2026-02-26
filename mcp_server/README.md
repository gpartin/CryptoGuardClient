# CryptoGuard MCP Server

The `mcp_server/` directory contains the Model Context Protocol server for CryptoGuard.

## Tools

| Tool | Description |
|------|-------------|
| `cryptoguard_validate_trade` | Validate a trade → PROCEED/CAUTION/BLOCK |
| `cryptoguard_scan_token` | Anomaly scan via WaveGuard physics engine |
| `cryptoguard_rug_check` | DEX pair rug pull risk assessment |
| `cryptoguard_search` | Search tokens by name/symbol/address |
| `cryptoguard_health` | Service health check |

## Usage

### stdio (Claude Desktop)

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

### HTTP (remote agents)

```bash
pip install CryptoGuardClient[mcp]
cryptoguard-mcp --http --port 3001
```
