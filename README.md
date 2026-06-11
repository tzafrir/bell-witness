# bell-witness — a joint-level extended no-signaling check on archival Bell data

To our knowledge this is the first test, on loophole-free Bell-test data, of
whether the **joint** statistics of one wing's outcome together with an
*environment witness* depend on the remote wing's setting. Quantum mechanics
fixes this quantity (`L_exp`, defined below) at exactly zero; a class of
classical-substrate models is forced by theorem to make it positive whenever
Bell is violated and the environment holds records of the hidden state. The
result is a clean, pre-registered null across 12 tests on the Delft 2015/2016
event-ready datasets, bounding **`L_exp` ≲ 0.105 (95%) in the recorded
heralding channel** — a factor ≈ 2.5 below the magnitude the simulated
substrate family predicts (0.25–0.30, parent-program numbers; see §Relation
to the parent program). One sub-threshold anomaly appeared and was killed by
the pre-registered confirmation protocol; the corpse is in the lab notes.

## The observable

```
L_exp = max over (a, C-readout) of | E[A·C | a, b=0] − E[A·C | a, b=1] |
```

`A` is Alice's outcome, `a`/`b` the two wings' settings, and `C` any readout
of an environment record that interacted with the pair near the source (here:
the heralding station's click times and detector channels). Under quantum
mechanics Bob's operation acts on his own tensor factor and commutes with
everything at A⊗C, so `L_exp = 0` exactly, at every decoherence level. All
published no-signaling checks are *marginal* (`E[A|a,b]` flat in `b`); this
joint-with-witness table had not been measured.

## Results (cumulative)

| Dataset | Obtained | Published S reproduced | Witness | Disposition |
|---|---|---|---|---|
| Delft 2015 (Hensen et al., Nature 526:682) | yes, MD5 verified | exact: S=2.422±0.204, k/n=196/245, p=0.039 | yes — station-C heralding records | null; part of pooled bound |
| Delft 2016 (Hensen et al., Sci. Rep. 6:30289) | yes, MD5 verified | exact: S=2.346±0.184, k=237/300, p=0.061 | yes — same | null; part of pooled bound |
| ETH 2023 (Storz et al., Nature 617:265) | yes, MD5 verified | exact: S=2.0747±0.0033, n=2²⁰ | none in public file | calibration-only; marginal NS bounded at ~0.6% |
| NIST 2015 (Shalm et al., PRL 115:250402) | inventoried (docs + public S3) | not parsed (targets on record) | none — nothing recorded at source station | calibration-only, closed without parse |
| Vienna 2015 (Giustina et al., PRL 115:250401) | no public repository | n/a | n/a | unobtainable |

Headline: 12/12 pre-registered `L_exp` tests null; pooled Delft (n = 8664
heralded events) gives observed `L_exp` = 0.028/0.029 against a 95%
permutation-null level of ≈ 0.105, both directions. Full tables:
`results/RETRO_REPORT.md`, `results/RETRO2_REPORT.md`.

## Reproduce everything (one command, ~2 minutes)

```bash
git clone https://github.com/tzafrir/bell-witness && cd bell-witness
pip install -r requirements.txt
make reproduce        # or: python3 reproduce.py
```

This (1) runs the synthetic known-answer suite, (2) downloads the public
datasets with MD5 verification (no data is redistributed in this repo; if a
host is unreachable it tells you which file to fetch manually and skips),
(3) re-derives every number in both reports — calibrations, the 12 `L_exp`
tests, the kill protocol — and (4) diffs them against
`results/expected/expected.json`, exiting nonzero on any mismatch. All
stochastic steps use explicit seeds recorded in the expected values;
permutation tests reproduce exactly under the pinned numpy. Wall-clock on a
clean clone: ~1–2 min after downloads.

## Repository map

```
CONTEXT.md, CONTEXT_RETRO2.md   mission briefs (M-RETRO, M-RETRO-2)
PREREGISTRATION.md              locked analysis plan + dated amendments
data/SOURCES.md                 provenance, checksums, licenses, witness determinations
data/raw/                       gitignored; populated by scripts/01_acquire.py
src/                            chsh.py, lexp.py (the estimator), synthetic.py, loaders.py
scripts/01..05                  acquire, calibrate, validate, witness search, kill protocol
reproduce.py                    single-command re-derivation + diff
results/RETRO_REPORT.md         M-RETRO verdict (Delft; the bound)
results/RETRO2_REPORT.md        M-RETRO-2 verdict (ETH, NIST; contact rationale)
results/LAB_NOTES.md            append-only run record — corpses included
results/expected/expected.json  the numbers reproduce.py must re-derive
contacts/                       data-request drafts (ETH, LMU Munich)
```

## How to audit us

* **Pre-registration predates the runs, provably.** The analysis plan
  (witness features, event sets, statistic, thresholds, kill protocol) was
  committed in `d6ac358` and the first run against real data is `d042d4f`.
  Amendment 1 (ETH/NIST expectations) is `7cb20b0`, committed before the ETH
  ZIP was downloaded; the first run using it is `e64e525`. Check:
  `git log --oneline` and `git show <hash> --stat`.
* **The corpses are kept.** `results/LAB_NOTES.md` is append-only and
  contains: the bug we found in our own synthetic validator (the original
  gadget planted exactly nothing — the recovery test caught it), the
  `delft1/primary/A-vs-b` anomaly (p = 0.004) and its death by every
  registered kill axis (`results/RETRO_REPORT.md` §4), and the voided E4.
* **Scope limits are stated, not buried.** `PREREGISTRATION.md` §9 and the
  report sections list what a null here does *not* exclude (witnesses
  living in unrecorded environment modes; certification limits at archival
  n — registered before the data was run).
* **The estimator was validated on planted answers first**: leak=0 quiet,
  leak=0.12 recovered, and the planted joint leak demonstrably invisible to
  marginal no-signaling (`scripts/03_validate_pipeline.py`).

## Relation to the parent program

This repository is the archival-data arm of a theory+simulation program on
classical-substrate models of quantum measurement. The substrate-side
magnitudes quoted here (predicted `L_exp` ≈ 0.25–0.30 at partial decoherence;
the T4 impossibility theorem forcing `L_exp` > 0 for the model class) are
carried by the parent-program documents, to be mirrored under `docs/`
(`t4_impossibility.md`, `translation-protocol.md`, `literature-survey.md`,
`proposal-v0.html`); see `docs/README.md` for status. This repo's own claims
are only: the pipeline validates on known answers, the published S values
reproduce exactly, and the 12 pre-registered tests are null with the stated
bound. Closest prior art for the logical move (hidden mechanism ⇒
operational signaling): Bancal et al., Nat. Phys. 8:867 (2012),
arXiv:1110.3795.

## Citation

If you use this pipeline or the bound, please cite (see `CITATION.cff`):

```bibtex
@misc{rehan2026bellwitness,
  author    = {Rehan, Tzafrir},
  title     = {bell-witness: a joint-level extended no-signaling check on
               archival loophole-free Bell data},
  year      = {2026},
  publisher = {GitHub},
  url       = {https://github.com/tzafrir/bell-witness},
  note      = {v1.0-archival}
}
```

Data credits: Hensen et al. (4TU.ResearchData, DOIs
10.4121/uuid:6e19e9b2-4a2d-40b5-8dd3-a660bf3c0a31 and
10.4121/uuid:53644d31-d862-4f9f-9ad2-0b571874b829); Storz et al. (ETH
Research Collection, DOI 10.3929/ethz-b-000624026, CC-BY 4.0); NIST Bell
test repository (public domain). No dataset is redistributed here; see
`data/SOURCES.md` for licenses and obligations.

## Contact

Tzafrir Rehan — tzafrir.r@gmail.com. Issues and re-analyses welcome; if you
break the result, that is the system working.
