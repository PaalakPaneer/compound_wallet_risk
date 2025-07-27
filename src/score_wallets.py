import os
import json
import pandas as pd
from datetime import datetime

EVENT_PATH = "output/compound_events"

def load_events(wallet):
    try:
        with open(f"{EVENT_PATH}/{wallet}.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Failed to load events for {wallet}: {e}")
        return []

def parse_timestamp(ts):
    try:
        return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
    except:
        return None

def compute_features(events):
    borrow_total = 0
    repay_total = 0
    supply_total = 0
    withdraw_total = 0
    absorb_count = 0
    unique_events = set()
    timestamps = []

    for e in events:
        evt = e.get("event_name")
        params = e.get("params", {})
        amt = float(params.get("amount", 0)) or 0
        value_usd = float(e.get("value_usd", 0)) or 0
        ts = parse_timestamp(e.get("timestamp"))

        if evt == "Borrow":
            borrow_total += value_usd
        elif evt == "RepayBorrow":
            repay_total += value_usd
        elif evt in {"Mint", "Supply"}:
            supply_total += value_usd
        elif evt in {"Redeem", "Withdraw"}:
            withdraw_total += value_usd
        elif evt == "Absorb":
            absorb_count += 1

        if evt:
            unique_events.add(evt)
        if ts:
            timestamps.append(ts)

    net_deposit = supply_total - withdraw_total
    activity_days = (max(timestamps) - min(timestamps)).days + 1 if len(timestamps) >= 2 else 1
    tx_freq = len(events) / activity_days if activity_days > 0 else 0.0
    repay_ratio = repay_total / borrow_total if borrow_total > 0 else 1.0  # Perfect if no borrow
    event_diversity = len(unique_events)

    return {
        "borrow_usd": borrow_total,
        "repay_usd": repay_total,
        "repay_to_borrow": repay_ratio,
        "net_deposit_usd": net_deposit,
        "absorb_count": absorb_count,
        "tx_per_day": tx_freq,
        "event_diversity": event_diversity
    }

def normalize(val, min_val, max_val):
    if max_val == min_val:
        return 0.5
    return (val - min_val) / (max_val - min_val)

def score_wallet(features, all_features_df):
    s = 0
    norm = lambda col: normalize(features[col], all_features_df[col].min(), all_features_df[col].max())

    # Weighted sum model
    s += norm("repay_to_borrow") * 250
    s += norm("net_deposit_usd") * 200
    s += norm("tx_per_day") * 150
    s += norm("event_diversity") * 100
    s += (1 - norm("absorb_count")) * 200  # penalize liquidations
    s += norm("repay_usd") * 100
    s *= 2

    return int(round(min(max(s, 0), 1000)))

def main():
    wallets = [f.replace(".json", "") for f in os.listdir(EVENT_PATH) if f.endswith(".json")]
    rows = []
    features_dict = {}

    for wallet in wallets:
        events = load_events(wallet)
        features = compute_features(events)
        features_dict[wallet] = features

    all_features_df = pd.DataFrame.from_dict(features_dict, orient="index")

    for wallet, feats in features_dict.items():
        score = score_wallet(feats, all_features_df)
        rows.append({"wallet_id": wallet, "score": score})

    os.makedirs("output", exist_ok=True)
    pd.DataFrame(rows).to_csv("output/wallet_scores.csv", index=False)
    print("Risk scoring complete! Output saved to `output/wallet_scores.csv`")

if __name__ == "__main__":
    main()
