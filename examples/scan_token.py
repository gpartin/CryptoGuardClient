"""Scan a token for anomalous market behavior."""

from cryptoguard import CryptoGuardClient

client = CryptoGuardClient()

# Scan Solana
scan = client.scan("solana")
print(f"Token: solana")
print(f"Risk Level: {scan.get('risk_level', 'N/A')}")
print(f"Recommendation: {scan.get('recommendation', 'N/A')}")

anomalies = scan.get("anomalies", [])
if anomalies:
    print(f"\nAnomalies detected ({len(anomalies)}):")
    for a in anomalies:
        print(f"  - {a.get('description', a.get('label', '?'))}")
else:
    print("\nNo anomalies detected.")
