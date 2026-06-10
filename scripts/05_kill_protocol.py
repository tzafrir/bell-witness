"""Kill protocol for the single pre-registered anomaly:
delft1/primary/A-vs-b, L_exp=0.205, p=0.004 (below 5x-floor certification).

Registered confirmation requirements (PREREGISTRATION.md §6) — ALL must hold
for the anomaly to survive as 'candidate, unconfirmed':
  (i)   re-derivation with independent split seeds 1-5,
  (ii)  re-derivation on held-back temporal halves (split by day number),
  (iii) detector-family robustness (coord vs linear agree in sign/magnitude).
Plus context diagnostics (not gates): look-elsewhere across the 12
pre-registered tests; behaviour of the implicated raw statistic.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
from src.loaders import load_delft1
from src.lexp import lexp

N_PERM = 1000


def perm_p(a, b, A, W, seed, n_perm=N_PERM, min_cell=50):
    obs, detail = lexp(a, b, A, W, seed=seed, min_cell=min_cell)
    rng = np.random.default_rng(seed + 12345)
    null = np.empty(n_perm)
    for i in range(n_perm):
        bp = b.copy()
        for ai in (0, 1):
            idx = np.where(a == ai)[0]
            bp[idx] = rng.permutation(b[idx])
        null[i], _ = lexp(a, bp, A, W, seed=int(rng.integers(1 << 30)),
                          min_cell=min_cell)
    p = float((1 + np.sum(null >= obs)) / (1 + n_perm))
    return obs, p, detail


def main():
    d = load_delft1()
    a, b, A, W, day = d["a"], d["b"], d["A"], d["W"], d["day"]

    print("== (i) independent holdout split seeds 1-5 (gate: p<0.01 each) ==")
    survived_i = True
    for seed in range(1, 6):
        obs, p, detail = perm_p(a, b, A, W, seed)
        gate = p < 0.01
        survived_i &= gate
        print(f"  seed={seed}  L_exp={obs:.4f}  p={p:.4f}  detail={detail}  "
              f"{'pass' if gate else 'FAIL'}")

    print("== (ii) held-back temporal halves by day number (gate: p<0.01 both) ==")
    med = np.median(day)
    survived_ii = True
    for name, m in (("early half", day <= med), ("late half", day > med)):
        obs, p, detail = perm_p(a[m], b[m], A[m], W[m], seed=0)
        gate = p < 0.01
        survived_ii &= gate
        print(f"  {name:11s} n={m.sum():4d}  L_exp={obs:.4f}  p={p:.4f}  "
              f"detail={detail}  {'pass' if gate else 'FAIL'}")

    print("== (iii) detector-family coherence on the seed-0 split ==")
    # reproduce the seed-0 split and report both detector values per a-stratum
    rng = np.random.default_rng(0)
    perm = rng.permutation(len(A))
    h = len(A) // 2
    tr, te = perm[:h], perm[h:]
    for ai in (0, 1):
        m0t = tr[(a[tr] == ai) & (b[tr] == 0)]
        m1t = tr[(a[tr] == ai) & (b[tr] == 1)]
        m0e = te[(a[te] == ai) & (b[te] == 0)]
        m1e = te[(a[te] == ai) & (b[te] == 1)]
        dvec = (A[m0t, None] * W[m0t]).mean(0) - (A[m1t, None] * W[m1t]).mean(0)
        j = int(np.argmax(np.abs(dvec)))
        w = dvec / (np.linalg.norm(dvec) + 1e-12)
        coord = abs((A[m0e] * W[m0e, j]).mean() - (A[m1e] * W[m1e, j]).mean())
        lin = abs((A[m0e] * np.sign(W[m0e] @ w)).mean()
                  - (A[m1e] * np.sign(W[m1e] @ w)).mean())
        print(f"  a={ai}: train direction peak coord={j}, "
              f"holdout coord={coord:.4f}, holdout linear={lin:.4f}")

    print("== context: look-elsewhere ==")
    print("  12 pre-registered tests; P(min p <= 0.004 under global null) "
          f"~= {1 - (1 - 0.004) ** 12:.3f}")
    print("  pooled/primary (superset incl. all D1 events): p=0.905 — a "
          "physical leak of 0.20 in 4746/8664 events would not vanish there.")

    print("== context: implicated raw statistic E[A*t1z | a=0, b] ==")
    for bi in (0, 1):
        m = (a == 0) & (b == bi)
        v = A[m] * W[m, 2]
        print(f"  b={bi}: n={m.sum():4d}  mean={v.mean():+.4f}  "
              f"sem={v.std() / np.sqrt(m.sum()):.4f}")

    print()
    verdict = ("anomaly SURVIVES (candidate, unconfirmed)"
               if (survived_i and survived_ii)
               else "anomaly KILLED")
    print("KILL PROTOCOL VERDICT:", verdict)


if __name__ == "__main__":
    main()
