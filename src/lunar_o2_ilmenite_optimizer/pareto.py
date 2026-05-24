"""
Pareto-frontier utilities.
"""
from __future__ import annotations

from typing import Dict, List


def dominates(a: Dict, b: Dict) -> bool:
    """Return True when a dominates b over the configured objectives."""
    better_or_equal = (
        a["oxygen_kg_hr"] >= b["oxygen_kg_hr"]
        and a["power_kw"] <= b["power_kw"]
        and a["h2_loss_kg_hr"] <= b["h2_loss_kg_hr"]
        and a["robustness_score"] >= b["robustness_score"]
    )
    strictly_better = (
        a["oxygen_kg_hr"] > b["oxygen_kg_hr"]
        or a["power_kw"] < b["power_kw"]
        or a["h2_loss_kg_hr"] < b["h2_loss_kg_hr"]
        or a["robustness_score"] > b["robustness_score"]
    )
    return better_or_equal and strictly_better


def pareto_frontier(rows: List[Dict]) -> List[Dict]:
    """Return non-dominated rows."""
    frontier = []
    for i, row in enumerate(rows):
        if not any(dominates(other, row) for j, other in enumerate(rows) if i != j):
            frontier.append(row)
    frontier.sort(key=lambda r: (-r["robustness_score"], -r["oxygen_kg_hr"], r["power_kw"]))
    return frontier


def scalar_rank_score(row: Dict) -> float:
    """Convenience score for sorting a frontier table."""
    return (
        2.2 * row["oxygen_kg_hr"]
        + 1.4 * row["robustness_score"]
        - 0.18 * row["power_kw"]
        - 1.0 * row["h2_loss_kg_hr"]
        - 0.08 * row["complexity_score"]
    )
