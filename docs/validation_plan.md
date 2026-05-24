# Validation Plan

## Current validation

The repository validates:

- candidate generation
- deterministic scoring
- stress-case robustness
- Pareto-frontier selection
- result serialization
- script execution

## Next validation gates

1. Add unit provenance for each model coefficient.
2. Add sensitivity sweeps around ilmenite fraction and thermal-loss assumptions.
3. Compare Pareto-frontier stability across stress-case weights.
4. Add plotting for oxygen yield versus power and robustness.
5. Add a notebook-free report generator for frontier tables.
6. Add calibration hooks for experimental or literature-derived process data.

## Acceptance logic

A useful trade-study model should keep candidate assumptions explicit, expose the non-dominated options, and make performance sensitivity visible under stress cases.
