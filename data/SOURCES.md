# Data acquisition log (M-RETRO §3.2)

All URLs verified by direct fetch on 2026-06-10 unless noted.

## D1 — Delft 2015 (Hensen et al.) — **ACQUIRED, witness lead: HIGH**

* Paper: Hensen et al., *Loophole-free Bell-inequality violation using electron
  spins separated by 1.3 kilometres*, Nature 526, 682 (2015).
  DOI: 10.1038/nature15759, arXiv:1508.05949.
* Data DOI: 10.4121/uuid:6e19e9b2-4a2d-40b5-8dd3-a660bf3c0a31
* Landing page: https://data.4tu.nl/articles/dataset/Loophole-free_Bell-inequality_violation_using_electron_spins_separated_by_1_3_kilometres/12703235
* Direct file: https://data.4tu.nl/file/e8cf2991-3153-48ad-b67d-dfd7d7d97fd3/289c4850-6ed5-45a3-8b19-de8671f873a8
* License: 4TU General Terms of Use.
* Local: `data/raw/delft1_data.zip`, 152,913 bytes,
  MD5 `342f29f8288c46575818acd2acebd535` — **matches published checksum**.
* Format: CSV text (`bell_open_data.txt`), 4746 rows × 17 cols, one row per
  heralded two-photon-signature event at midpoint station C. Column map given
  in the bundled `bell_open_data_analysis_example.py` (authoritative).
* **Witness channel: YES.** Columns 3–6 are the event-ready heralding records
  at location C: window-1/2 detection times (ps after sync) and detector
  channels. These are physical records held by the heralding station that
  interacted with the photons emitted by both NV centres at pair creation —
  exactly the "environment witness" class. Heralding occurs ~5.4–5.9 µs after
  sync; the setting random numbers are recorded ~10.4 µs after sync, so the
  witness record pre-dates the settings on every trial.
* Calibration targets (published): S = 2.42 ± 0.20, k/n = 196/245, p = 0.039.

## D2 — Delft 2016 second run (Hensen et al.) — **ACQUIRED, witness lead: HIGH**

* Paper: Hensen et al., *Loophole-free Bell test using electron spins in
  diamond: second experiment and additional analysis*, Sci. Rep. 6, 30289
  (2016), arXiv:1603.05705.
* Data DOI: 10.4121/uuid:53644d31-d862-4f9f-9ad2-0b571874b829
* Landing page: https://data.4tu.nl/articles/_/12694403/1
* Direct file: https://data.4tu.nl/file/86781ed5-3d14-4ac1-89a9-5e5cddecd748/3ef090cd-4426-48e7-8e77-44d545491667
* License: 4TU General Terms of Use.
* Local: `data/raw/delft2_data.zip`, 131,394 bytes,
  MD5 `de565fc8e550cdd6684b4182d4235d1f` — **matches published checksum**.
* Format: same 17-column CSV, two files for the two APD periods (one detector
  at station C was replaced mid-campaign): `..._old_detector.txt` (1047 rows),
  `..._new_detector.txt` (2871 rows). The new APD has a 700 ps different
  delay; window starts differ per period (bundled script is authoritative).
  Strict trials here include both ψ⁻ and ψ⁺ heralds (short window 2 for ψ⁺).
* **Witness channel: YES** (same heralding records as D1).
* Calibration targets (published): second experiment S = 2.35 ± 0.18;
  combined with D1: S = 2.38 ± 0.14.

## N1 — NIST 2015 (Shalm et al.) — **RECORDED, deferred (no documented witness; multi-GB raw)**

* Paper: Shalm et al., *Strong Loophole-Free Test of Local Realism*,
  PRL 115, 250402 (2015), arXiv:1511.03189.
* Data index: https://www.nist.gov/pml/applied-physics-division/bell-test-research-software-and-data
  (sub-pages: code, compressed data, processed compressed data, raw data from
  servers; files hosted on AWS S3).
* Format: ZIP/HDF5 per station (alice/, bob/) per day (2015_09_18,
  2015_09_19); individual archives 5.4 kB – 1.9 GB.
* Witness determination: the published channel list is settings + outcome
  timestamps per wing; no heralding station (CW-pumped SPDC source, no
  event-ready signal). Sync channels exist but are clock infrastructure, not
  environment records of the pair. **Classification: calibration-only at
  best; MEDIUM lead only if per-event source-side monitor channels turn out
  to exist inside the raw archives.** Deferred in this pass: multi-GB
  undocumented binary downloads are out of proportion to the expected return
  while the Delft witness analysis is open. Revisit decision logged in
  LAB_NOTES.
* Contact per NIST page: lynden.shalm@nist.gov, martin.stevens@nist.gov.

## V1 — Vienna 2015 (Giustina et al.) — **UNOBTAINABLE (no public repository)**

* Paper: Giustina et al., *Significant-Loophole-Free Test of Bell's Theorem
  with Entangled Photons*, PRL 115, 250401 (2015), arXiv:1511.03190.
* Search outcome (2026-06-10): no public data repository found; secondary
  literature that re-analysed this dataset reports obtaining it by private
  communication. No witness channel is described in the paper (CW SPDC, no
  herald). **Classification: unobtainable / would be calibration-only.**
  If the user can obtain the data, place it under `data/raw/vienna/` and it
  becomes a calibration-only target.

## E1 — ETH Zurich 2023 (Storz et al.) — **ACQUIRED, calibration-only**

* Paper: Storz et al., *Loophole-free Bell inequality violation with
  superconducting circuits*, Nature 617, 265 (2023). DOI: 10.1038/s41586-023-05885-0.
* Data DOI: 10.3929/ethz-b-000624026 (ETH Research Collection,
  handle 20.500.11850/624026). License: CC-BY 4.0 per record.
* Direct file (DSpace REST):
  https://www.research-collection.ethz.ch/server/api/core/bitstreams/88466bab-6aba-46e8-bd18-9a62c2c45ea5/content
  (the HTML landing page returns 500 to non-browser fetches; the REST API
  works: item uuid 100f0077-511e-4765-b6c8-08ff50a0962a).
* Local: `data/raw/eth2023_data.zip`, 1,273,595 bytes,
  MD5 `aa308b354b78d4ba4d8ef5a5457dae1a` — **matches repository checksum**.
* Format: `main_dataset_all_events.txt` — 2 header lines + 2^20 = 1,048,576
  trials, one line per trial: `Input Alice, Output Alice, Input Bob,
  Output Bob` (a ∈ {0,1}, A ∈ {−1,+1}, b, B likewise). Also fig2.txt
  (density matrix) and fig5.txt (phase-sweep aggregates) — not event data.
* **Witness determination: NONE — calibration-only, as registered (E1).**
  No per-trial timestamps, no auxiliary channels of any kind; pre-registered
  E4 (timing-jitter witness) is VOID: there is no timing column to use.
  Smallest revealable L_exp had a witness column existed:
  2/sqrt(2^20/8) ≈ 0.0055.
* Calibration targets (published): S = 2.0747 ± 0.0033, >1e6 trials,
  p < 10^-108.
* Contacts: Simon Storz (simon.storz@phys.ethz.ch), Andreas Wallraff.
  Readme states "More data available upon reasonable request."

## N1 — NIST 2015 — UPDATE 2026-06-10 (M-RETRO-2): inventory complete, **witness: NO**

* The S3 bucket lists publicly (193 keys, not truncated):
  `https://s3.amazonaws.com/nist-belltestdata/?list-type=2`. Official
  documentation downloaded and read:
  `belldata/File_Folder_Descriptions.pdf` (+ 2017 addendum),
  `belldata/code/analysis/DataProcessingDescription.pdf`.
* **Definitive per-event channel inventory** (identical at both wings; from
  File_Folder_Descriptions.pdf): raw files are (channel, timetag@78.125 ps,
  transfer#) records with channels 0 = detector click, 2 = RNG output 0,
  4 = RNG output 1, 5 = GPS PPS, 6 = Pockels sync. **Nothing is recorded at
  the source station** — no monitor photodiodes, no heralding arms, no
  source-side counts of any kind. GPS/sync are clock and settings
  infrastructure, not environment records of the pair.
* **Determination (registered question A1.2): NO source-side witness →
  calibration-only; stop without full parse.** Smallest revealable L_exp had
  a witness existed: naive all-trials floor 2/sqrt(1.77e8/8) ≈ 4e-4; the
  realistic click-limited floor (sparse detections, singles ~1e5–1e6 per
  run) is ~2–6e-3.
* Calibration targets if ever parsed: total trials 177,358,351,
  p = 5.9e-9 (adjusted 2.3e-7), PRL 115:250402 Table I.
* Honest note for a future round: per-event detection timetags (78 ps) DO
  exist at both wings, so an ETH-E4-class A-side timing-jitter witness is
  conceivable. That is not a source-side environment record and is outside
  the registered A1.2 question; pursuing it would need a new pre-registration
  amendment plus a multi-GB parse reproducing the published trial definition.
  Logged, not executed.

---

# License determinations (release audit, 2026-06-11)

This repository does **not** redistribute any dataset. It ships download
scripts plus MD5 checksums; data lands in the gitignored `data/raw/`.
Verified license status of each source:

| Source | License (verified) | Verification | Obligations on our use |
|---|---|---|---|
| Delft D1, D2 (4TU.ResearchData) | "4TU General Terms of Use" (DOI 10.4121/resource:terms_of_use); 4TU expects users to cite datasets as scholarly works | dataset landing pages, fetched 2026-06-10 | cite the dataset DOIs and papers (done here and in any output). Note: the release brief stated CC-BY for these; the records themselves say General Terms of Use — we record what the records say. |
| ETH 2023 | **CC-BY 4.0** (`dc.rights.license` = "Creative Commons Attribution 4.0 International") | DSpace item metadata, item uuid 100f0077-…, fetched 2026-06-11 | attribution required: credit Storz et al., data DOI 10.3929/ethz-b-000624026 (done) |
| NIST 2015 | US Government work — public domain (17 U.S.C. §105) | NIST-hosted data, no license file in bucket | none; we cite PRL 115:250402 and the NIST repository as good practice |
| Vienna 2015 | n/a — no data obtained | — | — |
