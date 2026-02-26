"""Scan an entire portfolio of tokens."""

from cryptoguard import CryptoGuardClient

client = CryptoGuardClient()

# Define your portfolio
portfolio = ["bitcoin", "ethereum", "solana", "cardano", "chainlink"]

# Batch scan
result = client.scan_portfolio(portfolio, sensitivity=1.0)
print(f"Portfolio scan: {len(portfolio)} tokens")

for token_result in result.get("results", []):
    coin = token_result.get("coin_id", "?")
    risk = token_result.get("risk_level", "N/A")
    print(f"  {coin}: {risk}")
