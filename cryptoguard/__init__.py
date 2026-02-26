"""
CryptoGuard — Per-transaction deterministic crypto validator SDK.

Quick start::

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
"""

from .client import (  # noqa: F401
    CryptoGuardClient,
    __version__,
)
from .exceptions import (  # noqa: F401
    CryptoGuardError,
    AuthenticationError,
    ValidationError,
    RateLimitError,
    PaymentRequiredError,
    ServerError,
)

__all__ = [
    # Client
    "CryptoGuardClient",
    # Exceptions
    "CryptoGuardError",
    "AuthenticationError",
    "ValidationError",
    "RateLimitError",
    "PaymentRequiredError",
    "ServerError",
    # Meta
    "__version__",
]
