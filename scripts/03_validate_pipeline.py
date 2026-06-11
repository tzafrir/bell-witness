"""Run the synthetic known-answer validation. Must pass before any real data
is touched (see CONTEXT.md §7 step 1). Prints a verdict for LAB_NOTES.md."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.synthetic import make_synthetic
from src.chsh import chsh_S, marginal_ns
from src.lexp import lexp, lexp_null, sensitivity_bound


def main():
    ok = True

    # --- Known answer 1: leak=0 must be quiet -------------------------------
    d = make_synthetic(leak=0.0, seed=2)
    floor = sensitivity_bound(len(d["A"]))
    obs0, null0, p0 = lexp_null(d["a"], d["b"], d["A"], d["W"], n_perm=100)
    quiet = (obs0 < 5 * floor) and (p0 > 0.05)
    ok &= quiet
    print(f"[leak=0.00] L_exp={obs0:.4f}  p={p0:.3f}  5x floor={5*floor:.4f}  "
          f"null mean={null0.mean():.4f}  -> {'PASS (quiet)' if quiet else 'FAIL'}")

    # --- Known answer 2: leak=0.12 must be recovered ------------------------
    d = make_synthetic(leak=0.12, seed=3)
    obs1, det1 = lexp(d["a"], d["b"], d["A"], d["W"])
    _, _, p1 = lexp_null(d["a"], d["b"], d["A"], d["W"], n_perm=100)
    rec = (obs1 > 0.06) and (p1 < 0.05)
    ok &= rec
    print(f"[leak=0.12] L_exp={obs1:.4f}  p={p1:.3f}  detector={det1}  "
          f"-> {'PASS (recovered)' if rec else 'FAIL'}")

    # --- Sanity: marginal NS stays flat even when the joint leaks -----------
    ns = marginal_ns(d["a"], d["b"], d["A"])
    max_z = max(abs(z) for (_, z) in ns.values())
    print(f"[leak=0.12] marginal NS max |z| = {max_z:.2f} "
          f"(joint leak {'IS' if max_z < 3 else 'IS NOT'} invisible to marginals)")

    # --- Sanity: CHSH machinery runs on synthetic ----------------------------
    S = chsh_S(d["a"], d["b"], d["A"], d["B"])
    print(f"[leak=0.12] synthetic CHSH S = {S:.3f} (machinery check only; "
          f"synthetic gadget is not built to violate)")

    print()
    print("PIPELINE VALIDATION:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
