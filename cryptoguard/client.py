"""
CryptoGuard Python Client
==========================

Per-transaction deterministic crypto validator — powered by WaveGuard physics engine.

Usage::

    from cryptoguard import CryptoGuardClient

    client = CryptoGuardClient()

    # Validate a trade
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
"""

from __future__ import annotations

from typing import Any, List, Optional

import requests

from .exceptions import (
    CryptoGuardError,
    AuthenticationError,
    ValidationError,
    RateLimitError,
    PaymentRequiredError,
    ServerError,
)

__version__ = "0.3.0"

_STATUS_MAP = {
    401: AuthenticationError,
    402: PaymentRequiredError,
    422: ValidationError,
    429: RateLimitError,
}


class CryptoGuardClient:
    """Python client for the CryptoGuard API.

    Args:
        base_url: API base URL. Defaults to the hosted Modal endpoint.
        timeout: Request timeout in seconds.

    Example::

        client = CryptoGuardClient()
        result = client.validate_trade("bitcoin", action="buy", amount_usd=1000)
        print(result["verdict"])
    """

    DEFAULT_URL = "https://gpartin--cryptoguard-api-fastapi-app.modal.run"

    def __init__(
        self,
        base_url: str | None = None,
        timeout: int = 90,
    ) -> None:
        self.base_url = (base_url or self.DEFAULT_URL).rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()

    # ── Internal helpers ──────────────────────────────────────────────

    def _handle_error(self, resp: requests.Response) -> None:
        """Raise a typed exception for non-2xx responses."""
        if resp.ok:
            return
        exc_cls = _STATUS_MAP.get(resp.status_code, None)
        detail = ""
        try:
            detail = resp.text
        except Exception:
            pass
        if exc_cls:
            raise exc_cls(
                f"HTTP {resp.status_code}: {resp.reason}",
                status_code=resp.status_code,
                detail=detail,
            )
        if resp.status_code >= 500:
            raise ServerError(
                f"HTTP {resp.status_code}: {resp.reason}",
                status_code=resp.status_code,
                detail=detail,
            )
        raise CryptoGuardError(
            f"HTTP {resp.status_code}: {resp.reason}",
            status_code=resp.status_code,
            detail=detail,
        )

    def _get(self, path: str, params: dict | None = None) -> Any:
        resp = self._session.get(
            f"{self.base_url}{path}",
            params=params,
            timeout=self.timeout,
        )
        self._handle_error(resp)
        return resp.json()

    def _post(self, path: str, body: dict) -> Any:
        resp = self._session.post(
            f"{self.base_url}{path}",
            json=body,
            timeout=self.timeout,
        )
        self._handle_error(resp)
        return resp.json()

    # ── Core endpoints (paid after free tier) ─────────────────────────

    def validate_trade(
        self,
        token: str,
        action: str = "buy",
        chain: str | None = None,
        pair_address: str | None = None,
        amount_usd: float | None = None,
        sensitivity: float | None = None,
    ) -> dict:
        """Validate a crypto trade before execution.

        Returns a dict with verdict (PROCEED/CAUTION/BLOCK),
        risk_score, risk_level, flags, and recommendation.

        Args:
            token: Token name, symbol, or contract address.
            action: Trade action — "buy", "sell", or "swap".
            chain: Blockchain for contract address resolution.
            pair_address: DEX pair address for rug pull check.
            amount_usd: Trade amount in USD for concentration risk.
            sensitivity: Anomaly sensitivity multiplier.
        """
        body: dict = {"token": token, "action": action}
        if chain:
            body["chain"] = chain
        if pair_address:
            body["pair_address"] = pair_address
        if amount_usd is not None:
            body["amount_usd"] = amount_usd
        if sensitivity is not None:
            body["sensitivity"] = sensitivity
        return self._post("/v1/validate-trade", body)

    def validate_trades(self, trades: list[dict]) -> dict:
        """Validate multiple trades in one call (max 20).

        Each trade dict should have at minimum ``{"token": "..."}``.
        """
        return self._post("/v1/validate-trades", {"trades": trades})

    def scan(
        self,
        coin_id: str,
        sensitivity: float = 1.0,
    ) -> dict:
        """Scan a token for anomalous market behavior.

        Compares to tier-matched peers via WaveGuard physics engine.

        Args:
            coin_id: CoinGecko coin ID (e.g., "bitcoin", "solana").
            sensitivity: Anomaly sensitivity multiplier.
        """
        return self._get(f"/v1/scan/{coin_id}", {"sensitivity": sensitivity})

    def scan_portfolio(
        self,
        coin_ids: list[str],
        sensitivity: float = 1.0,
    ) -> dict:
        """Scan multiple tokens in a single batch.

        Args:
            coin_ids: List of CoinGecko coin IDs (up to 50).
            sensitivity: Anomaly sensitivity multiplier.
        """
        return self._post(
            "/v1/portfolio/scan",
            {"coin_ids": coin_ids, "sensitivity": sensitivity},
        )

    def scan_history(self, coin_id: str, days: int = 30) -> dict:
        """Compare a token to its own recent history.

        Args:
            coin_id: CoinGecko coin ID.
            days: Number of days of history to compare.
        """
        return self._get(f"/v1/scan/{coin_id}/history", {"days": days})

    def rug_check(self, chain: str, pair_address: str) -> dict:
        """Assess rug pull risk for a DEX trading pair.

        Args:
            chain: Blockchain (solana, ethereum, base, bsc, etc.).
            pair_address: DEX pair contract address.
        """
        return self._get(f"/v1/rug-check/{chain}/{pair_address}")

    def new_pairs(
        self,
        chain: str | None = None,
        min_liquidity: float = 1000,
        max_age_hours: float = 24,
    ) -> dict:
        """Discover new DEX pair launches.

        Args:
            chain: Filter by blockchain (optional).
            min_liquidity: Minimum liquidity in USD.
            max_age_hours: Maximum pair age in hours.
        """
        params: dict = {
            "min_liquidity": min_liquidity,
            "max_age_hours": max_age_hours,
        }
        if chain:
            params["chain"] = chain
        return self._get("/v1/dex/new-pairs", params)

    # ── Free endpoints ────────────────────────────────────────────────

    def search(self, query: str) -> list[dict]:
        """Search for tokens by name, symbol, or contract address.

        Args:
            query: Search term.
        """
        return self._get("/v1/search", {"q": query})

    def dex_search(self, query: str) -> list[dict]:
        """Search DexScreener for trading pairs.

        Args:
            query: Search term.
        """
        return self._get("/v1/dex/search", {"q": query})

    def health(self) -> dict:
        """Check service health."""
        return self._get("/health")

    def pricing(self) -> dict:
        """Get pricing information."""
        return self._get("/v1/pricing")

    def free_tier(self) -> dict:
        """Check free tier remaining calls for today."""
        return self._get("/v1/free-tier")

    def stats(self) -> dict:
        """Get service statistics."""
        return self._get("/v1/stats")
