import numpy as np
from src.synthetic import make_synthetic
from src.lexp import lexp, lexp_null, sensitivity_bound


def test_null_is_quiet():
    d = make_synthetic(leak=0.0, seed=2)
    obs, null, p = lexp_null(d["a"], d["b"], d["A"], d["W"], n_perm=100)
    assert obs < 5 * sensitivity_bound(len(d["A"])), obs
    assert p > 0.05, p


def test_leak_recovered():
    d = make_synthetic(leak=0.12, seed=3)
    obs, _ = lexp(d["a"], d["b"], d["A"], d["W"])
    assert obs > 0.06, obs          # recovers a meaningful fraction
    _, _, p = lexp_null(d["a"], d["b"], d["A"], d["W"], n_perm=100)
    assert p < 0.05
