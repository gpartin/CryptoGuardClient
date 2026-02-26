"""Tests for CryptoGuardClient SDK."""

import pytest
from unittest.mock import patch, MagicMock
from cryptoguard import CryptoGuardClient
from cryptoguard.exceptions import (
    CryptoGuardError,
    PaymentRequiredError,
    RateLimitError,
    ServerError,
)


@pytest.fixture
def client():
    return CryptoGuardClient(base_url="http://test-api")


class TestClientInit:
    def test_default_url(self):
        c = CryptoGuardClient()
        assert "modal.run" in c.base_url

    def test_custom_url(self):
        c = CryptoGuardClient(base_url="http://localhost:8000")
        assert c.base_url == "http://localhost:8000"

    def test_trailing_slash_stripped(self):
        c = CryptoGuardClient(base_url="http://localhost:8000/")
        assert c.base_url == "http://localhost:8000"


class TestValidateTrade:
    @patch("cryptoguard.client.requests.Session")
    def test_validate_trade_basic(self, mock_session_cls, client):
        mock_resp = MagicMock()
        mock_resp.ok = True
        mock_resp.json.return_value = {
            "verdict": "PROCEED",
            "risk_score": 15,
            "risk_level": "LOW",
        }
        client._session.post = MagicMock(return_value=mock_resp)

        result = client.validate_trade("bitcoin")
        assert result["verdict"] == "PROCEED"
        client._session.post.assert_called_once()

    @patch("cryptoguard.client.requests.Session")
    def test_validate_trade_with_options(self, mock_session_cls, client):
        mock_resp = MagicMock()
        mock_resp.ok = True
        mock_resp.json.return_value = {"verdict": "CAUTION"}
        client._session.post = MagicMock(return_value=mock_resp)

        result = client.validate_trade(
            "solana", action="sell", amount_usd=5000, chain="solana"
        )
        assert result["verdict"] == "CAUTION"


class TestExceptions:
    def test_payment_required(self, client):
        mock_resp = MagicMock()
        mock_resp.ok = False
        mock_resp.status_code = 402
        mock_resp.reason = "Payment Required"
        mock_resp.text = '{"payment": "required"}'
        client._session.get = MagicMock(return_value=mock_resp)

        with pytest.raises(PaymentRequiredError):
            client.health()

    def test_rate_limit(self, client):
        mock_resp = MagicMock()
        mock_resp.ok = False
        mock_resp.status_code = 429
        mock_resp.reason = "Too Many Requests"
        mock_resp.text = "Rate limit exceeded"
        client._session.post = MagicMock(return_value=mock_resp)

        with pytest.raises(RateLimitError):
            client.validate_trade("bitcoin")

    def test_server_error(self, client):
        mock_resp = MagicMock()
        mock_resp.ok = False
        mock_resp.status_code = 500
        mock_resp.reason = "Internal Server Error"
        mock_resp.text = "Something broke"
        client._session.get = MagicMock(return_value=mock_resp)

        with pytest.raises(ServerError):
            client.health()


class TestFreeEndpoints:
    def test_search(self, client):
        mock_resp = MagicMock()
        mock_resp.ok = True
        mock_resp.json.return_value = [
            {"coin_id": "pepe", "name": "Pepe", "symbol": "PEPE"}
        ]
        client._session.get = MagicMock(return_value=mock_resp)

        result = client.search("pepe")
        assert len(result) == 1
        assert result[0]["coin_id"] == "pepe"

    def test_health(self, client):
        mock_resp = MagicMock()
        mock_resp.ok = True
        mock_resp.json.return_value = {"status": "ok", "version": "0.3.0"}
        client._session.get = MagicMock(return_value=mock_resp)

        result = client.health()
        assert result["status"] == "ok"
