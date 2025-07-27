```markdown
## Data Collection

All wallet activities were pulled from Compound V2/V3 via The Graph or Covalent APIs and saved to JSON files. Each file holds decoded event logs like `Borrow`, `RepayBorrow`, `Mint`, and more.

---

## Feature Selection

| Feature | Description |
|--------|-------------|
| borrow_usd | Total borrowed in USD |
| repay_usd | Total repaid in USD |
| repay_to_borrow | Repay/Borrow ratio |
| net_deposit_usd | Supply - Withdraw in USD |
| absorb_count | Liquidations faced |
| tx_per_day | Activity frequency |
| event_diversity | Protocol usage breadth |

---

## Scoring Logic

A deterministic score is calculated using:

```python
score = (
    norm(repay_to_borrow) * 250 +
    norm(net_deposit_usd) * 200 +
    norm(tx_per_day) * 150 +
    norm(event_diversity) * 100 +
    (1 - norm(absorb_count)) * 200 +
    norm(repay_usd) * 100
) * 2