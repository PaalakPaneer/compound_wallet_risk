# Compound Wallet Risk Scoring

This project analyzes wallet activity on the Compound V2/V3 lending protocols and assigns a risk score between 0 and 1000 to each wallet based on behavioral patterns, usage, and protocol interaction.

# How to Get a Covalent API Key

Go to: https://www.covalenthq.com/platform/#/auth/register/

Sign up and verify your email.

Copy your API key (starts with ckey_)

Open src/fetch_graph_data.py and replace this line:

```

COVALENT_API_KEY = "your_api_key_here"

```

# How to Run

1. Install dependencies
```

pip install requests pandas numpy

```

2. Add wallet addresses

Edit data/input_wallets.csv and add one wallet address per line:

```

0xabc123...
0xdef456...

```

3. Fetch Compound activity

```

python src/fetch_graph_data.py

```

4. Score wallets
```

python src/score_wallets.py

```

This creates output/scores.csv with the following format:

```

wallet_id,score
0xabc123...,742
0xdef456...,621

```

# Additional Notes

Scoring is based only on Compound V2/V3 events (borrow, repay, supply, liquidation, etc).

Behavior is evaluated using ratio metrics, activity frequency, and protocol engagement.

See analysis.md for a full breakdown of scoring logic and risk factors.