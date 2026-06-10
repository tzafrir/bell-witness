# MISSION HANDOFF — Witness Evidence in Archival Bell Data

This file is the self-contained mission brief for this repository. Read it fully
before writing any code. The science is unusual; the discipline is the point.

## 0. Who you are and what you're doing

You are continuing a fundamental-physics research program as a rigorous,
skeptical collaborator — not a cheerleader. The prior phase (theory +
simulation) produced a falsifiable prediction and an experimental proposal.
Your job now is the cheapest, highest-value next step: search existing public
loophole-free Bell-test data for the predicted signal, and — far more likely —
establish honestly what those datasets can and cannot bound, while building a
validated, reusable analysis pipeline and a precise observable definition for a
future dedicated experiment.

**Prime directive: truth over progress.** A clean null with a believable
sensitivity bound is a success. A "detection" that you did not try your hardest
to kill is a failure. Keep your dead ends in writing.

## 1. The physics, compressed

**Hypothesis class under test.** Models where measurement outcomes are computed
from underlying classical configurations (e.g. graph-rewrite substrates),
proposed as a sub-quantum layer. A theorem (below) shows this whole class must
do something quantum mechanics forbids.

**The observable — `L_exp`.** Standard Bell tests have two wings, Alice
(setting `a`, outcome `A`) and Bob (setting `b`, outcome `B`). Now add a
witness `C`: any record held by an environment/ancilla that interacted with the
pair near the source. Define, for witness readout `C` and settings:

```
L_exp = max over (a, C-readout) of | E[A·C | a, b=0]  -  E[A·C | a, b=1] |
```

i.e. does the joint statistics of Alice's outcome and the witness depend on
Bob's setting?

* Quantum mechanics: `L_exp = 0`, exactly, at every decoherence level. Bob's
  operation acts on his tensor factor and commutes with all of A⊗C. This is
  no-signaling extended to the joint system+environment level.
* Substrate class: `L_exp > 0` whenever the pair still violates Bell and the
  witness holds records of the shared hidden state. In the simulated family the
  optimal-detector leak was 0.25–0.30 (15–26σ above noise), not suppressible by
  adversarial optimization, and relatively largest at partial decoherence —
  exactly the regime real entangled pairs occupy.

**T4 impossibility theorem (the spine).** With (i) setting-independent
preparation and (ii) outcomes that are functions of side-local configurations,
Bell violation implies the existence of an A-side observable whose joint
statistics with A depend on `b`. So `L_exp = 0` while violating is impossible
for the whole class; the only escape is that no physical system can read the
A-side configuration ("micro-inaccessibility" as a brute axiom). Closest prior
art: Bancal et al., Nat. Phys. 8:867 (2012) — finite-speed hidden influences
imply superluminal signaling. Same logical shape (hidden mechanism ⇒
operational signaling); our axis is configuration-disturbance with accessible
records, with measured magnitudes.

**Why no existing analysis already answers this.** Every published
no-signaling check is marginal: `E[A|a,b=0] == E[A|a,b=1]`. Our signal hides in
the joint `(A, C)` and is invisible to marginal checks (the substrate's
marginals are pinned flat by a symmetry). Speed-of-influence experiments
(Salart 2008; Yin 2013) bound propagating mechanisms, not ours. Leggett-model
tests exclude a different class. Quantum-Darwinism experiments prove
environment-record readout is feasible but never in a Bell-with-remote-setting
configuration. The joint-with-witness table is unmeasured.

## 2. The mission, concretely

**Milestone M-RETRO:** produce, for each obtainable public loophole-free Bell
dataset, either (a) a measured `L_exp` with a permutation-based significance
and a sensitivity bound, or (b) a documented reason it cannot be computed (no
witness channel), plus a reproduction of the published `S` and
marginal-no-signaling as parser calibration.

**The witness problem is the crux.** These experiments were not built with a
monitored-decoherence ancilla, so a clean `C` usually does not exist. Rank the
leads:

1. **HIGHEST VALUE — Delft 2015** (Hensen et al., NV centers, event-ready via
   entanglement swapping). Entanglement is heralded by a photonic Bell-state
   measurement at a central station. Those heralding detector records are a
   genuine environment witness correlated with the pair at birth. This is the
   one dataset where a real (if weak) `L_exp` test may be possible. Primary
   target.
2. **MEDIUM** — any dataset with auxiliary channels temporally correlated with
   the source: sync/monitor photodiodes, timing jitter, heralding-arm click
   patterns. Weak, coverage/fidelity unknown, but a bound is a bound.
3. **CALIBRATION-ONLY** — datasets with only `(a,b,A,B,timestamp)`. No witness.
   Use them to validate the parser (reproduce `S`), confirm marginal NS,
   establish the noise floor, and document null sensitivity.

**Do not manufacture a witness from `B` itself** — B is the remote outcome,
not an environment record; using it conflates the very things the test must
separate. If you think you've found a clever proxy, write down why it is or
isn't a legitimate environment record before computing anything with it.

## 3. First acquisition steps (before coding analysis)

1. Web-search for the actual public data repositories — verify URLs and
   formats yourself; do not trust any hardcoded link. Search terms:
   * `Hensen 2015 loophole-free Bell test data repository` (Delft / TU Delft / 4TU.ResearchData)
   * `Shalm 2015 NIST loophole-free Bell data` (NIST often publishes data)
   * `Giustina 2015 Vienna Bell test data`
   * `loophole-free Bell test raw event data download`
2. Record, in `data/SOURCES.md`, for each dataset: paper, DOI, data URL,
   license, file format, and whether any auxiliary/heralding channel is present.
3. Attempt download into `data/raw/` (gitignored). If the sandbox blocks the
   host, stop and tell the user exactly which URL to download manually and
   where to place it — don't fake data.
4. Inspect formats before parsing. Write a small `head`/`describe` step first.

## 4. Repo layout

```
CONTEXT.md              # this file
PREREGISTRATION.md      # filled BEFORE touching real data (see §6)
README.md               # one-paragraph mission + how to run
data/
  SOURCES.md            # acquisition log (§3.2)
  raw/                  # gitignored
  processed/
src/
  chsh.py               # S + marginal no-signaling
  lexp.py               # the L_exp estimator
  synthetic.py          # known-answer validator
  loaders.py            # per-dataset parsers -> canonical arrays
scripts/
  01_acquire.py
  02_calibrate_parser.py   # reproduce published S; confirm marginal NS
  03_validate_pipeline.py  # run synthetic known-answer tests
  04_witness_search.py     # the actual L_exp hunt + permutation null
results/
  LAB_NOTES.md          # append-only; predictions, runs, KEPT CORPSES
tests/
  test_lexp_synthetic.py
```

**Canonical in-memory format** all loaders must produce: `a, b` int arrays in
{0,1}; `A, B` int arrays in {-1,+1}; `W` float array of shape `(n_trials, k)`
of witness features (empty `(n,0)` if none); optional `t` timestamps. One row
per coincidence/heralded trial.

## 5. Code discipline (encoded in src/)

See `src/chsh.py`, `src/lexp.py`, `src/synthetic.py`,
`tests/test_lexp_synthetic.py`. Key points:

* `lexp()` trains its optimal detector on a holdout split (kills selection
  inflation); allowed detector family is one coordinate + one linear (sign)
  direction. Do not expand the detector family post hoc without logging it as
  a new pre-registration.
* `lexp_null()` permutes `b` within each `a` stratum — exact null for "b
  leaks" while preserving the witness/A relationship.
* `sensitivity_bound()` reports the smallest `L_exp` the dataset could have
  revealed (~ 2/sqrt(holdout cell size)).
* `make_synthetic()` is the CALIBRATION GADGET: never trust the pipeline on
  real data until it passes leak=0 (null quiet) and leak≈0.1 (recovery).

## 6. PREREGISTRATION.md — fill BEFORE running on real data

Per dataset, before you look: the witness channel(s) and why each is a
legitimate environment record; the exact `L_exp` statistic (fixed in code);
the significance threshold (permutation p < 0.01 AND obs > 5× sensitivity
floor, both required); the allowed detector scan (coordinate + single linear
direction); and what each outcome will mean. Commit it. Do not edit after
seeing results — append a dated amendment if you must change course, and say
why.

## 7. Order of operations (the confirmation protocol)

1. `03_validate_pipeline.py`: synthetic tests must pass (null quiet, leak
   recovered). If they don't, fix the pipeline before anything else.
2. `02_calibrate_parser.py`: for each real dataset, reproduce the published
   `S` (within stated error) and run `marginal_ns`. A parser that can't
   reproduce `S` is not trusted for `L_exp`.
3. `04_witness_search.py`: only on datasets with a real witness channel,
   compute `L_exp` + permutation null + sensitivity bound. For
   calibration-only datasets, record the sensitivity floor.
4. Confirmation: any apparent signal (p<0.01, obs>5×floor) must be re-derived
   on an independent split seed, on a held-back portion of the data, and
   survive a basis-scan robustness check, before it is written as anything but
   "candidate, unconfirmed."

## 8. results/LAB_NOTES.md — append-only discipline

Every run gets an entry: date, script, dataset, the prediction you registered,
the number you got, and the verdict. Broken predictions and discarded runs
stay in the file. Tag entries `[KEPT CORPSE]` when an approach dies, with the
cause of death.

## 9. Honest expectations

The most probable outcome of M-RETRO is not a detection. It is:

* Delft heralding records might permit a weak `L_exp` test → most likely a
  null with a modest bound (e.g. `L_exp < 0.1`), still the first joint-level
  extended-no-signaling check ever made.
* Other datasets → parser calibration + marginal-NS reproduction + a
  documented "no witness channel; smallest revealable `L_exp` was X."
* A clean, well-characterized null across the board, plus a validated pipeline
  and a precisely defined observable, is the deliverable.

A positive result would be extraordinary and must be disbelieved until it has
survived every kill attempt you can design.

## 10. Definition of done (M-RETRO)

* [ ] `data/SOURCES.md` complete for every reachable dataset (with
      witness-channel determination).
* [ ] Synthetic tests pass; pipeline validated on known answers.
* [ ] Published `S` reproduced and marginal NS confirmed for every parsed
      dataset.
* [ ] `L_exp` + permutation null + sensitivity bound for every witness-bearing
      dataset; sensitivity floor logged for the rest.
* [ ] `results/RETRO_REPORT.md`: per-dataset table (S reproduced?, witness?,
      L_exp, p, bound), an honest verdict, and the strongest single bound the
      archival data yields on the substrate class.
* [ ] `PREREGISTRATION.md` and `LAB_NOTES.md` reflect the true history,
      corpses included.

## 11. Parent-program records (request from the user as needed, into docs/)

`lemma2-lab-notes.html` (v4, master record) · `t4_impossibility.md` (theorem +
proof) · `translation-protocol.md` (observable derivation) · `proposal-v0.html`
(the dedicated experiment) · `literature-survey.md` (prior-art map) ·
`bridging_surface_results.md` & `leak_law_results.md` (measured magnitudes and
scaling laws).

**Key external references:** Bancal et al. Nat. Phys. 8:867 (2012),
arXiv:1110.3795 · Hensen et al. Nature 526:682 (2015) · Shalm et al. and
Giustina et al. PRL 115 (2015) · Salart et al. Nature 454:861 (2008) ·
Gröblacher et al. Nature 446:871 (2007) · bounded-signaling analysis
frameworks arXiv:2602.05507 and arXiv:2511.06624.
