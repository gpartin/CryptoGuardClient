"""Check rug pull risk for a DEX trading pair."""

from cryptoguard import CryptoGuardClient

client = CryptoGuardClient()

# Check a Solana DEX pair (replace with real pair address)
chain = "solana"
pair_address = "YOUR_PAIR_ADDRESS_HERE"

rug = client.rug_check(chain, pair_address)
print(f"Token: {rug.get('token_symbol', '?')}")
print(f"Risk Level: {rug.get('risk_level', 'N/A')}")
print(f"Risk Score: {rug.get('risk_score', 'N/A')}")
print(f"Recommendation: {rug.get('recommendation', 'N/A')}")

flags = rug.get("flags", [])
if flags:
    print(f"\nRisk Flags ({len(flags)}):")
    for f in flags:
        print(f"  - {f}")
