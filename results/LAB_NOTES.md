# LAB NOTES — append-only

Format per entry: date · script · dataset · registered prediction · result ·
verdict. Corpses stay in the file; they are instruments, not embarrassments.

---

## 2026-06-10 · scripts/03_validate_pipeline.py · synthetic · [KEPT CORPSE]

**Prediction:** synthetic known-answer tests pass as shipped in the handoff
brief (leak=0 quiet, leak=0.12 recovered with obs > 0.06).

**Result:** leak=0 PASSED (L_exp=0.0052, p=0.93). leak=0.12 FAILED
(L_exp=0.021, p=0.13 — nothing recovered).

**Diagnosis:** the generator, not the estimator, was broken. The original
gadget added a sub-threshold imprint of size `leak` (=0.12) to a ±1 `base`
inside a `sign()`: since |imprint| < 1, `sign(base + imprint) == base` on
every trial, so the "planted" leak was exactly zero. The estimator correctly
reported no leak. Cause of death: planting mechanism mathematically inert.

**Fix:** probability-flip planting — with prob `leak/2`, overwrite A with the
b-dependent readout `(2b−1)·sign(W0)`, which plants
`E[A·sign(W0)|b=1] − E[A·sign(W0)|b=0] = leak` exactly.

**Lesson kept:** a validator that cannot fail to plant is itself unvalidated.
The leak=0.12 recovery test is exactly what caught this; a pipeline trusted
on real data without it would have produced confident nulls with an estimator
that was never demonstrated to detect anything.

---

## 2026-06-10 · scripts/03_validate_pipeline.py · synthetic (post-fix)

**Prediction:** leak=0 quiet; leak=0.12 recovered; planted joint leak
invisible to marginal NS.

**Result:** PASS on all three.
* leak=0.00: L_exp=0.0052, p=0.931, 5×floor=0.063 → quiet.
* leak=0.12: L_exp=0.1029, p=0.010 (saturated at 1/101 with n_perm=100),
  detector = linear on coord 0 (the planted coordinate) → recovered.
* marginal NS at leak=0.12: max |z| = 1.62 → the joint leak is invisible to
  the standard marginal check, as the theory claims.

**Verdict:** pipeline validated on known answers. Cleared to parse real data.

---

## 2026-06-10 · acquisition (scripts/01_acquire.py; manual web search)

* D1 Delft 2015: downloaded from 4TU.ResearchData, MD5 matches published
  checksum (342f29f8288c46575818acd2acebd535). 4746 heralded events, 17 cols.
  **Witness channel present** (station-C heralding click times + channels).
* D2 Delft 2016 second run: downloaded, MD5 matches
  (de565fc8e550cdd6684b4182d4235d1f). 1047 + 2871 events, two APD periods.
  Witness channel present.
* NIST 2015: repository located (NIST AWS S3, multi-GB ZIP/HDF5 per wing per
  day). No documented witness channel (no heralding station in a CW-pumped
  SPDC design). **Decision: deferred** — see SOURCES.md. Revisit if the
  Delft analysis motivates checking source-side monitor channels.
* Vienna 2015: no public repository exists; prior re-analyses obtained data
  by private communication. Documented unobtainable.

---

## 2026-06-10 · PREREGISTRATION.md committed

Registered before any statistic touched real data: witness features (k=5
heralding-record features), event sets (all-heralded primary / strict
secondary with min_cell 50/15), statistic + null + thresholds, the mirror
direction, calibration targets (D1 S=2.42±0.20 k/n=196/245; D2 S=2.35±0.18),
predictions and pre-computed sensitivity floors (D1 0.082, D2 0.090, pooled
0.061, strict ≈0.33–0.36). Noted in advance: the 5×floor certification rule
cannot certify even a substrate-magnitude (0.25–0.30) leak at single-dataset
archival n — archival data bounds, the dedicated experiment certifies.
