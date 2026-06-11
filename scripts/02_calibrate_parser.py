"""Parser calibration: reproduce the published S and k/n for D1 and D2 from
our canonical loaders, and run the standard marginal no-signaling check.

Published targets (registered in PREREGISTRATION.md §7 before this ran):
  D1: S = 2.42 +/- 0.20, k/n = 196/245, p = 0.039
  D2: S = 2.35 +/- 0.18 (combined psi-/psi+ as in the experimenters' script)
A parser that cannot reproduce S is not trusted for L_exp.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
from src.loaders import load_delft1, load_delft2
from src.chsh import marginal_ns

TAU = 5.4e-6 * 2
KSI = 3. / 4 + 3 * (TAU + TAU ** 2)


def binom_sf(k, n, p):
    """P(X >= k) for X ~ Bin(n, p), exact, no scipy dependency."""
    from math import comb
    return sum(comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k, n + 1))


def chsh_with_psi(a, b, A, B, psi_plus):
    """CHSH per the experimenters' convention: for psi+ heralds the role of
    Bob's random bit is flipped (S uses E00+E01-E10+E11); equivalently the
    winning condition is (-1)^(a*(b+psi)) = x*y."""
    results = {}
    for psi, mask in (("psi_min", ~psi_plus), ("psi_plus", psi_plus)):
        if not mask.any():
            results[psi] = None
            continue
        E = np.zeros(4)
        Eerr = np.zeros(4)
        ncell = np.zeros(4, dtype=int)
        for ii, (ai, bi) in enumerate([(0, 0), (0, 1), (1, 0), (1, 1)]):
            m = mask & (a == ai) & (b == bi)
            ncell[ii] = m.sum()
            E[ii] = np.mean(A[m] * B[m]) if m.any() else np.nan
            Eerr[ii] = np.sqrt((1 - E[ii] ** 2) / max(ncell[ii], 1))
        signs = (1, 1, -1, 1) if psi == "psi_plus" else (1, 1, 1, -1)
        S = float(np.dot(signs, E))
        Serr = float(np.sqrt((np.array(Eerr) ** 2).sum()))
        results[psi] = dict(S=S, Serr=Serr, n=int(ncell.sum()), E=E)
    return results


def report(d):
    s = d["strict"]
    a, b, A, B = d["a"][s], d["b"][s], d["A"][s], d["B"][s]
    psi_plus = d["psi_plus"][s]
    n = int(s.sum())
    # winning-trial count k exactly as in the experimenters' scripts
    psi_term = psi_plus.astype(int)
    c = ((-1.) ** (a * (b + psi_term)) * (A * B) + 1) / 2
    k = int(c.sum())
    p = binom_sf(k, n, KSI)
    print(f"=== {d['name']}: strict trials n={n}, k={k}, p={p:.3f}")
    res = chsh_with_psi(a, b, A, B, psi_plus)
    Ss = []
    for psi, r in res.items():
        if r is None:
            continue
        print(f"  {psi:9s} n={r['n']:4d}  S = {r['S']:+.3f} +/- {r['Serr']:.3f}  "
              f"E = {np.array2string(r['E'], precision=3)}")
        Ss.append(r)
    if len(Ss) == 2:
        ntot = sum(r["n"] for r in Ss)
        Sc = sum(r["S"] * r["n"] / ntot for r in Ss)
        Sce = np.sqrt(sum((r["n"] / ntot) ** 2 * r["Serr"] ** 2 for r in Ss))
        print(f"  combined  n={ntot:4d}  S = {Sc:+.3f} +/- {Sce:.3f}")
    # standard marginal no-signaling on the strict trials, both directions
    print("  marginal NS (strict): A vs b:",
          {k_: (f"{v[0]:+.4f}", f"z={v[1]:+.2f}") for k_, v in marginal_ns(a, b, A).items()})
    print("                        B vs a:",
          {k_: (f"{v[0]:+.4f}", f"z={v[1]:+.2f}") for k_, v in marginal_ns(b, a, B).items()})
    # and on the all-heralded set (the witness-search PRIMARY event set)
    aa, bb, AA, BB = d["a"], d["b"], d["A"], d["B"]
    print("  marginal NS (all-heralded): A vs b:",
          {k_: (f"{v[0]:+.4f}", f"z={v[1]:+.2f}") for k_, v in marginal_ns(aa, bb, AA).items()})
    print("                              B vs a:",
          {k_: (f"{v[0]:+.4f}", f"z={v[1]:+.2f}") for k_, v in marginal_ns(bb, aa, BB).items()})
    print()


def report_eth():
    """E2/E3 gates for ETH 2023 (registered in PREREGISTRATION Amendment 1):
    reproduce S = 2.0747 +/- 0.0033 at n > 1e6; marginal-NS battery."""
    from src.loaders import load_eth2023
    from src.chsh import correlators
    d = load_eth2023()
    a, b, A, B = d["a"], d["b"], d["A"], d["B"]
    n = len(A)
    E = correlators(a, b, A, B)
    counts = np.array([[(np.sum((a == ai) & (b == bi))) for bi in (0, 1)]
                       for ai in (0, 1)])
    errs = np.sqrt((1 - E ** 2) / counts)
    best, best_signs = 0.0, None
    from src.chsh import SIGNS
    for s in SIGNS:
        v = float(np.dot(s, E.ravel()))
        if abs(v) > abs(best):
            best, best_signs = v, s
    Serr = float(np.sqrt((errs.ravel() ** 2).sum()))
    z_violation = (abs(best) - 2) / Serr
    print(f"=== eth2023: n={n} trials")
    print(f"  E = {np.array2string(E.ravel(), precision=4)}  signs={best_signs}")
    print(f"  S = {abs(best):.4f} +/- {Serr:.4f}   (published 2.0747 +/- 0.0033)")
    print(f"  violation z = {z_violation:.1f} sigma above S=2")
    print("  marginal NS: A vs b:",
          {k_: (f"{v[0]:+.5f}", f"z={v[1]:+.2f}") for k_, v in marginal_ns(a, b, A).items()})
    print("               B vs a:",
          {k_: (f"{v[0]:+.5f}", f"z={v[1]:+.2f}") for k_, v in marginal_ns(b, a, B).items()})


def main():
    report(load_delft1())
    report(load_delft2())
    report_eth()


if __name__ == "__main__":
    main()
