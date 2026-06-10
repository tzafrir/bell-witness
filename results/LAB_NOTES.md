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

---

## 2026-06-10 · scripts/02_calibrate_parser.py · D1, D2

**Prediction (registered):** reproduce D1 S=2.42±0.20, k/n=196/245, p=0.039;
D2 S=2.35±0.18; marginal NS null everywhere.

**Result:**
* D1: n=245, k=196, p=0.039, S = +2.422 ± 0.204 — exact match.
* D2: n=300, k=237, p=0.061, combined S = +2.346 ± 0.184; ψ⁻ S=2.309±0.213
  (n=228), ψ⁺ S=2.465±0.368 (n=72). Verified against the paper text
  (arXiv:1603.05705): k₂=237, complete-analysis p=0.061, S=2.35±0.18,
  combined k=433/n=545 — all match.
* Marginal NS: 16 checks (2 datasets × 2 event sets × both directions × 2
  settings), max |z| = 2.23 → null, as expected.

**Verdict:** parser trusted. Cleared for the pre-registered witness search.

---

## 2026-06-10 · scripts/04_witness_search.py · D1, D2, pooled

**Prediction (registered):** QM null — every L_exp consistent with its
permutation null; substrate alternative ≈ 0.25–0.30.

**Result (12 pre-registered tests; n_perm=1000, seed 0):**
11 clean nulls. The most sensitive test, pooled/primary, gave
L_exp = 0.028 (A-vs-b, p=0.91) and 0.029 (B-vs-a, p=0.90) against a null 95%
level of 0.104/0.105. One anomaly: delft1/primary/A-vs-b, L_exp=0.205,
p=0.004 — below the 5×floor certification threshold (0.41), so logged as
"anomaly below certification threshold", kill protocol mandatory. Driving
detector: coordinate t1z (window-1 click time) on a=0 trials. Immediate red
flags noted before the kill run: D1's own strict subset null (p=0.19);
pooled set, which CONTAINS all 4746 D1 events, null (p=0.91).

---

## 2026-06-10 · scripts/05_kill_protocol.py · delft1/primary/A-vs-b · [KEPT CORPSE]

**Registered gates (PREREGISTRATION §6):** survive (i) independent split
seeds 1–5, (ii) held-back temporal halves, (iii) detector-family coherence.
Gate threshold applied: p<0.01 per re-derivation (the registered candidate
threshold; the prereg did not pin the per-rederivation gate numerically —
noted for honesty. Immaterial here: every re-derivation fails even at 0.05).

**Result: KILLED on every axis.**
* (i) seeds 1–5: L_exp = 0.068, 0.037, 0.025, 0.029, 0.070;
  p = 0.60, 0.92, 0.97, 0.96, 0.60. Winning feature changes with seed.
* (ii) temporal halves (by day): early p=0.15, late p=0.75; different
  winning features in each half, neither matching the original (t1z).
* (iii) coherence: on the original seed-0 split, coord detector 0.2047 vs
  linear detector 0.0053 on the same direction — incoherent.
* Raw statistic E[A·t1z | a=0, b]: −0.0059±0.0310 (b=0) vs −0.0780±0.0273
  (b=1): a 1.7σ ripple in the full sample, amplified to 0.205 by one
  particular holdout split. Look-elsewhere: P(min p ≤ 0.004 across the 12
  registered tests) ≈ 4.7%.

**Cause of death:** split-specific noise amplification + selection across 12
tests. Not detector drift, not a temporal artifact, not physics.

**Verdict:** M-RETRO outcome is a clean null across all datasets, all event
sets, both directions. Pooled archival exclusion: L_exp ≲ 0.105 (95% null
level) in the recorded heralding channel — a factor ≈2.5 below the simulated
substrate-family magnitude (0.25–0.30).

---

# M-RETRO-2 (CONTEXT_RETRO2.md)

## 2026-06-10 · PREREGISTRATION Amendment 1 committed

E1–E4 (ETH) and the NIST inventory-before-parse protocol registered and
committed BEFORE downloading the ETH ZIP or opening any NIST file.

---

## 2026-06-10 · acquisition + E1 schema check · ETH 2023

* ETH Research Collection HTML route returns 500 to non-browser fetches;
  the DSpace 7 REST API works (item uuid 100f0077-511e-4765-b6c8-08ff50a0962a).
  ZIP downloaded, MD5 matches repository checksum
  (aa308b354b78d4ba4d8ef5a5457dae1a).
* **E1 confirmed exactly as registered:** `main_dataset_all_events.txt` is
  per-trial (a, A, b, B) only — 2^20 = 1,048,576 trials, no timestamps, no
  auxiliary columns. fig2/fig5 files are aggregates, not event data.
  Witness disposition: calibration-only. **E4 VOID** (no timing column).
  No schema surprise → no stop, no further amendment needed.
* Temptation log (required by the addendum's prohibition clause): none —
  with only (a, A, b, B) per trial the only constructible "witnesses" are
  forbidden ones (neighbor-trial outcomes). Not computed, not explored.

---

## 2026-06-10 · scripts/02_calibrate_parser.py (report_eth) · ETH 2023 · E2+E3

**Prediction (registered):** S = 2.0747 ± 0.0033 at n > 1e6; marginal NS null.

**Result:**
* E2 PASS, exact to all published digits: S = 2.0747 ± 0.0033 at
  n = 1,048,576 trials; violation z = 22.4σ above S = 2; winning sign
  pattern (1,−1,1,1) with E = [+0.529, −0.513, +0.500, +0.533].
* E3: marginal-NS battery (4 z-values): +0.22, −2.12, +0.78, −2.32.
  Max |z| = 2.32 (unremarkable for a 4-test battery, P ≈ 8%). Largest
  proportion shift 0.32% ± 0.14% → marginal setting-dependence bounded at
  ~0.6% (95%) — the tightest marginal-NS reproduction in the project.

**Verdict:** parser trusted on ETH; dataset closed as calibration-only.
No L_exp computable (k = 0 witness columns; `lexp` returns the registered
"no witness channel" disposition).

---

## 2026-06-10 · NIST 2015 channel inventory (A1.2) · determination: NO witness

* The S3 bucket lists publicly (193 keys, complete). Instead of downloading
  a data unit, the official format documentation answered the inventory
  question outright (`File_Folder_Descriptions.pdf`,
  `DataProcessingDescription.pdf` — both saved knowledge into SOURCES.md).
* Per-event channels at BOTH wings (identical): 0 detector click, 2 RNG
  output 0, 4 RNG output 1, 5 GPS PPS, 6 Pockels sync. **Nothing recorded
  at the source station.** GPS/sync are clock/settings infrastructure, not
  environment records of the pair.
* **Determination: NO → calibration-only; full parse not performed**, per
  the registered protocol ("do not sink days into a witness-free archive").
  Floors logged in SOURCES.md (naive 4e-4; click-limited ~2–6e-3).
  Calibration targets recorded for any future parse: 177,358,351 trials,
  p = 5.9e-9 (adjusted 2.3e-7).
* Future-round note (not executed): per-event 78-ps detection timetags do
  exist at both wings → an ETH-E4-class timing-jitter witness is
  conceivable but is outside the registered A1.2 question and would require
  a new amendment + multi-GB parse. Logged to keep the record honest.
