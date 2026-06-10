# M-RETRO-2 REPORT — Second-opinion round on open archives

**Date:** 2026-06-10 · **Plan:** `PREREGISTRATION.md` Amendment 1 (committed
before any new data was opened) · **Run record:** `LAB_NOTES.md` ·
**Extends:** `results/RETRO_REPORT.md` (M-RETRO, Delft, clean 12/12 null).

## TL;DR

Both genuinely open archives are now closed out. ETH 2023 reproduces
**exactly** (S = 2.0747 ± 0.0033 to all published digits, n = 2²⁰ trials)
and is calibration-only as registered — the public file carries no witness
channel, so the registered timing-jitter test (E4) is void, not failed.
NIST 2015's channel inventory is now definitive from the official format
documentation: **nothing is recorded at the source station**, so it closes
as calibration-only without a multi-GB parse, per the registered protocol.
The strongest archival bound on the substrate class is unchanged:
**L_exp ≲ 0.105 (95%), Delft pooled heralding channel.** The two contact
drafts that could change this — ETH (sub-percent sensitivity at the
maximal-leak operating point) and Munich (the only other event-ready
archive) — are written and committed in `contacts/`.

## 1. Dataset disposition (cumulative, all rounds)

| Dataset | Obtained | S reproduced | Witness | Disposition |
|---|---|---|---|---|
| D1 Delft 2015 | yes, MD5 ok | exact (2.422±0.204, 196/245, p=0.039) | yes — heralding records | null; part of pooled bound |
| D2 Delft 2016 | yes, MD5 ok | exact (2.346±0.184, 237/300, p=0.061) | yes — heralding records | null; part of pooled bound |
| **E1 ETH 2023** | **yes, MD5 ok** | **exact (S = 2.0747 ± 0.0033, n = 1,048,576, 22.4σ)** | **none** — per-trial (a,A,b,B) only; E4 void | **calibration-only**; floor had a witness existed: 0.0055 |
| **N1 NIST 2015** | docs + bucket inventory | not parsed (targets recorded: 177,358,351 trials, p=5.9e-9) | **none** — channels are click/RNG/GPS/sync per wing; nothing at source station | **calibration-only, closed without full parse** (registered A1.2 step 4) |
| V1 Vienna 2015 | no public repository | n/a | n/a | unobtainable |

## 2. ETH 2023 detail (Tasks E1–E4)

* **E1 (schema):** confirmed exactly as registered before opening the ZIP —
  2 header lines + 2²⁰ trial lines of `a, A, b, B`; no timestamps, no
  auxiliary channels; fig2/fig5 are aggregates. No schema surprise → no
  amendment triggered.
* **E2 (calibration):** S = 2.0747 ± 0.0033 — equal to the published
  headline to all four decimals; E = [+0.529, −0.513, +0.500, +0.533];
  violation 22.4σ above 2.
* **E3 (marginal NS at million-trial precision):** battery z-values
  {+0.22, −2.12, +0.78, −2.32}; max |z| = 2.32 is unremarkable for a 4-test
  battery (~8% by chance). Largest proportion shift 0.32% ± 0.14% →
  marginal setting-dependence bounded at ≈ 0.6% (95%). Tightest marginal-NS
  reproduction in the project.
* **E4 (conditional witness):** void — there is no timing column. The
  registered prize (a sub-percent L_exp bound, floor ≈ 0.0055) is exactly
  what the public file cannot deliver and what the ETH contact letter asks
  for.
* **Prohibition compliance:** no neighbor-trial construction was computed or
  explored; with only (a,A,b,B) per trial every constructible "witness" is
  in the forbidden class. Logged in LAB_NOTES.

## 3. NIST 2015 detail (Task 2)

The inventory question was answered from the official documentation rather
than a sample download — stronger than one file's schema, since
`File_Folder_Descriptions.pdf` specifies the complete channel map for all
runs: per wing, channels 0 (detector click), 2/4 (RNG output 0/1), 5 (GPS
PPS), 6 (Pockels sync); raw records are (channel, 78.125-ps timetag,
transfer#). There is no source-station recording of any kind — no monitor
photodiodes, no heralding arms. GPS/sync are infrastructure, not
environment records of the pair.

**Determination: NO witness → calibration-only, full parse not performed.**
Floors had a witness existed: naive all-trials 2/√(1.77e8/8) ≈ 4×10⁻⁴;
realistic click-limited ~2–6×10⁻³. Calibration targets for any future
parse are on record (Table I of PRL 115:250402). One honest loose end is
logged: per-event detection timetags would support an ETH-E4-class
*A-side timing-jitter* witness in a future round — that is not a
source-side environment record, sits outside the registered question, and
would require a new pre-registration amendment plus a multi-GB parse.

## 4. The S ≈ 2.07 maximal-leak regime: what open archives can and cannot say

The parent program's mechanism law predicts leak-per-unit-violation is
maximal near the classical boundary. ETH 2023 (S = 2.075, barely violating,
>10⁶ trials) is therefore the single most diagnostic operating point in the
archival record: a witness channel there would resolve L_exp down to
~0.006 — seventeen times below the Delft bound and ~50× below the simulated
substrate magnitude. **The open archives cannot make this measurement:**
the only event-level records published for ETH are settings and outcomes,
and the joint-with-witness table needs at least one recorded auxiliary
degree of freedom. This is not a deficiency of the experiments — no one had
a reason to publish such channels — it is the precise, on-paper motivation
for the two data requests:

* **ETH** retains (per the readme, "more data available upon reasonable
  request") possibly IQ readout traces, per-trial timestamps, or
  transfer-photon diagnostics → any one of them turns the most diagnostic
  operating point into the most sensitive L_exp test ever done.
* **Munich** (Rosenfeld et al. 2017, event-ready atoms, S = 2.221 ± 0.033)
  is the only other heralded-architecture archive in existence; its 4-APD
  BSM records are the same witness class as Delft and would roughly double
  the world's heralded-witness statistics.

## 5. Strongest-bound statement (unchanged)

> **L_exp ≲ 0.105 (95%), Delft 2015+2016 pooled, station-C heralding
> channel** — excluding substrate-class models whose hidden-configuration
> records imprint on that recorded channel at the simulated-family magnitude
> (0.25–0.30). ETH and NIST add exact parser calibrations and
> million/hundred-million-trial marginal baselines, but no new joint-channel
> constraint: their public records carry no witness.

## 6. Definition of done (M-RETRO-2)

- [x] ETH ZIP acquired (MD5 verified), schema documented in SOURCES.md,
      calibration gate passed exactly, marginal-NS battery run, witness
      disposition logged; E4 determined void (no timestamps exist).
- [x] NIST channel inventory complete with a definitive NO witness
      determination; full parse correctly not performed.
- [x] Both contact drafts written and committed (`contacts/`).
- [x] This report, with the regime statement (§4) and the unchanged
      strongest bound (§5).
- [x] LAB_NOTES.md appended throughout; no new corpses this round (the one
      registered conditional, E4, died by voidness, not by failure — that
      distinction is recorded).
