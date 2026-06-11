"""The L_exp hunt: pre-registered witness search on the Delft datasets.

Runs, for each dataset x event-set x direction (registered in
PREREGISTRATION.md before execution):
  - observed L_exp (holdout optimal detector, seed 0)
  - permutation null (n_perm=1000, b shuffled within a strata)
  - sensitivity floor and the 5x-floor certification threshold
Decision rule: candidate iff p < 0.01 AND obs > 5*floor. Otherwise null;
exclusion level = max(obs, null 95th percentile).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
from src.loaders import load_delft1, load_delft2, load_pooled
from src.lexp import lexp, sensitivity_bound

N_PERM = 1000


def run_one(tag, a, b, A, W, min_cell, n_perm=N_PERM):
    n = len(A)
    floor = sensitivity_bound(n)
    obs, detail = lexp(a, b, A, W, seed=0, min_cell=min_cell)
    # lexp_null re-calls lexp with default min_cell; inline the loop so the
    # registered min_cell applies to null draws too
    rng = np.random.default_rng(0)
    null = np.empty(n_perm)
    for i in range(n_perm):
        bp = b.copy()
        for ai in (0, 1):
            idx = np.where(a == ai)[0]
            bp[idx] = rng.permutation(b[idx])
        null[i], _ = lexp(a, bp, A, W, seed=int(rng.integers(1 << 30)),
                          min_cell=min_cell)
    p = float((1 + np.sum(null >= obs)) / (1 + n_perm))
    q95 = float(np.quantile(null, 0.95))
    candidate = (p < 0.01) and (obs > 5 * floor)
    verdict = "CANDIDATE (kill protocol required)" if candidate else (
        "anomaly below certification threshold (kill protocol required)"
        if p < 0.01 else "null")
    rec = dict(tag=tag, n=n, obs=float(obs), detail=detail, p=p,
               null_mean=float(null.mean()), null_q95=q95,
               floor=float(floor), five_floor=float(5 * floor),
               exclusion=float(max(obs, q95)), verdict=verdict)
    print(f"{tag:34s} n={n:5d}  L_exp={obs:.4f}  p={p:.4f}  "
          f"null95={q95:.4f}  5xfloor={5*floor:.4f}  -> {verdict}")
    return rec


def main():
    out = []
    for load in (load_delft1, load_delft2, load_pooled):
        d = load()
        name = d["name"]
        s = d["strict"]
        sets = [("primary", np.ones(len(d["A"]), bool), 50),
                ("strict", s, 15)]
        for set_name, m, min_cell in sets:
            a, b, A, B = d["a"][m], d["b"][m], d["A"][m], d["B"][m]
            W = d["W"][m]
            out.append(run_one(f"{name}/{set_name}/A-vs-b", a, b, A, W, min_cell))
            out.append(run_one(f"{name}/{set_name}/B-vs-a (mirror)", b, a, B, W, min_cell))
    res_path = Path(__file__).resolve().parents[1] / "results" / "witness_search.json"
    res_path.write_text(json.dumps(out, indent=2))
    print(f"\nwritten: {res_path}")


if __name__ == "__main__":
    main()
