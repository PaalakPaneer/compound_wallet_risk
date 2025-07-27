import os
import requests
import json
import time

COVALENT_API_KEY = "cqt_rQw7vfx9qdq6YcvcHgWYghrjQrWY"
CHAIN_ID = "1"  # Ethereum mainnet
INPUT_FILE = "data/input_wallets.csv"

COMPOUND_V2_CONTRACTS = {
    "0x3d9819210a31b4961b30ef54be2aed79b9c9cd3b",  # Comptroller
    "0x5d3a536e4d6dbd6114cc1ead35777bab948e3643",  # cDAI
    "0x39aa39c021dfbae8fac545936693ac917d5e7563",  # cUSDC
    "0x4ddc2d193948926d02f9b1fe9e1daa0718270ed5",  # cETH
    "0x35a18000230da775cac24873d00ff85bccded550",  # cUNI
    "0x7713dd9ca933848f6819f38b8352d9a15ea73f67a",  # cFEI
}

COMPOUND_V3_CONTRACTS = {
    "0xc3d688b66703497daa19211eedff47f25384cdc3",  # USDCv3 Comet
    "0xa17581a9e3356d9a858b789d68b4d866e593ae94",  # WETHv3 Comet
}

COMPOUND_METHODS = {
    "Mint", "Borrow", "RepayBorrow", "Redeem",       # V2
    "Supply", "Withdraw", "BuyCollateral", "Absorb"  # V3
}

def fetch_wallet_transactions(wallet):
    url = f"https://api.covalenthq.com/v1/{CHAIN_ID}/address/{wallet}/transactions_v3/"
    params = {"key": COVALENT_API_KEY}
    response = requests.get(url, params=params)

    os.makedirs("output/raw_responses", exist_ok=True)
    with open(f"output/raw_responses/{wallet}.json", "w", encoding="utf-8") as f:
        f.write(response.text)

    try:
        data = response.json()
    except Exception:
        return []

    if "data" not in data or data["data"] is None:
        return []

    return data["data"]["items"]

def extract_compound_events(transactions):
    compound_events = []

    for tx in transactions:
        tx_hash = tx["tx_hash"]
        to_address = (tx.get("to_address") or "").lower()
        logs = tx.get("log_events", [])
        timestamp = tx.get("block_signed_at")
        value_eth = tx.get("value_quote", 0)

        matched = False

        if to_address in COMPOUND_V2_CONTRACTS.union(COMPOUND_V3_CONTRACTS):
            matched = True

        for log in logs:
            decoded = log.get("decoded")
            if decoded and decoded.get("name") in COMPOUND_METHODS:
                event_name = decoded["name"]
                contract = log.get("sender_address")
                params_list = decoded.get("params") or []
                params = {p["name"]: p["value"] for p in params_list} 

                compound_events.append({
                    "tx_hash": tx_hash,
                    "timestamp": timestamp,
                    "event_name": event_name,
                    "contract": contract,
                    "value_usd": value_eth,
                    "params": params,
                })
                matched = True

    return compound_events

def main():
    os.makedirs("output/compound_events", exist_ok=True)

    with open(INPUT_FILE, "r") as f:
        wallets = [line.strip() for line in f if line.strip()]

    for wallet in wallets:
        print(f"Fetching Compound activity for: {wallet}")
        txs = fetch_wallet_transactions(wallet)
        events = extract_compound_events(txs)

        with open(f"output/compound_events/{wallet}.json", "w", encoding="utf-8") as f:
            json.dump(events, f, indent=2)

        print(f"{len(events)} compound events saved for {wallet}\n")
        time.sleep(1.2)

if __name__ == "__main__":
    main()
