"""Search for tokens and check free tier status."""

from cryptoguard import CryptoGuardClient

client = CryptoGuardClient()

# Search for a token
results = client.search("pepe")
print(f"Search results for 'pepe': {len(results)} found")
for r in results[:5]:
    print(f"  {r.get('name')} ({r.get('symbol')}) -> {r.get('coin_id')}")

# Check free tier remaining
tier = client.free_tier()
print(f"\nFree tier: {tier}")

# Check service health
health = client.health()
print(f"Health: {health}")
