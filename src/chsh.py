import numpy as np
from itertools import product

# CHSH sign patterns: three plus, one minus (all positions)
SIGNS = [(1, 1, 1, -1), (1, 1, -1, 1), (1, -1, 1, 1), (-1, 1, 1, 1)]


def correlators(a, b, A, B):
    E = np.full((2, 2), np.nan)
    for ai, bi in product((0, 1), (0, 1)):
        m = (a == ai) & (b == bi)
        if m.any():
            E[ai, bi] = np.mean(A[m] * B[m])
    return E


def chsh_S(a, b, A, B):
    E = correlators(a, b, A, B).ravel()  # [E00,E01,E10,E11]
    return max(abs(float(np.dot(s, E))) for s in SIGNS)


def marginal_ns(a, b, A):
    """Two-proportion z for E[A|a,b=0] vs E[A|a,b=1], each a.
    This is the STANDARD existing check; we reproduce it as a baseline and
    to establish that the marginal channel is null (signal must be elsewhere)."""
    out = {}
    for ai in (0, 1):
        m0 = (a == ai) & (b == 0)
        m1 = (a == ai) & (b == 1)
        n0, n1 = int(m0.sum()), int(m1.sum())
        if min(n0, n1) < 50:
            out[ai] = (np.nan, np.nan)
            continue
        k0 = int((A[m0] == 1).sum())
        k1 = int((A[m1] == 1).sum())
        p0, p1 = k0 / n0, k1 / n1
        p = (k0 + k1) / (n0 + n1)
        se = np.sqrt(p * (1 - p) * (1 / n0 + 1 / n1)) + 1e-12
        out[ai] = (p0 - p1, (p0 - p1) / se)  # (shift, z)
    return out
