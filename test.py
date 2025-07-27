import requests
import json

API_KEY = "cqt_rQw7vfx9qdq6YcvcHgWYghrjQrWY"
wallet = "0x0039f22efb07a647557c7c5d17854cfd6d489ef3"
url = f"https://api.covalenthq.com/v1/1/address/{wallet}/balances_v2/"

params = {
    "key": "cqt_rQw7vfx9qdq6YcvcHgWYghrjQrWY"
}

r = requests.get(url, params=params)
print("Status Code:", r.status_code)

try:
    data = r.json()
    for item in data['data']['items']:
        token_symbol = item.get('contract_ticker_symbol')
        decimals = item.get('contract_decimals')
        balance_raw = item.get('balance')

        if decimals is None or balance_raw is None:
            continue  # Skip problematic token

        balance = int(balance_raw) / (10 ** decimals)
        print(f"{token_symbol}: {balance}")

except Exception as e:
    print("Error parsing JSON:", e)
    print("Raw text:", r.text)
