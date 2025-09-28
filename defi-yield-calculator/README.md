# DeFi Yield Calculator (Python)

A simple CLI tool to compute APR and APY and simulate compounding for DeFi positions.

## Features
- Convert APR ↔ APY with a chosen compounding frequency
- Simulate earnings over a period (days/months/years)
- Compare multiple pools (CSV input)

## Quick Start
```bash
python yield_calc.py --apr 12 --principal 10000 --days 30 --compound daily
python yield_calc.py --apy 15 --principal 5000 --months 6
python yield_calc.py --compare pools.csv --principal 10000 --days 90
```

`pools.csv` example:
```csv
name,apr
Pool A,12
Pool B,18
Pool C,8
```

## Notes
- APR = simple interest rate.
- APY = effective annual yield after compounding.
