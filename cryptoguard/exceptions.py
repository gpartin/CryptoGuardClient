"""
CryptoGuard exception hierarchy.

All exceptions inherit from CryptoGuardError so you can catch them with a
single ``except CryptoGuardError`` block, or handle specific cases granularly.
"""

__all__ = [
    "CryptoGuardError",
    "AuthenticationError",
    "ValidationError",
    "RateLimitError",
    "PaymentRequiredError",
    "ServerError",
]


class CryptoGuardError(Exception):
    """Base exception for all CryptoGuard SDK errors.

    Attributes
    ----------
    message : str
        Human-readable error description.
    status_code : int
        HTTP status code (0 if not from an HTTP response).
    detail : str
        Raw error body from the API, if available.
    """

    def __init__(self, message: str, status_code: int = 0, detail: str = ""):
        self.message = message
        self.status_code = status_code
        self.detail = detail
        super().__init__(message)


class AuthenticationError(CryptoGuardError):
    """API key is invalid, expired, or missing (HTTP 401)."""
    pass


class ValidationError(CryptoGuardError):
    """Request data failed server-side validation (HTTP 422).

    Check ``detail`` for specifics (e.g. unknown token, invalid chain).
    """
    pass


class RateLimitError(CryptoGuardError):
    """Free tier limit exceeded (HTTP 429).

    You have used all 5 free calls for today. Either wait until
    tomorrow or use x402 payments for unlimited access.
    """
    pass


class PaymentRequiredError(CryptoGuardError):
    """x402 payment required (HTTP 402).

    Free tier exhausted. The response body contains x402 payment
    requirements (network, amount, wallet address).
    """
    pass


class ServerError(CryptoGuardError):
    """Internal server error (HTTP 5xx).

    Usually transient — retry after a short delay.
    """
    pass
