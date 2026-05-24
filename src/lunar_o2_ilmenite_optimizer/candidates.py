"""
Candidate generation for ilmenite oxygen extraction trade studies.
"""
from __future__ import annotations

from itertools import product
from typing import Dict, Iterable, List


def generate_candidates() -> List[Dict]:
    """Generate a compact grid of process candidates."""
    feed_rate_kg_hr = [5.0, 10.0, 15.0]
    reactor_temp_c = [850.0, 950.0, 1050.0]
    reduction_time_min = [30.0, 45.0, 60.0]
    grind_micron = [50.0, 100.0, 200.0]
    h2_recycle = [False, True]
    heat_recovery = [False, True]
    condenser_mode = ["low", "nominal", "high"]

    candidates = []
    for idx, combo in enumerate(product(
        feed_rate_kg_hr,
        reactor_temp_c,
        reduction_time_min,
        grind_micron,
        h2_recycle,
        heat_recovery,
        condenser_mode,
    )):
        feed, temp, time, grind, recycle, heat, condenser = combo
        candidates.append({
            "id": f"candidate_{idx:04d}",
            "feed_rate_kg_hr": feed,
            "reactor_temp_c": temp,
            "reduction_time_min": time,
            "grind_micron": grind,
            "h2_recycle": recycle,
            "heat_recovery": heat,
            "condenser_mode": condenser,
        })
    return candidates
