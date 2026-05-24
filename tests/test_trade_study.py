import json
import subprocess
import sys
from pathlib import Path

from lunar_o2_ilmenite_optimizer import generate_candidates, score_candidate, evaluate_robustness, pareto_frontier


def test_candidate_generation():
    candidates = generate_candidates()
    assert len(candidates) > 100
    assert {"feed_rate_kg_hr", "reactor_temp_c", "h2_recycle"} <= set(candidates[0].keys())


def test_scoring_and_robustness():
    candidate = generate_candidates()[0]
    scored = score_candidate(candidate)
    robust = evaluate_robustness(candidate)
    assert scored["oxygen_kg_hr"] > 0
    assert scored["power_kw"] > 0
    assert 0 <= robust["robustness_score"] <= 1.5


def test_pareto_frontier_nonempty():
    rows = []
    for candidate in generate_candidates()[:50]:
        rows.append({**score_candidate(candidate), **evaluate_robustness(candidate)})
    frontier = pareto_frontier(rows)
    assert len(frontier) >= 1


def test_run_trade_study_script():
    result = subprocess.run(
        [sys.executable, "scripts/run_trade_study.py"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    assert "n_candidates" in result.stdout
    assert Path("results/summary.json").exists()
    payload = json.loads(Path("results/summary.json").read_text(encoding="utf-8"))
    assert payload["n_candidates"] > payload["n_pareto"] >= 1
