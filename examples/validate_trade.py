"""Validate a single trade — the primary CryptoGuard use case."""

from cryptoguard import CryptoGuardClient

client = CryptoGuardClient()

# Validate buying Bitcoin
result = client.validate_trade("bitcoin", action="buy", amount_usd=1000)
print(f"Verdict: {result['verdict']}")
print(f"Risk: {result.get('risk_level', 'N/A')} (score: {result.get('risk_score', 'N/A')})")
print(f"Recommendation: {result.get('recommendation', 'N/A')}")

if result.get("flags"):
    print(f"Flags: {', '.join(result['flags'])}")
