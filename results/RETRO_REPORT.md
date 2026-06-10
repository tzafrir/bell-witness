# M-RETRO REPORT — Witness search in archival loophole-free Bell data

**Date:** 2026-06-10 · **Analysis plan:** `PREREGISTRATION.md` (committed
before any statistic touched real data) · **Run record:** `LAB_NOTES.md`
(append-only, corpses included) · **Raw numbers:** `witness_search.json`

## TL;DR

A clean, pre-registered null. The first joint-level extended-no-signaling
check (`L_exp`) ever run on loophole-free Bell data finds no dependence of
the joint (outcome, environment-witness) statistics on the remote setting, in
either direction, in any dataset or event set. The pooled Delft data bounds
`L_exp ≲ 0.105` (95% permutation-null level) in the recorded heralding
channel — a factor ≈ 2.5 below the 0.25–0.30 magnitude of the simulated
substrate family. One split-level fluctuation appeared and was killed by the
pre-registered confirmation protocol. The pipeline is validated end-to-end on
planted known answers and reproduces every published headline number of both
Delft experiments to the digit.

## 1. Dataset disposition

| Dataset | Obtained | S reproduced | Witness channel | Disposition |
|---|---|---|---|---|
| D1 Delft 2015 (Nature 526:682) | yes, MD5 verified | **yes, exact**: S=2.422±0.204, k/n=196/245, p=0.039 | yes — station-C heralding click times + channels | witness search run |
| D2 Delft 2016 (Sci. Rep. 6:30289) | yes, MD5 verified | **yes, exact**: S=2.346±0.184, k=237/n=300, p=0.061 (and ψ⁻/ψ⁺ subsets, combined k=433/n=545 all match paper) | yes — same | witness search run |
| NIST 2015 (PRL 115:250402) | located, deferred | n/a | none documented (no heralding station; CW SPDC) | calibration-only at best; multi-GB undocumented raw deferred — see `data/SOURCES.md` |
| Vienna 2015 (PRL 115:250401) | **no public repository** | n/a | none described | unobtainable; smallest revealable L_exp: n/a (no event data) |

Marginal no-signaling (the standard published check): null in all 16
configurations (2 datasets × 2 event sets × both directions × 2 settings),
max |z| = 2.23 — confirming the parser and that any signal must live in the
joint channel, where no one had looked.

## 2. Pipeline validation (known answers, before real data)

* leak = 0: L_exp = 0.005, p = 0.93 → quiet.
* leak = 0.12 planted: L_exp = 0.103 recovered on the planted coordinate,
  p = 0.010 (saturated at n_perm=100) → recovered.
* The planted *joint* leak is invisible to marginal NS (max |z| = 1.62) —
  demonstrating on synthetic data the central claim that marginal checks
  cannot see this signal.
* [KEPT CORPSE] The handoff's original synthetic gadget planted exactly
  nothing (sub-threshold imprint inside a sign() of a ±1 base); the recovery
  test caught it and the planting was fixed before any real data was parsed.

## 3. Witness search results (all 12 pre-registered tests)

Witness `W` (k=5, fixed in advance): window-1/2 detector channel, z-scored
window-1/2 click time, channel parity — all exclusively station-C heralding
records, recorded ~5 µs before the setting bits exist.

| Test | n | L_exp | p (1000 perms) | null 95% | 5×floor | Verdict |
|---|---|---|---|---|---|---|
| delft1/primary/A-vs-b | 4746 | 0.2047 | 0.0040 | 0.146 | 0.411 | anomaly → **killed** (§4) |
| delft1/primary/B-vs-a | 4746 | 0.0265 | 0.971 | 0.139 | 0.411 | null |
| delft1/strict/A-vs-b | 245 | 0.4496 | 0.192 | 0.599 | 1.807 | null |
| delft1/strict/B-vs-a | 245 | 0.3386 | 0.398 | 0.605 | 1.807 | null |
| delft2/primary/A-vs-b | 3918 | 0.0831 | 0.550 | 0.159 | 0.452 | null |
| delft2/primary/B-vs-a | 3918 | 0.0998 | 0.331 | 0.152 | 0.452 | null |
| delft2/strict/A-vs-b | 300 | 0.0840 | 0.972 | 0.540 | 1.633 | null |
| delft2/strict/B-vs-a | 300 | 0.2312 | 0.629 | 0.556 | 1.633 | null |
| pooled/primary/A-vs-b | 8664 | 0.0278 | 0.905 | 0.104 | 0.304 | null |
| pooled/primary/B-vs-a | 8664 | 0.0291 | 0.896 | 0.105 | 0.304 | null |
| pooled/strict/A-vs-b | 545 | 0.0979 | 0.887 | 0.402 | 1.212 | null |
| pooled/strict/B-vs-a | 545 | 0.3143 | 0.160 | 0.396 | 1.212 | null |

## 4. The anomaly and its death

`delft1/primary/A-vs-b` hit p = 0.004 (below the registered p<0.01) but at
0.205 was well under the 5×floor certification threshold (0.411) → logged as
"anomaly below certification threshold", kill protocol mandatory. It failed
**every** registered confirmation axis:

* Independent holdout seeds 1–5: p = 0.60 / 0.92 / 0.97 / 0.96 / 0.60, with
  the winning feature changing from seed to seed.
* Held-back temporal halves (by day): p = 0.15 / 0.75, different winning
  features in each half, neither the original.
* Detector-family coherence: on the original split, 0.205 (coordinate) vs
  0.005 (linear) — incoherent.
* The implicated raw statistic is a 1.7σ ripple in the full sample;
  look-elsewhere across the 12 registered tests gives ≈ 4.7% for one p ≤
  0.004 by chance; and the pooled superset containing all 4746 D1 events is
  flat (p = 0.91), which no physical leak would permit.

**Cause of death: split-specific noise amplification + multiplicity.**

## 5. The strongest archival bound

From pooled/primary (n = 8664, both directions): observed L_exp = 0.028 /
0.029 against a 95% permutation-null level of ≈ 0.105.

> Substrate-class models whose hidden-configuration records imprint on the
> *recorded* heralding channel (station-C click times and detector channels)
> at the simulated-family magnitude L_exp ≈ 0.25–0.30 are **excluded** by
> archival Delft data; the archival exclusion level in that channel is
> **L_exp ≲ 0.105** (95%).

Honest scope limits (registered in advance, PREREGISTRATION §9):
* The witness is coarse — 2 binary channels + 2 timestamps. Substrates whose
  records live in unrecorded environment modes are not constrained.
* The 5×floor certification rule could not have certified even a true
  0.25–0.30 effect at single-dataset archival n; archival data bounds, a
  dedicated experiment certifies. This was stated before the data was run.
* n_perm = 1000 caps reportable p at ~0.001.

## 6. What this feeds forward

* A validated, reusable `L_exp` pipeline (holdout optimal detector +
  stratified permutation null + planted-leak calibration gadget) and a
  precise observable definition, ready for the monitored-decoherence-ancilla
  Bell experiment proposed in the parent program.
* The dedicated experiment needs, to certify a 0.25-magnitude effect at the
  registered 5×floor rule: n ≳ 2·(2·4)·(5·2/0.25)² ≈ 13k heralded trials
  with a designed witness channel — about 1.5× the entire pooled archival
  record, well within reach of a purpose-built run.
* If NIST raw archives turn out to contain per-event source-side monitor
  channels, they become a second witness-bearing dataset; the loader
  interface is ready (`data/SOURCES.md` has the exact URLs and contacts).

## 7. Definition of done — status

* [x] `data/SOURCES.md` complete with witness-channel determination for all
      four target datasets.
* [x] Synthetic known-answer tests pass (after fixing the inert planting
      mechanism — corpse kept).
* [x] Published S reproduced exactly and marginal NS confirmed for every
      parsed dataset (D1, D2).
* [x] L_exp + permutation null + sensitivity bound for every witness-bearing
      dataset (12 tests); sensitivity status documented for NIST (deferred)
      and Vienna (unobtainable).
* [x] This report, with the honest verdict and the strongest single bound.
* [x] `PREREGISTRATION.md` and `LAB_NOTES.md` reflect the true history,
      corpses included.
