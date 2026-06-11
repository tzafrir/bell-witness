# RELEASE AUDIT — v1.0-archival (2026-06-11)

Final deliverable of `RELEASE_TASK.md`. Everything below was verified on the
commit this file ships in; the tag `v1.0-archival` points at it.

> **Tag status:** the annotated tag exists locally at the tip of branch
> `claude/charming-brahmagupta-upip67`, but the execution environment's
> push access is scoped to that branch only (tag push returns HTTP 403).
> **One manual step for the maintainer**, after merging/fast-forwarding to
> this branch tip:
> `git tag -a v1.0-archival <branch tip> -m "Archival null: 12/12 pre-registered L_exp tests null; pooled Delft bound L_exp <~ 0.105 (95%)" && git push origin v1.0-archival`
> — or create the tag/release at the branch tip in the GitHub UI using the
> draft note in `RELEASING.md`.

## 1. Hygiene findings (full git history, not just HEAD)

| Check | Result |
|---|---|
| Secrets / tokens / keys (`git log -p` sweep for api_key, secret, token, password, AKIA…, ghp_…, PRIVATE KEY) | **clean** — the only hits are `.streamlit/secrets.toml` *pattern lines inside the stock `.gitignore`*, not secrets |
| Absolute local paths / machine names (`/home/…`, `/Users/…`, `/root/…`, `C:\`) | **clean** — zero occurrences in any committed blob |
| Emails in history | `noreply@anthropic.com` (commit author), `tzafrir.r@gmail.com` (repo owner's git author identity + deliberate public contact in README/CITATION), `simon.storz@phys.ethz.ch`, `lynden.shalm@nist.gov`, `martin.stevens@nist.gov` (professional contacts taken from the sources' own public pages). **Nothing unintended.** |
| `data/raw/` ever committed | **never** — no data file, `.zip`, `.h5`, or dataset `.txt` appears in any commit |
| Large files | largest blob in history is **12 KB** (a Markdown file); nothing within three orders of magnitude of the 5 MB limit |
| Dataset redistribution | none — the repo ships download scripts + MD5 checksums only |

**Flagged, remediation proposed but NOT executed:** the initial commit's
author identity is `Tzafrir Rehan <tzafrir.r@gmail.com>`. If that email were
ever to be removed it would require a full history rewrite
(`git filter-repo --email-callback`), which would change every commit hash
and destroy the pre-registration hash chain that is the repository's core
credibility artifact. Since the same email is deliberately published as the
contact address, we recommend leaving history untouched.

## 2. Clean-clone reproduction (the 10-minute test — passed in under 1)

Procedure: `git clone <repo> /tmp/bw-clone && cd /tmp/bw-clone &&
python3 reproduce.py` on Python 3.11.15 with `requirements.txt` pinned
versions (numpy 2.4.6, pytest 9.0.3). Transcript tail:

```
== step 1: synthetic known-answer suite (pytest) ==  2 passed
== step 2: acquire public data (checksummed) ==
[delft1] md5 342f29f8288c46575818acd2acebd535 OK
[delft2] md5 de565fc8e550cdd6684b4182d4235d1f OK
[eth2023] md5 aa308b354b78d4ba4d8ef5a5457dae1a OK
== step 3: re-derive all published numbers ==
   (12 pre-registered L_exp tests print identically to RETRO_REPORT §3)
== step 4: diff against committed expected values ==
REPRODUCTION OK in 55s (all sections; every compared number matches
results/expected/expected.json)
real    0m55.186s
```

Coverage of the diff: synthetic validation numbers, D1/D2 calibration
(n, k, p, S per ψ-sector, marginal-NS max |z|), ETH calibration (S, error,
violation z, four marginal z's, all four correlators), all 12 witness tests
(obs, p, null 95%, floor, verdict strings), and the full kill protocol
(5 seeds, 2 temporal halves, 4 coherence numbers, the raw implicated
statistic). Float tolerance 1e-9 relative; seeds are stated in
`reproduce.py` and fixed in the scripts. CI (`.github/workflows/ci.yml`)
runs lint + the synthetic suite only — no data downloads in CI.

## 3. License determinations (also recorded in `data/SOURCES.md`)

| Source | License | Our obligation |
|---|---|---|
| Delft D1/D2 (4TU.ResearchData) | "4TU General Terms of Use" (DOI 10.4121/resource:terms_of_use) | cite dataset DOIs + papers — done. **Discrepancy flag:** the release brief asserted CC-BY; the dataset records themselves say General Terms of Use, and we recorded what the records say. |
| ETH 2023 | CC-BY 4.0 (verified in DSpace `dc.rights.license` metadata) | attribution — given in README, SOURCES, reports |
| NIST 2015 | US Government work, public domain (17 U.S.C. §105) | none; cited as good practice |
| Code/prose of this repo | MIT (`LICENSE`), with an explicit scope note that data is not redistributed and remains under the original licenses | — |

## 4. Pre-registration hash table (also in README and PREREGISTRATION header)

| Registration | Commit | First run using it | Verify |
|---|---|---|---|
| Original plan §1–§9 (witness features, event sets, statistic, thresholds, kill protocol) | `d6ac358` | `d042d4f` (calibration, 12-test search, kill protocol, RETRO report) | `git show d6ac358 --stat` |
| Amendment 1 (ETH E1–E4, NIST A1.2) | `7cb20b0` | `e64e525` (ETH calibration, NIST inventory, RETRO2 report) | `git show 7cb20b0 --stat` |

The PREREGISTRATION.md auditability header was added 2026-06-11 as a
clearly-dated **addition**; no registered content was edited.

## 5. Deliberately NOT changed (record preservation)

1. `results/LAB_NOTES.md` — untouched in this release pass. The synthetic
   -gadget corpse, the killed anomaly, and the voided E4 stay verbatim.
2. **Git history not rewritten** — including the author email noted in §1
   and the absence of session links on the four pre-release commits.
   Rewriting would alter the pre-registration hash chain.
3. `results/witness_search.json` — the original run's machine output, kept
   as committed by run commit `d042d4f`.
4. All numbers in both reports — the tone pass (§6 below) touched claim
   *phrasing* only, never a number, table, or verdict.
5. The brief's "Delft is CC-BY" claim was **not** copied into SOURCES.md;
   the verified license label is recorded instead (flagged in §3).

## 6. Tone-pass change log (phrasing only)

* "first … ever run" → "to our knowledge the first" (README, RETRO_REPORT).
* "most sensitive L_exp test ever done" → "~17× more sensitive than the
  current Delft bound (floor ~0.006 vs 0.105)" (RETRO2 §4).
* "only other event-ready archive in existence" → "… we are aware of"
  (RETRO2, Munich letter).
* "by two orders of magnitude" → "by more than an order of magnitude"
  (ETH letter; 0.105→0.006 is ≈17×, not ≈100×).
* "double the world's heralded-witness statistics" → "double the available
  heralded-witness statistics" (Munich letter).

## 7. Email placeholder text

Replace `[Link]` in the contact drafts with exactly:

```
https://github.com/tzafrir/bell-witness/tree/v1.0-archival
```

(After executing the Zenodo step in `RELEASING.md`, prefer citing the
minted version DOI in the preprint and keep the URL above as the
human-browsable mirror.)
