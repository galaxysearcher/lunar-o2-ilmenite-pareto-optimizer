"""
Robustness scoring across stress cases.
"""
from __future__ import annotations

from typing import Dict, Iterable, List

from .model import score_candidate


DEFAULT_STRESS_CASES = [
    {"name": "nominal", "feed_purity_factor": 1.00, "thermal_loss_factor": 1.00, "h2_leak_factor": 1.00, "dust_penalty": 0.0},
    {"name": "low_ilmenite", "feed_purity_factor": 0.82, "thermal_loss_factor": 1.00, "h2_leak_factor": 1.00, "dust_penalty": 0.1},
    {"name": "cold_bias", "feed_purity_factor": 1.00, "thermal_loss_factor": 1.18, "h2_leak_factor": 1.00, "dust_penalty": 0.0},
    {"name": "h2_leakage", "feed_purity_factor": 1.00, "thermal_loss_factor": 1.00, "h2_leak_factor": 1.35, "dust_penalty": 0.0},
    {"name": "dust_loading", "feed_purity_factor": 0.92, "thermal_loss_factor": 1.08, "h2_leak_factor": 1.10, "dust_penalty": 0.35},
]


def evaluate_robustness(candidate: Dict, stress_cases: List[Dict] | None = None) -> Dict:
    """Evaluate a candidate across stress cases and compute a robustness score."""
    stress_cases = stress_cases or DEFAULT_STRESS_CASES
    scored = [score_candidate(candidate, case) for case in stress_cases]

    nominal = scored[0]
    nominal_o2 = max(1e-9, nominal["oxygen_kg_hr"])
    worst_o2 = min(row["oxygen_kg_hr"] for row in scored)
    worst_margin = min(row["thermal_margin_c"] for row in scored)
    max_power = max(row["power_kw"] for row in scored)
    max_h2_loss = max(row["h2_loss_kg_hr"] for row in scored)

    yield_retention = worst_o2 / nominal_o2
    thermal_score = max(0.0, min(1.0, worst_margin / 220.0))
    power_score = max(0.0, min(1.0, 1.0 - (max_power - nominal["power_kw"]) / max(1.0, nominal["power_kw"])))
    h2_score = max(0.0, min(1.0, 1.0 - (max_h2_loss - nominal["h2_loss_kg_hr"]) / max(0.05, max_h2_loss)))

    robustness = 0.40 * yield_retention + 0.25 * thermal_score + 0.20 * power_score + 0.15 * h2_score

    return {
        "robustness_score": robustness,
        "yield_retention": yield_retention,
        "worst_oxygen_kg_hr": worst_o2,
        "worst_thermal_margin_c": worst_margin,
        "max_power_kw": max_power,
        "max_h2_loss_kg_hr": max_h2_loss,
    }
