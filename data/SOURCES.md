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
