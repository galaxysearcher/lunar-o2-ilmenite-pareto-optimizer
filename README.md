# Lunar O2 Ilmenite Pareto Optimizer

Pareto and robustness analysis for lunar oxygen extraction tradeoffs using ilmenite processing scenarios.

The workflow evaluates discrete process configurations for hydrogen reduction of ilmenite-bearing regolith. Each candidate is scored for oxygen yield, power draw, hydrogen loss, process complexity, thermal margin, and robustness across stress cases.

```text
process candidates -> performance model -> robustness sweep -> Pareto frontier -> ranked trade table
```

## What this project does

- Generates a structured candidate set for ilmenite oxygen extraction.
- Estimates oxygen yield, power draw, hydrogen loss, and thermal margin.
- Evaluates robustness across nominal and stressed operating cases.
- Builds a Pareto frontier using yield, power, hydrogen loss, and robustness objectives.
- Writes CSV and JSON outputs for review and comparison.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
python scripts/run_trade_study.py
```

The run writes:

```text
results/candidates.csv
results/pareto_frontier.json
results/summary.json
```

## Run tests

```bash
python -m pytest
```

## Repository structure

```text
src/lunar_o2_ilmenite_optimizer/
  candidates.py
  model.py
  pareto.py
  robustness.py

scripts/
  run_trade_study.py

docs/
  methodology.md
  validation_plan.md

examples/
  stress_cases.json
```

## Output fields

Each candidate includes:

- process configuration
- oxygen yield estimate
- power estimate
- hydrogen loss estimate
- complexity score
- thermal margin
- robustness score
- Pareto-frontier status

## Research workflow

This repository turns a lunar oxygen extraction concept into an explicit trade-study workflow. The core pattern is: define candidate process policies, score each policy against mission-relevant objectives, evaluate stress-case robustness, and surface the non-dominated options.
