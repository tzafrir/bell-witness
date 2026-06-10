import numpy as np


def make_synthetic(n=200_000, leak=0.0, k=8, seed=1):
    """Known-answer validator. leak=0 -> L_exp ~ noise; leak>0 -> recover it.
    This is the CALIBRATION GADGET: never trust the pipeline on real data
    until it passes leak=0 (null) and leak=0.12 (recovery).

    Planting mechanism: with probability leak/2 a trial's A is overwritten by
    a b-dependent readout of witness coordinate 0, so
        E[A*sign(W0) | b=1] - E[A*sign(W0) | b=0] = leak
    exactly, i.e. the planted L_exp (sign detector on coord 0) equals `leak`
    by construction.

    NOTE [2026-06-10, KEPT CORPSE]: the original gadget added a sub-threshold
    imprint of size `leak` to a +-1 base inside a sign(): |imprint| < 1 can
    never flip a +-1 base, so it planted exactly nothing and the recovery test
    failed. The estimator was fine; the generator was broken. See LAB_NOTES.
    """
    rng = np.random.default_rng(seed)
    a = rng.integers(0, 2, n)
    b = rng.integers(0, 2, n)
    W = rng.normal(size=(n, k))
    A = np.sign(W[:, 1] + 0.5 * rng.normal(size=n) + 1e-9).astype(int)  # structure, no leak
    flip = rng.random(n) < leak / 2                                     # the planted leak
    A[flip] = ((2 * b - 1) * np.sign(W[:, 0] + 1e-12))[flip].astype(int)
    B = (-A * np.sign(W[:, 2] + 0.5 * rng.normal(size=n) + 1e-9)).astype(int)  # for CHSH
    return dict(a=a, b=b, A=A, B=B, W=W)
