# PRE-REGISTRATION — Witness search in archival Bell data

**Status: REGISTERED 2026-06-10, before any statistic was computed on real
data.** At the time of writing, the only operations performed on real data
were: download, checksum verification, `head` of the first rows, and reading
the experimenters' bundled column documentation and analysis scripts. No
correlator, no S, no marginal-NS, no L_exp had been computed.

This file is append-only after this commit. Amendments must be dated and
justified, never edited in place.

---

## 1. Datasets and roles

| ID | Dataset | Role | Witness channel |
|----|---------|------|-----------------|
| D1 | Delft 2015 (Hensen et al., Nature 526:682) | calibration + witness search | heralding records at station C |
| D2 | Delft 2016 second run (arXiv:1603.05705) | calibration + witness search | heralding records at station C |
| D1+D2 | pooled | witness search (highest sensitivity) | same |
| N1 | NIST 2015 (Shalm et al.) | recorded, deferred (see SOURCES.md) | none documented |
| V1 | Vienna 2015 (Giustina et al.) | unobtainable | n/a |

## 2. Why the Delft heralding records are a legitimate environment witness

The event-ready signal at midpoint station C is produced by photodetection of
the two photons that were each entangled with one NV-centre electron spin and
interfered on a beamsplitter (entanglement swapping). The detectors at C are
an environment system that physically interacted with the pair at its
creation. The records — detection times (ps resolution) within window 1 and
window 2 and which APD fired — are stored, classical, per-trial environment
records correlated with the newborn pair state (they determine which Bell
state was heralded). They are recorded at ~5.4–5.9 µs after the sync pulse,
*before* the setting random numbers exist at A and B (~10.4 µs), and are
causally disconnected from Bob's setting choice for the same trial. They are
not derived from outcome B or from either setting.

Under QM, any operation on Bob's factor commutes with everything at A⊗C, so
the joint statistics of (A, C-record) cannot depend on b — at any decoherence
level. Under the substrate class (T4), these records may carry imprints of the
shared hidden configuration, which b-dependent measurement disturbs.

**Explicitly excluded as witnesses:** outcome B, setting b, outcome A, setting
a, anything computed from them, and run/day bookkeeping labels.

## 3. Witness feature vector (fixed, k = 5)

For every heralded event, `W` columns in this exact order:

| j | Feature | Definition |
|---|---------|------------|
| 0 | `ch1` | window-1 detector channel, mapped {0,1} → {−1,+1} |
| 1 | `ch2` | window-2 detector channel, mapped {0,1} → {−1,+1} |
| 2 | `t1z` | window-1 detection time, z-scored |
| 3 | `t2z` | window-2 detection time, z-scored |
| 4 | `parity` | `ch1 · ch2` (+1 = ψ⁺-type herald, −1 = ψ⁻-type) |

Z-scoring uses mean/std over the loaded event set; for D2 it is computed
*within each detector period separately* (the replaced APD has a 700 ps delay
offset which is instrument configuration, not signal). Z-scoring is a fixed
b-blind transform; the permutation null (which permutes b only, holding W
fixed) is exact regardless.

## 4. Event sets

* **PRIMARY ("all-heralded")**: every row of the open data file(s) —
  inclusion requires only the two-photon signature at station C, which is
  b-independent by construction. D1: n = 4746. D2: n = 1047 + 2871 = 3918.
  Pooled: n = 8664. `min_cell = 50`.
* **SECONDARY ("strict-trials")**: the published Bell-trial filter exactly as
  in the experimenters' bundled scripts (event-ready windows, ψ-state
  selection, invalid-marker and excitation-click vetoes). Expected n ≈ 245
  (D1) and n ≈ 300 (D2). Because per-(a,b)-cell holdout counts are ~30,
  `min_cell = 15` for this set only. This is registered *now*, not after
  seeing results.
* Outcome definition (both sets): `A = +1` if a PSB photon is detected at
  location A in the published readout window (10620–14320 ns after sync),
  else −1. Same rule for `B` at location B. This is the experiment's own
  outcome definition applied to all heralded events.

## 5. Statistics (already fixed in code, committed before this run)

* `L_exp` estimator: `src/lexp.py::lexp` — 50/50 holdout split (seed = 0),
  detector trained on train half, effect sized on test half. Detector family:
  best single coordinate + single linear (sign) direction. **This family will
  not be expanded post hoc.**
* Null: `src/lexp.py::lexp_null`, permuting b within each a stratum,
  `n_perm = 1000`, seed = 0.
* Sensitivity floor: `src/lexp.py::sensitivity_bound(n)`.
* Marginal no-signaling: `src/chsh.py::marginal_ns` (baseline reproduction).
* **Mirror test (registered as a co-primary direction):** the T4 argument is
  side-symmetric, so we also compute `L_exp` with roles swapped —
  `lexp(b, a, B, W)` — i.e. does the joint (B, C-record) depend on a? The
  witness is still C; B serves as outcome in its own test, never as witness
  for A's test.

## 6. Decision rule (per dataset × event set × direction)

* **Candidate signal** requires BOTH: permutation p < 0.01 AND
  observed `L_exp` > 5 × `sensitivity_bound(n)`.
* Anything else is a **null**; report the exclusion level as
  max(observed L_exp, 95th percentile of the permutation null).
* A candidate is written up only as "candidate, unconfirmed" until it
  survives ALL of: (i) re-derivation with independent split seeds 1–5,
  (ii) re-derivation on a held-back temporal half of the data (split by run
  number), (iii) detector-family robustness (coordinate vs linear agree in
  sign and rough magnitude). The parent program killed two candidates this
  way; the expectation is death.

## 7. Registered predictions

* Parser calibration: our port of the experimenters' analysis reproduces
  D1: S = 2.42 ± 0.20 (k/n = 196/245, p ≈ 0.039) and D2: S = 2.35 ± 0.18
  (combined ψ⁻/ψ⁺ as in their script). Failure to reproduce = parser is not
  trusted, fix before proceeding.
* Marginal NS: null (|z| < 3) for all datasets — this is the established
  baseline; the substrate's marginals are pinned flat by symmetry, so a
  marginal violation would indicate a data/parser problem, not a discovery.
* QM prediction: every `L_exp` consistent with its permutation null
  (p uniform), observed values ≪ 5×floor.
* Substrate prediction: `L_exp` ≈ 0.25–0.30 in the simulated family. Note,
  registered honestly *in advance*: at D1-primary size (n = 4746) the 5×floor
  is ≈ 0.41, so even a true substrate-magnitude leak would register as
  p < 0.001 but FAIL the 5×floor criterion at single-dataset size; at pooled
  size 5×floor ≈ 0.30, borderline. Archival data can therefore *bound* but
  not cleanly *certify* a substrate-magnitude effect under this rule. We will
  not weaken the rule after seeing data; if p < 0.01 with obs < 5×floor
  occurs, it is reported as "anomaly below certification threshold", subject
  to the same kill protocol, and flagged for the dedicated experiment.
* Sensitivity floors implied by n (computed from the formula, not the data):
  D1-primary 0.082, D2-primary 0.090, pooled 0.061, D1-strict ≈ 0.36,
  D2-strict ≈ 0.33.

## 8. What each outcome will mean

* **All null** (expected): first joint-level extended-no-signaling check on
  loophole-free Bell data; archival exclusion `L_exp < ~0.1–0.15` (pooled
  null 95% level) for substrate models whose records survive in the heralding
  channel; pipeline + observable validated for the dedicated experiment.
* **Anomaly below certification threshold**: kill protocol, then report as
  unconfirmed anomaly with explicit look-elsewhere caveats; design the
  dedicated experiment to target it.
* **Candidate passing §6**: extraordinary; assume artifact; exhaust kill
  protocol; seek independent re-analysis before any claim.

## 9. Known limitations, stated in advance

* The Delft witness is *coarse*: 2 binary channels + 2 timestamps. A
  substrate whose records decohere into unrecorded environment modes (or live
  in the photon degrees of freedom not captured by APD click time/channel)
  is not excluded by a null here. The bound applies to the recorded channel.
* The all-heralded PRIMARY set includes events the experimenters excluded
  from the Bell test (invalid markers, excitation clicks, ψ⁺ window tails).
  Inclusion is b-blind, so the L_exp null logic is exact; but the *physical*
  interpretation of a leak bound is cleanest on the strict set. Both are
  reported.
* n_perm = 1000 limits the smallest reportable p to ~0.001.
