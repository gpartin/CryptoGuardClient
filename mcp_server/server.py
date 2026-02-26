"""
CryptoGuard MCP Server — Model Context Protocol for Claude Desktop & AI Agents.

Per-transaction deterministic crypto validator powered by WaveGuard physics engine.
5 tools: validate_trade, scan_token, rug_check, search, health.

Transports
----------
- **stdio** (default) — add to Claude Desktop config
- **HTTP** — ``cryptoguard-mcp --http --port 3001``

Claude Desktop config
~~~~~~~~~~~~~~~~~~~~~
Add to ``~/.config/claude/claude_desktop_config.json``
(macOS/Linux) or ``%APPDATA%\\Claude\\claude_desktop_config.json`` (Windows)::

    {
      "mcpServers": {
        "cryptoguard": {
          "command": "uvx",
          "args": ["--from", "CryptoGuardClient", "cryptoguard-mcp"]
        }
      }
    }

Smithery / Glama config
~~~~~~~~~~~~~~~~~~~~~~~
::

    {
      "mcpServers": {
        "cryptoguard": {
          "url": "https://gpartin--cryptoguard-api-fastapi-app.modal.run/mcp",
          "transport": "http"
        }
      }
    }
"""

from __future__ import annotations

import os
import sys
import json
import argparse
from typing import Any, Dict, List, Optional

# ── Configuration ──────────────────────────────────────────────────────────

API_URL = os.environ.get(
    "CRYPTOGUARD_API_URL",
    "https://gpartin--cryptoguard-api-fastapi-app.modal.run",
)

# ── HTTP client ───────────────────────────────────────────────────────────

try:
    import requests

    _session = requests.Session()
except ImportError:
    _session = None  # type: ignore[assignment]


def _api_post(path: str, body: dict) -> dict:
    if _session is None:
        raise RuntimeError("requests library required: pip install requests")
    resp = _session.post(f"{API_URL}{path}", json=body, timeout=90)
    resp.raise_for_status()
    return resp.json()


def _api_get(path: str, params: dict | None = None) -> Any:
    if _session is None:
        raise RuntimeError("requests library required: pip install requests")
    resp = _session.get(f"{API_URL}{path}", params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


# ═══════════════════════════════════════════════════════════════════════════
# MCP Tool Definitions
# ═══════════════════════════════════════════════════════════════════════════

TOOLS = [
    {
        "name": "cryptoguard_validate_trade",
        "description": (
            "Validate a crypto trade BEFORE execution. Returns a verdict: "
            "PROCEED, CAUTION, or BLOCK. Runs 5 checks: peer anomaly scan "
            "via WaveGuard physics engine, self-history comparison, rug pull "
            "risk assessment, CEX/DEX price cross-check, and concentration "
            "risk analysis. Accepts token name, symbol, or contract address.\n\n"
            "Example: validate buying $500 of PEPE before executing."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "token": {
                    "type": "string",
                    "description": (
                        "Token to validate. Can be a name (bitcoin), "
                        "symbol (BTC), or contract address (0x...)."
                    ),
                },
                "action": {
                    "type": "string",
                    "enum": ["buy", "sell", "swap"],
                    "description": "Trade action type (default: buy).",
                },
                "chain": {
                    "type": "string",
                    "description": (
                        "Blockchain for contract address resolution "
                        "(ethereum, solana, base, bsc, polygon, avalanche, arbitrum)."
                    ),
                },
                "pair_address": {
                    "type": "string",
                    "description": "DEX pair address for rug pull check.",
                },
                "amount_usd": {
                    "type": "number",
                    "description": "Trade amount in USD for concentration risk analysis.",
                },
            },
            "required": ["token"],
        },
    },
    {
        "name": "cryptoguard_scan_token",
        "description": (
            "Scan a single token for anomalous market behavior using "
            "WaveGuard physics-based anomaly detection. Compares the token "
            "to TIER-MATCHED peers (microcaps vs microcaps, large-caps vs "
            "large-caps). Returns anomaly scores, risk level, and explanations.\n\n"
            "Example: scan 'solana' to check if its metrics are unusual."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "coin_id": {
                    "type": "string",
                    "description": "CoinGecko coin ID (e.g., 'bitcoin', 'solana', 'pepe').",
                },
                "sensitivity": {
                    "type": "number",
                    "description": (
                        "Anomaly sensitivity multiplier (default: 1.0). "
                        "Higher = more sensitive."
                    ),
                },
            },
            "required": ["coin_id"],
        },
    },
    {
        "name": "cryptoguard_rug_check",
        "description": (
            "Assess rug pull risk for a specific DEX trading pair. Scores "
            "6 risk factors (0-100): liquidity depth, pair age, volume/"
            "liquidity ratio, price action, buy/sell imbalance, and metadata.\n\n"
            "Example: check if a new Solana pair is a potential rug pull."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "chain": {
                    "type": "string",
                    "description": "Blockchain (solana, ethereum, base, bsc).",
                },
                "pair_address": {
                    "type": "string",
                    "description": "DEX pair contract address.",
                },
            },
            "required": ["chain", "pair_address"],
        },
    },
    {
        "name": "cryptoguard_search",
        "description": (
            "Search for a token's CoinGecko coin ID by name, symbol, or "
            "contract address. Use this first if you're unsure of the "
            "correct coin_id for scan_token or validate_trade.\n\n"
            "Example: search 'pepe' to find the correct coin ID."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Token name, symbol, or contract address to search.",
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "cryptoguard_health",
        "description": (
            "Check CryptoGuard API health, version, and service status. "
            "No payment required. Use this to verify the service is running."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
]


# ═══════════════════════════════════════════════════════════════════════════
# Tool Execution
# ═══════════════════════════════════════════════════════════════════════════


def execute_tool(name: str, arguments: dict) -> dict:
    """Execute an MCP tool and return the result."""
    try:
        if name == "cryptoguard_validate_trade":
            body = {"token": arguments["token"]}
            for key in ("action", "chain", "pair_address", "amount_usd"):
                if key in arguments:
                    body[key] = arguments[key]

            result = _api_post("/v1/validate-trade", body)

            verdict = result.get("verdict", "UNKNOWN")
            risk = result.get("risk_level", "UNKNOWN")
            score = result.get("risk_score", 0)
            rec = result.get("recommendation", "No recommendation")
            flags = result.get("flags", [])

            lines = [
                f"Verdict: {verdict} | Risk: {risk} (score: {score})",
                f"Recommendation: {rec}",
            ]
            if flags:
                lines.append(f"Flags: {', '.join(flags)}")

            checks = result.get("checks_performed", [])
            if checks:
                lines.append(f"Checks: {', '.join(checks)}")

            summary = "\n".join(lines)
            return {
                "content": [
                    {"type": "text", "text": summary},
                    {"type": "text", "text": json.dumps(result, indent=2, default=str)},
                ]
            }

        elif name == "cryptoguard_scan_token":
            coin_id = arguments["coin_id"].lower().strip()
            sensitivity = arguments.get("sensitivity", 1.0)
            result = _api_get(f"/v1/scan/{coin_id}", {"sensitivity": sensitivity})

            risk = result.get("risk_level", "UNKNOWN")
            rec = result.get("recommendation", "")
            anomalies = result.get("anomalies", [])

            lines = [f"Token: {coin_id} | Risk: {risk}"]
            if rec:
                lines.append(f"Recommendation: {rec}")
            if anomalies:
                for a in anomalies[:5]:
                    desc = a.get("description", a.get("label", "?"))
                    lines.append(f"  - {desc}")

            summary = "\n".join(lines)
            return {
                "content": [
                    {"type": "text", "text": summary},
                    {"type": "text", "text": json.dumps(result, indent=2, default=str)},
                ]
            }

        elif name == "cryptoguard_rug_check":
            chain = arguments["chain"]
            pair = arguments["pair_address"]
            result = _api_get(f"/v1/rug-check/{chain}/{pair}")

            risk = result.get("risk_level", "UNKNOWN")
            score = result.get("risk_score", 0)
            rec = result.get("recommendation", "")
            flags = result.get("flags", [])

            lines = [
                f"Rug Check: {result.get('token_symbol', '?')} on {chain}",
                f"Risk: {risk} (score: {score})",
            ]
            if rec:
                lines.append(f"Recommendation: {rec}")
            if flags:
                for f in flags[:5]:
                    lines.append(f"  Warning: {f}")

            summary = "\n".join(lines)
            return {
                "content": [
                    {"type": "text", "text": summary},
                    {"type": "text", "text": json.dumps(result, indent=2, default=str)},
                ]
            }

        elif name == "cryptoguard_search":
            query = arguments["query"]
            result = _api_get("/v1/search", {"q": query})

            if isinstance(result, list):
                lines = [f"Found {len(result)} results for '{query}':"]
                for r in result[:10]:
                    name_ = r.get("name", "?")
                    symbol = r.get("symbol", "?")
                    cid = r.get("coin_id", "?")
                    lines.append(f"  {name_} ({symbol}) -> coin_id: {cid}")
                summary = "\n".join(lines)
            else:
                summary = json.dumps(result, indent=2)

            return {"content": [{"type": "text", "text": summary}]}

        elif name == "cryptoguard_health":
            result = _api_get("/health")
            status = result.get("status", "?")
            version = result.get("version", "?")
            return {
                "content": [
                    {"type": "text", "text": f"Status: {status} | Version: {version}"},
                ]
            }

        else:
            return {
                "content": [{"type": "text", "text": f"Unknown tool: {name}"}],
                "isError": True,
            }

    except Exception as e:
        return {
            "content": [{"type": "text", "text": f"Error: {e}"}],
            "isError": True,
        }


# ═══════════════════════════════════════════════════════════════════════════
# MCP Protocol Handler (stdio JSON-RPC transport)
# ═══════════════════════════════════════════════════════════════════════════


class MCPStdioServer:
    """Minimal MCP server implementing JSON-RPC 2.0 over stdio."""

    def __init__(self) -> None:
        self.server_info = {
            "name": "cryptoguard",
            "version": "0.3.0",
        }

    def handle_message(self, msg: dict) -> Optional[dict]:
        """Process a JSON-RPC 2.0 message and return the response."""
        method = msg.get("method", "")
        msg_id = msg.get("id")
        params = msg.get("params", {})

        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {"listChanged": False},
                    },
                    "serverInfo": self.server_info,
                },
            }

        elif method == "notifications/initialized":
            return None

        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {"tools": TOOLS},
            }

        elif method == "resources/list":
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {"resources": []},
            }

        elif method == "prompts/list":
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {"prompts": []},
            }

        elif method == "tools/call":
            tool_name = params.get("name", "")
            arguments = params.get("arguments", {})
            result = execute_tool(tool_name, arguments)
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": result,
            }

        elif method == "ping":
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {},
            }

        else:
            if msg_id is not None:
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}",
                    },
                }
            return None

    def run_stdio(self) -> None:
        """Run the MCP server on stdin/stdout."""
        sys.stderr.write(
            f"CryptoGuard MCP server v0.3.0 started (API: {API_URL})\n"
        )
        sys.stderr.flush()

        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except json.JSONDecodeError as e:
                sys.stderr.write(f"Invalid JSON: {e}\n")
                sys.stderr.flush()
                continue

            response = self.handle_message(msg)
            if response is not None:
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()


# ═══════════════════════════════════════════════════════════════════════════
# HTTP transport (for remote MCP clients / Smithery / Glama)
# ═══════════════════════════════════════════════════════════════════════════


def run_http_server(port: int = 3001) -> None:
    """Run MCP over HTTP for remote agent access."""
    try:
        from fastapi import FastAPI as FA
        import uvicorn
    except ImportError:
        print("HTTP transport requires: pip install 'CryptoGuardClient[mcp]'")
        sys.exit(1)

    mcp_app = FA(title="CryptoGuard MCP Server", version="0.3.0")
    server = MCPStdioServer()

    @mcp_app.post("/mcp")
    async def mcp_endpoint(request: dict) -> dict:  # type: ignore[type-arg]
        return server.handle_message(request)  # type: ignore[return-value]

    @mcp_app.get("/mcp/tools")
    async def mcp_tools() -> dict:  # type: ignore[type-arg]
        return {"tools": TOOLS}

    print(f"CryptoGuard MCP HTTP server v0.3.0 on port {port}")
    uvicorn.run(mcp_app, host="0.0.0.0", port=port)


# ═══════════════════════════════════════════════════════════════════════════
# Entry point
# ═══════════════════════════════════════════════════════════════════════════


def main():
    """Entry point for ``cryptoguard-mcp`` console script."""
    parser = argparse.ArgumentParser(
        description="CryptoGuard MCP Server v0.3.0"
    )
    parser.add_argument(
        "--http",
        action="store_true",
        help="Use HTTP transport instead of stdio",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=3001,
        help="HTTP port (default: 3001)",
    )
    parser.add_argument(
        "--api-url",
        type=str,
        default=None,
        help="CryptoGuard API URL (overrides $CRYPTOGUARD_API_URL)",
    )
    args = parser.parse_args()

    global API_URL
    if args.api_url:
        API_URL = args.api_url

    if args.http:
        run_http_server(args.port)
    else:
        server = MCPStdioServer()
        server.run_stdio()


if __name__ == "__main__":
    main()
