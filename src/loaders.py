"""Per-dataset parsers -> canonical arrays.

Canonical format (one row per heralded event):
  a, b   : int arrays in {0,1}
  A, B   : int arrays in {-1,+1}
  W      : float array (n, k) witness features (empty (n,0) if none)
  t      : float seconds since epoch (optional)
plus dataset extras: strict (bool published-Bell-trial mask), psi_plus (bool),
day, run, period.

Window parameters are taken verbatim from the experimenters' bundled analysis
scripts (the authoritative column/filter documentation shipped with the data).
"""
from datetime import datetime
from pathlib import Path

import numpy as np

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"

# Column indices in the 17-column open-data CSV (column 0 is the timestamp)
COLS = dict(day=1, run=2, c1t=3, c1c=4, c2t=5, c2c=6, rndA=7, rndB=8,
            rndAt=9, rndBt=10, roA=11, roB=12, exA=13, exB=14, invA=15, invB=16)

READOUT_START = 10620   # ns after sync
READOUT_LEN = 3700      # ns
INVALID_PAST = 250      # sync pulses


def _read_csv(path):
    raw = np.genfromtxt(path, delimiter=",", dtype=np.int64,
                        usecols=range(1, 17))
    with open(path) as f:
        t = np.array([datetime.fromisoformat(line.split(",", 1)[0]).timestamp()
                      for line in f])
    return raw, t


def _outcomes(d):
    inA = (d[:, COLS["roA"] - 1] > READOUT_START) & \
          (d[:, COLS["roA"] - 1] <= READOUT_START + READOUT_LEN)
    inB = (d[:, COLS["roB"] - 1] > READOUT_START) & \
          (d[:, COLS["roB"] - 1] <= READOUT_START + READOUT_LEN)
    return (inA.astype(int) * 2 - 1), (inB.astype(int) * 2 - 1)


def _no_veto(d):
    invA, invB = d[:, COLS["invA"] - 1], d[:, COLS["invB"] - 1]
    okA = (invA == 0) | (invA > INVALID_PAST)
    okB = (invB == 0) | (invB > INVALID_PAST)
    no_exc = (d[:, COLS["exA"] - 1] == 0) & (d[:, COLS["exB"] - 1] == 0)
    return okA & okB & no_exc


def _zscore(x, groups=None):
    x = x.astype(float)
    out = np.empty_like(x)
    if groups is None:
        groups = np.zeros(len(x), dtype=int)
    for g in np.unique(groups):
        m = groups == g
        out[m] = (x[m] - x[m].mean()) / (x[m].std() + 1e-12)
    return out


def witness_features(d, period=None):
    """Pre-registered k=5 witness vector: [ch1, ch2, t1z, t2z, parity].
    All built exclusively from station-C heralding records."""
    ch1 = 2 * d[:, COLS["c1c"] - 1] - 1
    ch2 = 2 * d[:, COLS["c2c"] - 1] - 1
    t1z = _zscore(d[:, COLS["c1t"] - 1], period)
    t2z = _zscore(d[:, COLS["c2t"] - 1], period)
    return np.column_stack([ch1, ch2, t1z, t2z, ch1 * ch2]).astype(float)


def _in_window(time, chan, start0, start1, length):
    return (((start0 <= time) & (time < start0 + length) & (chan == 0)) |
            ((start1 <= time) & (time < start1 + length) & (chan == 1)))


def load_delft1():
    """Hensen et al. 2015. Strict filter: psi-minus heralds only."""
    d, t = _read_csv(RAW / "delft1" / "bell_open_data.txt")
    start0, start1 = 5426350, 5425700
    length, sep = 55000 - 2550, 250000
    c1t, c1c = d[:, COLS["c1t"] - 1], d[:, COLS["c1c"] - 1]
    c2t, c2c = d[:, COLS["c2t"] - 1], d[:, COLS["c2c"] - 1]
    w1 = _in_window(c1t, c1c, start0, start1, length)
    w2 = _in_window(c2t, c2c, start0 + sep, start1 + sep, length)
    psi_min = c1c != c2c
    strict = w1 & w2 & psi_min & _no_veto(d)
    A, B = _outcomes(d)
    return dict(a=d[:, COLS["rndA"] - 1], b=d[:, COLS["rndB"] - 1],
                A=A, B=B, W=witness_features(d), t=t,
                strict=strict, psi_plus=~psi_min,
                day=d[:, COLS["day"] - 1], run=d[:, COLS["run"] - 1],
                period=np.zeros(len(d), dtype=int), name="delft1")


def load_delft2():
    """Hensen et al. 2016 second run. Two APD periods (700 ps delay shift);
    strict filter accepts psi-minus and short-window psi-plus heralds."""
    parts = []
    for pid, (fname, start0) in enumerate([
            ("bell_open_data_2_old_detector.txt", 5426000),
            ("bell_open_data_2_new_detector.txt", 5426000 - 700)]):
        d, t = _read_csv(RAW / "delft2" / fname)
        start1, length, sep = 5425100, 50000, 250000
        plus_len0, plus_len1 = 4000, 2500
        c1t, c1c = d[:, COLS["c1t"] - 1], d[:, COLS["c1c"] - 1]
        c2t, c2c = d[:, COLS["c2t"] - 1], d[:, COLS["c2c"] - 1]
        w1 = _in_window(c1t, c1c, start0, start1, length)
        w2_min = _in_window(c2t, c2c, start0 + sep, start1 + sep, length)
        w2_plus = (((start0 + sep <= c2t) & (c2t < start0 + sep + plus_len0) & (c2c == 0)) |
                   ((start1 + sep <= c2t) & (c2t < start1 + sep + plus_len1) & (c2c == 1)))
        psi_min = c1c != c2c
        strict = ((w1 & w2_min & psi_min) | (w1 & w2_plus & ~psi_min)) & _no_veto(d)
        parts.append((d, t, strict, psi_min, np.full(len(d), pid)))
    d = np.vstack([p[0] for p in parts])
    t = np.concatenate([p[1] for p in parts])
    strict = np.concatenate([p[2] for p in parts])
    psi_min = np.concatenate([p[3] for p in parts])
    period = np.concatenate([p[4] for p in parts])
    A, B = _outcomes(d)
    return dict(a=d[:, COLS["rndA"] - 1], b=d[:, COLS["rndB"] - 1],
                A=A, B=B, W=witness_features(d, period), t=t,
                strict=strict, psi_plus=~psi_min,
                day=d[:, COLS["day"] - 1], run=d[:, COLS["run"] - 1],
                period=period, name="delft2")


def load_pooled():
    """D1 + D2 pooled; z-scoring is per source period (D1 / D2-old / D2-new)."""
    d1, d2 = load_delft1(), load_delft2()
    out = {}
    for key in ("a", "b", "A", "B", "t", "strict", "psi_plus", "day", "run"):
        out[key] = np.concatenate([d1[key], d2[key]])
    out["period"] = np.concatenate([d1["period"], d2["period"] + 1])
    out["W"] = np.vstack([d1["W"], d2["W"]])
    out["name"] = "pooled"
    return out


def load_eth2023():
    """Storz et al. 2023, ETH Zurich. Per-trial (a, A, b, B) only; no witness
    channel exists in the public file (pre-registered determination E1, see
    SOURCES.md). W is the canonical empty (n, 0) array."""
    path = RAW / "eth2023" / "ETH_repo_upload" / "main_dataset_all_events.txt"
    d = np.genfromtxt(path, delimiter=",", dtype=np.int64, skip_header=2)
    a, A, b, B = d[:, 0], d[:, 1], d[:, 2], d[:, 3]
    return dict(a=a, b=b, A=A, B=B, W=np.empty((len(a), 0)), t=None,
                strict=np.ones(len(a), bool), name="eth2023")
