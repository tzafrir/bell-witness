#!/usr/bin/env python3
"""Single-command reproduction of every number in results/RETRO_REPORT.md and
results/RETRO2_REPORT.md.

    python reproduce.py                  # full run, exits nonzero on any mismatch
    python reproduce.py --write-expected # regenerate results/expected/expected.json

Steps:
  1. synthetic known-answer suite (pytest tests/)
  2. acquire public data via scripts/01_acquire.py (checksum-verified;
     datasets whose host is unreachable are skipped with manual instructions
     and their comparisons reported as SKIPPED, not failed)
  3. re-derive: synthetic validation numbers, D1/D2/ETH calibration, the 12
     pre-registered L_exp tests, and the kill-protocol numbers
  4. diff against results/expected/expected.json (seeds are stated there;
     all permutation tests are exactly reproducible with pinned numpy)
"""
import argparse
import importlib.util
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import numpy as np  # noqa: E402

from src.chsh import chsh_S, marginal_ns  # noqa: E402
from src.lexp import lexp, lexp_null, sensitivity_bound  # noqa: E402
from src.synthetic import make_synthetic  # noqa: E402

EXPECTED_PATH = ROOT / "results" / "expected" / "expected.json"
REPRODUCED_PATH = ROOT / "results" / "reproduced.json"
RTOL, ATOL = 1e-9, 1e-12


def load_script(fname):
    spec = importlib.util.spec_from_file_location(
        fname.replace(".py", ""), ROOT / "scripts" / fname)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def step1_synthetic_suite():
    print("== step 1: synthetic known-answer suite (pytest) ==")
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", str(ROOT / "tests")],
                       cwd=ROOT)
    if r.returncode != 0:
        print("synthetic suite FAILED — aborting (pipeline not trusted)")
        sys.exit(1)


def step2_acquire():
    print("== step 2: acquire public data (checksummed) ==")
    acq = load_script("01_acquire.py")
    (ROOT / "data" / "raw").mkdir(parents=True, exist_ok=True)
    return {name: acq.acquire(name, spec) for name, spec in acq.DATASETS.items()}


def compute_synthetic():
    """The numbers in RETRO_REPORT §2 (seeds: data 2/3, estimator 0)."""
    d0 = make_synthetic(leak=0.0, seed=2)
    obs0, _, p0 = lexp_null(d0["a"], d0["b"], d0["A"], d0["W"], n_perm=100, seed=0)
    d1 = make_synthetic(leak=0.12, seed=3)
    obs1, det1 = lexp(d1["a"], d1["b"], d1["A"], d1["W"], seed=0)
    _, _, p1 = lexp_null(d1["a"], d1["b"], d1["A"], d1["W"], n_perm=100, seed=0)
    ns = marginal_ns(d1["a"], d1["b"], d1["A"])
    return dict(
        leak0=dict(obs=float(obs0), p=float(p0),
                   five_floor=float(5 * sensitivity_bound(len(d0["A"])))),
        leak012=dict(obs=float(obs1), p=float(p1), detector=det1),
        leak012_marginal_max_z=float(max(abs(z) for _, z in ns.values())),
        leak012_chsh_S=float(chsh_S(d1["a"], d1["b"], d1["A"], d1["B"])),
    )


def compute_calibration(loaders, cal):
    """The numbers in RETRO_REPORT §1/§3 baseline and RETRO2 §2 (E2/E3)."""
    out = {}
    for name, load in (("delft1", loaders.load_delft1),
                       ("delft2", loaders.load_delft2)):
        d = load()
        s = d["strict"]
        a, b, A, B = d["a"][s], d["b"][s], d["A"][s], d["B"][s]
        psi_plus = d["psi_plus"][s]
        c = ((-1.) ** (a * (b + psi_plus.astype(int))) * (A * B) + 1) / 2
        n, k = int(s.sum()), int(c.sum())
        p = cal.binom_sf(k, n, cal.KSI)
        res = cal.chsh_with_psi(a, b, A, B, psi_plus)
        entry = dict(n=n, k=k, p=float(p))
        for psi, r in res.items():
            if r is not None:
                entry[psi] = dict(S=round(float(r["S"]), 12),
                                  Serr=round(float(r["Serr"]), 12), n=r["n"])
        both = [r for r in res.values() if r is not None]
        if len(both) == 2:
            ntot = sum(r["n"] for r in both)
            entry["combined_S"] = float(sum(r["S"] * r["n"] / ntot for r in both))
        zs = []
        for aa, bb, AA in ((d["a"], d["b"], d["A"]), (d["b"], d["a"], d["B"])):
            for strict_only in (True, False):
                m = s if strict_only else np.ones(len(AA), bool)
                zs += [z for _, z in marginal_ns(aa[m], bb[m], AA[m]).values()]
        entry["marginal_ns_max_abs_z"] = float(max(abs(z) for z in zs))
        out[name] = entry
    # ETH (E2/E3)
    d = loaders.load_eth2023()
    a, b, A, B = d["a"], d["b"], d["A"], d["B"]
    from src.chsh import SIGNS, correlators
    E = correlators(a, b, A, B)
    counts = np.array([[np.sum((a == ai) & (b == bi)) for bi in (0, 1)]
                       for ai in (0, 1)])
    errs = np.sqrt((1 - E ** 2) / counts)
    best = max((abs(float(np.dot(sg, E.ravel()))) for sg in SIGNS))
    Serr = float(np.sqrt((errs.ravel() ** 2).sum()))
    zs = [z for _, z in marginal_ns(a, b, A).values()] + \
         [z for _, z in marginal_ns(b, a, B).values()]
    out["eth2023"] = dict(n=int(len(A)), S=float(best), Serr=Serr,
                          violation_z=float((best - 2) / Serr),
                          marginal_z=[float(z) for z in zs],
                          E=[float(x) for x in E.ravel()])
    return out


def compute_witness(loaders, ws):
    """The 12 pre-registered tests of RETRO_REPORT §3 (seed 0, n_perm 1000)."""
    out = []
    for load in (loaders.load_delft1, loaders.load_delft2, loaders.load_pooled):
        d = load()
        for set_name, m, min_cell in (
                ("primary", np.ones(len(d["A"]), bool), 50),
                ("strict", d["strict"], 15)):
            a, b, A, B, W = (d["a"][m], d["b"][m], d["A"][m], d["B"][m], d["W"][m])
            for tag, args in (
                    (f"{d['name']}/{set_name}/A-vs-b", (a, b, A, W, min_cell)),
                    (f"{d['name']}/{set_name}/B-vs-a (mirror)", (b, a, B, W, min_cell))):
                rec = ws.run_one(tag, *args)
                out.append({k: rec[k] for k in
                            ("tag", "n", "obs", "p", "null_q95", "floor", "verdict")})
    return out


def compute_kill(loaders, kp):
    """The kill-protocol numbers of RETRO_REPORT §4 (registered gates)."""
    d = loaders.load_delft1()
    a, b, A, W, day = d["a"], d["b"], d["A"], d["W"], d["day"]
    seeds = {}
    for seed in range(1, 6):
        obs, p, _ = kp.perm_p(a, b, A, W, seed)
        seeds[str(seed)] = dict(obs=float(obs), p=float(p))
    halves = {}
    med = np.median(day)
    for name, m in (("early", day <= med), ("late", day > med)):
        obs, p, _ = kp.perm_p(a[m], b[m], A[m], W[m], seed=0)
        halves[name] = dict(n=int(m.sum()), obs=float(obs), p=float(p))
    # detector coherence on the original seed-0 split
    rng = np.random.default_rng(0)
    perm = rng.permutation(len(A))
    h = len(A) // 2
    tr, te = perm[:h], perm[h:]
    coherence = {}
    for ai in (0, 1):
        m0t = tr[(a[tr] == ai) & (b[tr] == 0)]
        m1t = tr[(a[tr] == ai) & (b[tr] == 1)]
        m0e = te[(a[te] == ai) & (b[te] == 0)]
        m1e = te[(a[te] == ai) & (b[te] == 1)]
        dv = (A[m0t, None] * W[m0t]).mean(0) - (A[m1t, None] * W[m1t]).mean(0)
        j = int(np.argmax(np.abs(dv)))
        w = dv / (np.linalg.norm(dv) + 1e-12)
        coherence[f"a{ai}"] = dict(
            peak_coord=j,
            coord=float(abs((A[m0e] * W[m0e, j]).mean()
                            - (A[m1e] * W[m1e, j]).mean())),
            linear=float(abs((A[m0e] * np.sign(W[m0e] @ w)).mean()
                             - (A[m1e] * np.sign(W[m1e] @ w)).mean())))
    raw = {}
    for bi in (0, 1):
        m = (a == 0) & (b == bi)
        v = A[m] * W[m, 2]
        raw[f"b{bi}"] = dict(n=int(m.sum()), mean=float(v.mean()),
                             sem=float(v.std() / np.sqrt(m.sum())))
    return dict(seeds=seeds, halves=halves, coherence=coherence,
                raw_stat_A_t1z_a0=raw)


def diff(expected, got, path="", failures=None):
    failures = [] if failures is None else failures
    if isinstance(expected, dict):
        for k, v in expected.items():
            if not isinstance(got, dict) or k not in got:
                failures.append(f"{path}/{k}: missing")
            else:
                diff(v, got[k], f"{path}/{k}", failures)
    elif isinstance(expected, list):
        if not isinstance(got, list) or len(got) != len(expected):
            failures.append(f"{path}: list length {len(got)} != {len(expected)}")
        else:
            for i, (e, g) in enumerate(zip(expected, got)):
                diff(e, g, f"{path}[{i}]", failures)
    elif isinstance(expected, float) or isinstance(got, float):
        if not np.isclose(float(expected), float(got), rtol=RTOL, atol=ATOL):
            failures.append(f"{path}: {got!r} != expected {expected!r}")
    elif expected != got:
        failures.append(f"{path}: {got!r} != expected {expected!r}")
    return failures


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write-expected", action="store_true")
    args = ap.parse_args()
    t0 = time.time()

    step1_synthetic_suite()
    status = step2_acquire()

    loaders_mod = __import__("src.loaders", fromlist=["x"])
    cal = load_script("02_calibrate_parser.py")
    ws = load_script("04_witness_search.py")
    kp = load_script("05_kill_protocol.py")

    print("== step 3: re-derive all published numbers ==")
    computed = {"synthetic": compute_synthetic()}
    delft_ok = status["delft1"] == "ok" and status["delft2"] == "ok"
    if delft_ok or status["eth2023"] == "ok":
        computed["calibration"] = {}
    if delft_ok:
        c = compute_calibration(loaders_mod, cal)
        computed["calibration"].update({k: c[k] for k in ("delft1", "delft2")})
        computed["witness_search"] = compute_witness(loaders_mod, ws)
        computed["kill_protocol"] = compute_kill(loaders_mod, kp)
    if status["eth2023"] == "ok":
        c = compute_calibration(loaders_mod, cal) if not delft_ok else c
        computed["calibration"]["eth2023"] = c["eth2023"]

    REPRODUCED_PATH.write_text(json.dumps(computed, indent=1))
    if args.write_expected:
        EXPECTED_PATH.parent.mkdir(parents=True, exist_ok=True)
        EXPECTED_PATH.write_text(json.dumps(computed, indent=1))
        print(f"expected values written: {EXPECTED_PATH}")
        return 0

    print("== step 4: diff against committed expected values ==")
    expected = json.loads(EXPECTED_PATH.read_text())
    skipped = [k for k, v in status.items() if v != "ok"]
    failures = []
    for section, exp in expected.items():
        if section in computed:
            diff(exp, computed[section], section, failures)
        else:
            print(f"  {section}: SKIPPED (datasets unavailable: {skipped})")
    dt = time.time() - t0
    if failures:
        print(f"\nMISMATCHES ({len(failures)}):")
        for f in failures[:40]:
            print(" ", f)
        print(f"\nREPRODUCTION FAILED in {dt:.0f}s")
        return 1
    n_skip = len(skipped)
    print(f"\nREPRODUCTION OK in {dt:.0f}s "
          f"({'all sections' if n_skip == 0 else f'{n_skip} dataset(s) skipped: {skipped}'}; "
          f"every compared number matches results/expected/expected.json)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
