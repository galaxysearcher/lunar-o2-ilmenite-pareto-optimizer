# Methodology

## Objective

Evaluate lunar oxygen extraction process candidates using Pareto and robustness analysis.

The model compares candidate policies for hydrogen reduction of ilmenite-bearing regolith. Each candidate is scored on yield, power, hydrogen loss, process complexity, thermal margin, and stress-case robustness.

## Candidate variables

The candidate grid varies:

- feed rate
- reactor temperature
- reduction time
- grind size
- hydrogen recycle
- heat recovery
- condenser mode

## Objectives

The Pareto frontier uses four objectives:

- maximize oxygen yield
- minimize power draw
- minimize hydrogen loss
- maximize robustness score

## Robustness

Robustness is evaluated across five cases:

- nominal
- low ilmenite content
- cold thermal bias
- hydrogen leakage
- dust loading

The robustness score combines yield retention, thermal margin, power stability, and hydrogen-loss stability.

## Ranking

The scalar rank score is used only to sort the Pareto frontier for review. Frontier membership remains based on dominance over the configured objectives.
