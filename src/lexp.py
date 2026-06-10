import numpy as np


def lexp(a, b, A, W, seed=0, min_cell=50):
    """
    Optimal-detector L_exp on a HOLDOUT split (kills selection inflation).
    a,b in {0,1}; A in {-1,+1}; W shape (n,k) witness features.
    Detector trained on half the data, effect sized on the other half.
    Returns (L_exp, detail dict).  k==0 -> returns 0.0 (no witness).
    """
    n = len(A)
    k = W.shape[1]
    if k == 0:
        return 0.0, {"reason": "no witness channel"}
    rng = np.random.default_rng(seed)
    perm = rng.permutation(n)
    h = n // 2
    tr, te = perm[:h], perm[h:]
    best, detail = 0.0, {}
    for ai in (0, 1):
        m0t = tr[(a[tr] == ai) & (b[tr] == 0)]
        m1t = tr[(a[tr] == ai) & (b[tr] == 1)]
        m0e = te[(a[te] == ai) & (b[te] == 0)]
        m1e = te[(a[te] == ai) & (b[te] == 1)]
        if min(len(m0t), len(m1t), len(m0e), len(m1e)) < min_cell:
            continue
        # train: direction maximizing b-shift of E[A*W_j]
        d = (A[m0t, None] * W[m0t]).mean(0) - (A[m1t, None] * W[m1t]).mean(0)  # (k,)
        j = int(np.argmax(np.abs(d)))
        w = d / (np.linalg.norm(d) + 1e-12)
        # evaluate both a coordinate detector and a linear (sign) detector
        for name, Cfn in (("coord", lambda M: W[M, j]),
                          ("linear", lambda M: np.sign(W[M] @ w))):
            val = abs((A[m0e] * Cfn(m0e)).mean() - (A[m1e] * Cfn(m1e)).mean())
            if val > best:
                best, detail = val, {"a": ai, "detector": name, "coord": j}
    return best, detail


def lexp_null(a, b, A, W, n_perm=200, seed=0):
    """Permutation null: shuffle b labels (within each a) and recompute L_exp.
    Returns (observed, null_samples, p_value). The witness/A relationship is
    preserved; only the b-association is destroyed -> exact null for 'b leaks'."""
    rng = np.random.default_rng(seed)
    obs, _ = lexp(a, b, A, W, seed=seed)
    null = np.empty(n_perm)
    for i in range(n_perm):
        bp = b.copy()
        for ai in (0, 1):
            idx = np.where(a == ai)[0]
            bp[idx] = rng.permutation(b[idx])
        null[i], _ = lexp(a, bp, A, W, seed=int(rng.integers(1 << 30)))
    p = (1 + np.sum(null >= obs)) / (1 + n_perm)
    return obs, null, float(p)


def sensitivity_bound(n_trials, n_cells=4):
    """Crude detectable-effect floor: a b-shift in a holdout mean of a
    +-1 product resolves at ~ 2/sqrt(N_holdout_cell). Report this as the
    smallest L_exp the dataset could have revealed."""
    per_cell = n_trials / (2 * n_cells)  # half held out, split by (a,b)
    return 2.0 / np.sqrt(max(per_cell, 1.0))
