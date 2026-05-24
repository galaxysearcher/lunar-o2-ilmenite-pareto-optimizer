from __future__ import annotations

import csv
import json
from pathlib import Path

from lunar_o2_ilmenite_optimizer import generate_candidates, score_candidate, pareto_frontier, evaluate_robustness
from lunar_o2_ilmenite_optimizer.pareto import scalar_rank_score


def main() -> int:
    rows = []
    for candidate in generate_candidates():
        base = score_candidate(candidate)
        robust = evaluate_robustness(candidate)
        row = {**base, **robust}
        row["rank_score"] = scalar_rank_score(row)
        rows.append(row)

    frontier = pareto_frontier(rows)
    for row in rows:
        row["pareto"] = row["id"] in {f["id"] for f in frontier}

    frontier_ranked = sorted(frontier, key=scalar_rank_score, reverse=True)

    Path("results").mkdir(exist_ok=True)
    fieldnames = list(rows[0].keys())
    with Path("results/candidates.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    Path("results/pareto_frontier.json").write_text(json.dumps(frontier_ranked[:25], indent=2), encoding="utf-8")
    summary = {
        "n_candidates": len(rows),
        "n_pareto": len(frontier),
        "best_ranked_candidate": frontier_ranked[0],
        "top_5_ids": [row["id"] for row in frontier_ranked[:5]],
    }
    Path("results/summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
