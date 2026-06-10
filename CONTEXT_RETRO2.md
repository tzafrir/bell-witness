# M-RETRO-2 ADDENDUM — Second-opinion round on open archives

> Extends `CONTEXT.md`; everything there still binds (pre-registration
> before real data, append-only lab notes, corpses kept, truth over
> progress). M-RETRO is complete: clean 12/12 null, pooled Delft bound
> L_exp <~ 0.105 in the recorded heralding channel. This round targets the
> two genuinely OPEN archives and prepares the two contact routes.

---

## Task 1 — ETH Zurich 2023 (open download, calibration-class)

**Dataset.** Storz et al., "Loophole-free Bell inequality violation with
superconducting circuits," Nature 617:265 (2023). Raw data published CC-BY
4.0 on the ETH Research Collection:
- Landing page: https://www.research-collection.ethz.ch/handle/20.500.11850/624026
- DOI: https://doi.org/10.3929/ethz-b-000624026
- File: `Bell_Test_ETHZ_2023_rawData` (ZIP, ~1.2 MB)
- Contacts on record: Simon Storz, Andreas Wallraff.
Verify the URL by search if the fetch fails; do not guess mirrors.

**Registered expectations (write these into PREREGISTRATION.md §addendum
BEFORE opening the ZIP):**
- E1: schema is per-trial settings + outcomes (possibly timestamps); the
  1.2 MB size at >1M trials leaves no room for analog/auxiliary channels.
  Expected witness disposition: **calibration-class** (no environment
  record). If the schema surprises us (any per-trial channel beyond
  a,b,A,B), STOP, amend the pre-registration with the new channel named and
  its legitimacy argued, then proceed.
- E2: calibration gate = reproduce **S = 2.0747 ± 0.0033** (paper headline;
  also reproduce their trial count >1.0e6). Parser is untrusted until this
  passes.
- E3: marginal no-signaling battery at million-trial precision — this will
  be the tightest marginal-NS reproduction in the project; report max |z|
  and the implied marginal bound.
- E4: IF per-trial timestamps exist: A-station timing jitter is a
  *legitimate but extremely weak* witness candidate (a recorded A-side
  degree of freedom; coverage/fidelity unknown and presumably tiny).
  Pre-register it as W before computing anything; expected null. At n ~ 1e6
  the holdout null level is ~2/sqrt(n/8) ≈ 0.006 — i.e. a sub-percent
  L_exp bound is achievable IF any witness column exists. That number is
  the prize that justifies the inspection.

**Forbidden:** constructing W from other trials' outcomes (previous/next
trial A or B). Temporal neighbors are not environment records of the
current pair — same prohibition class as using B itself. If tempted, write
the temptation and its refusal into LAB_NOTES.md.

**Why this dataset matters scientifically despite calibration-class
expectation:** S = 2.075 is a barely-violating experiment, and the parent
program's mechanism law says leak-per-unit-violation is MAXIMAL near the
classical boundary. This is exactly the regime where a witness channel
would shout. The public file likely cannot deliver the witness — but that
is what Task 3's email is for, and the report should state this regime
argument explicitly so the ask has its motivation on paper.

## Task 2 — NIST 2015 resume (open, undocumented, possible hidden witness)

Status from M-RETRO: located, multi-GB, undocumented, deferred. URLs and
notes already in `data/SOURCES.md`.

**Protocol: inventory before parse.**
1. Download the smallest unit (one run file / one day) — not the archive.
2. Channel inventory FIRST: enumerate every per-event field present.
   The single question that matters: do per-event source-side monitor
   channels exist (monitor photodiodes, sync detectors, heralding-arm
   counts, anything recorded at the source station)?
3. If yes → it becomes the second witness-bearing dataset: write the
   pre-registration addendum (channels named, legitimacy argued, the same
   12-test grid structure as Delft), THEN parse fully, calibration gate =
   reproduce the published S/p of PRL 115:250402.
4. If no → log "calibration-only; smallest revealable L_exp = <floor>"
   in SOURCES.md and stop. Do not sink days into a witness-free archive;
   the marginal-NS reproduction at NIST's n is a nice-to-have, not a goal.

## Task 3 — Contact drafts (agent writes, user sends)

Produce `contacts/eth_request.md` and `contacts/munich_request.md`:
short, specific, zero-jargon-waste emails that
- name the exact per-event records requested:
  * ETH (Storz/Wallraff): per-trial readout records beyond the published
    ZIP — raw or integrated IQ readout traces, per-trial timestamps,
    transfer-photon diagnostics if logged.
  * Munich (Weinfurter group, PRL 119:010402): per-event BSM heralding
    records — APD channel IDs and click times for all 4 APDs — plus
    setting bits and outcomes (~tens of thousands of heralded events;
    S = 2.221 ± 0.033 is the calibration gate if granted).
- state the analysis in one sentence (a pre-registered test of whether
  joint outcome+heralding-record statistics depend on the remote setting —
  a quantity QM fixes at exactly zero and no published analysis has
  checked),
- offer the pre-registration document up front (commitment before data),
- note the result is publishable either way and credits the data source,
- and make the no-cost path easy ("if the records were not retained, a
  one-line reply saying so is itself a useful datum for our survey").

## Definition of done (M-RETRO-2)

- [ ] ETH ZIP acquired, schema documented in SOURCES.md, calibration gate
      passed (S = 2.0747 ± 0.0033 reproduced), marginal-NS battery run,
      witness disposition logged; E4 executed iff timestamps exist.
- [ ] NIST channel inventory complete with a yes/no witness determination;
      full parse only on yes.
- [ ] Both contact drafts written and committed.
- [ ] `results/RETRO2_REPORT.md`: same table format as M-RETRO, updated
      strongest-bound statement (currently L_exp <~ 0.105, Delft pooled),
      and an explicit statement of what the open archives can and cannot
      say about the S≈2.07 maximal-leak regime.
- [ ] LAB_NOTES.md appended throughout; any corpse kept and tagged.
