"""
Performance model for ilmenite oxygen extraction candidates.

The model is intentionally compact and deterministic so tradeoffs can be inspected.
"""
from __future__ import annotations

from typing import Dict


CONDENSER_EFF = {
    "low": 0.82,
    "nominal": 0.90,
    "high": 0.95,
}


def _conversion(temp_c: float, minutes: float, grind_micron: float) -> float:
    temp_term = max(0.0, min(1.0, (temp_c - 780.0) / 330.0))
    time_term = max(0.0, min(1.0, minutes / 70.0))
    grind_term = max(0.55, min(1.05, 160.0 / grind_micron))
    conversion = 0.25 + 0.62 * temp_term * time_term * grind_term
    return max(0.05, min(0.92, conversion))


def score_candidate(candidate: Dict, stress: Dict | None = None) -> Dict:
    """
    Score one process candidate.

    Stress cases modify feed purity, thermal loss, hydrogen leakage, and dust handling.
    """
    stress = stress or {}
    feed_factor = float(stress.get("feed_purity_factor", 1.0))
    thermal_loss = float(stress.get("thermal_loss_factor", 1.0))
    h2_leak = float(stress.get("h2_leak_factor", 1.0))
    dust_penalty = float(stress.get("dust_penalty", 0.0))

    feed = float(candidate["feed_rate_kg_hr"])
    temp = float(candidate["reactor_temp_c"])
    minutes = float(candidate["reduction_time_min"])
    grind = float(candidate["grind_micron"])

    ilmenite_fraction = 0.12 * feed_factor
    recoverable_o2_fraction = 0.316
    conversion = _conversion(temp, minutes, grind)
    condenser_eff = CONDENSER_EFF[candidate["condenser_mode"]]

    oxygen_kg_hr = feed * ilmenite_fraction * recoverable_o2_fraction * conversion * condenser_eff

    heat_power = 0.0028 * feed * (temp - 20.0) * thermal_loss
    grind_power = 0.25 * feed * (100.0 / grind)
    residence_power = 0.018 * minutes
    condenser_power = {"low": 0.15, "nominal": 0.28, "high": 0.45}[candidate["condenser_mode"]]
    recycle_credit = 0.30 if candidate["h2_recycle"] else 0.0
    heat_credit = 0.42 if candidate["heat_recovery"] else 0.0
    power_kw = max(0.2, heat_power + grind_power + residence_power + condenser_power - recycle_credit - heat_credit)

    h2_loss_kg_hr = feed * ilmenite_fraction * (0.020 if candidate["h2_recycle"] else 0.075) * h2_leak
    complexity = (
        1.0
        + (0.7 if candidate["h2_recycle"] else 0.0)
        + (0.5 if candidate["heat_recovery"] else 0.0)
        + {"low": 0.0, "nominal": 0.2, "high": 0.45}[candidate["condenser_mode"]]
        + dust_penalty
    )
    thermal_margin_c = 1120.0 - temp - 30.0 * thermal_loss

    return {
        **candidate,
        "oxygen_kg_hr": oxygen_kg_hr,
        "power_kw": power_kw,
        "h2_loss_kg_hr": h2_loss_kg_hr,
        "complexity_score": complexity,
        "thermal_margin_c": thermal_margin_c,
        "conversion": conversion,
    }
