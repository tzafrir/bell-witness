# TASK — Prepare `witness-evidence` for public release

> Goal: this repository becomes the public artifact cited in data-request
> emails to ETH Zurich and LMU Munich, and the companion to a forthcoming
> preprint. Audience: experimental physicists deciding whether to trust us
> with unpublished data. Optimize for: verifiability in 10 minutes, honesty
> on display, zero surprises.

## Governing principle
**Do not sanitize the history.** `LAB_NOTES.md`, the kept corpses, the
killed anomaly, the voided E4, and the bug we found in our own synthetic
gadget are the repository's credibility — they stay, prominently. Clean the
*hygiene*, never the *record*. If any cleanup would alter what a past run
said, stop and flag instead.

## 1. Safety & hygiene audit (do first, report findings)
- Scan full git history (not just HEAD) for: credentials, tokens, API keys,
  absolute local paths, machine names, emails that aren't meant to be
  public. `git log -p | grep`-style sweep plus a secrets scanner if
  available. If history is dirty, propose (don't execute) a remediation.
- Confirm `data/raw/` was never committed (check history, not just
  `.gitignore`). Large-file check: nothing > 5 MB in history.
- Verify no dataset files are redistributed in-repo. We do not re-host
  others' data: the repo ships **download scripts + MD5 checksums**, not
  data. Check each source's license anyway and record it in
  `data/SOURCES.md` (Delft/4TU and ETH are CC-BY — note attribution
  requirements; NIST is public domain US-gov — note it).

## 2. Reproducibility from a clean clone (the 10-minute test)
- `requirements.txt` with pinned versions (the actual ones used).
- A single entry point: `make reproduce` (or `python reproduce.py`) that:
  (1) runs the synthetic known-answer suite, (2) downloads public data via
  the acquire scripts (with checksum verification; skip gracefully if a
  host is unreachable and say which file to fetch manually), (3) re-derives
  every number that appears in `results/RETRO_REPORT.md` and
  `results/RETRO2_REPORT.md`, (4) diffs them against committed expected
  values in `results/expected/*.json` and exits nonzero on mismatch.
- Seeds: every stochastic step takes an explicit seed; the committed
  expected values state theirs. Permutation tests must reproduce exactly.
- Run the whole thing yourself from a fresh clone in a temp dir. Fix what
  breaks. Record the wall-clock time in the README ("reproduces in ~N min").

## 3. README rewrite (public-facing)
Structure: (a) one-paragraph claim — first joint-level extended
no-signaling check on loophole-free Bell data; clean pre-registered null;
L_exp <~ 0.105 (95%), Delft pooled heralding channel; (b) the observable in
5 lines with the QM-predicts-exactly-zero statement; (c) results table
(the cumulative disposition table from RETRO2); (d) `make reproduce`
quickstart; (e) repository map; (f) **"How to audit us"** section pointing
to PREREGISTRATION.md (with commit hashes proving it predates the data
runs — surface those hashes explicitly), LAB_NOTES.md, and the anomaly
kill in RETRO_REPORT §4; (g) relation to the parent program (one
paragraph + docs/ pointers); (h) citation + contact.

## 4. Scientific packaging
- `CITATION.cff` (author: Tzafrir Rehan; title; year 2026; repo URL) and a
  BibTeX block in the README.
- `LICENSE`: MIT for code. State explicitly that *data remains under the
  original sources' licenses* and is not redistributed here.
- `docs/`: include the parent-program documents the user provides
  (t4_impossibility.md, translation-protocol.md, literature-survey.md,
  proposal-v0.html); link, don't summarize.
- `PREREGISTRATION.md`: add a header note listing the commit hash of each
  registration/amendment and the hash of the first run that used it
  (auditability without trusting us).
- Add `results/expected/` JSONs if not already present (they are the diff
  targets for §2).

## 5. Tone pass on prose files
Sweep README and reports for any sentence that oversells. The standard:
every claim either has a number in this repo behind it, or names the file
in the parent program that carries it. Replace "proves/demonstrates the
universe..." style phrasing (if any crept in) with the bounded claim. Keep
the scope-limits paragraphs intact and visible.

## 6. Release mechanics
- Ensure tests pass in CI if CI exists; otherwise add a minimal GitHub
  Action running the synthetic suite + lint on push (no data downloads in
  CI).
- Tag `v1.0-archival`. Draft (don't publish) a GitHub Release note: 5
  lines, the bound, the reproduce command.
- Recommend-but-don't-execute: Zenodo archive of the tagged release for a
  DOI (the preprint and emails can then cite a DOI, not a mutable URL).
  Put the instructions in `RELEASING.md`.

## 7. Final deliverable
`RELEASE_AUDIT.md` summarizing: hygiene findings (and any flagged history
issues), the clean-clone reproduction transcript (timings, all diffs
green), license determinations per dataset, the pre-registration hash
table, and a short list of anything you chose NOT to change because it
would have altered the record. End with the exact text the user should put
in the email placeholder: `[Link]` -> the repo URL + tag.

**Definition of done:** a physicist with no context can clone, run one
command, watch every published number re-derive itself, read the
pre-registration hashes, find the corpses, and conclude we are exactly as
careful as we claim. Nothing more, nothing hidden.
