# Compound Wallet Risk Scoring

This project fetches Compound V2/V3 wallet activity and assigns a risk score (0–1000) to each wallet based on behavioral patterns and protocol engagement.

## Structure

- `src/`: Python scripts for data fetching and scoring
- `data/`: Input wallet list
- `output/`: Wallet event logs and final scores

## Run

```bash
python src/fetch_graph_data.py
python src/score_wallets.py
