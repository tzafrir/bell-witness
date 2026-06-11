# Releasing

## Tagged release

The archival result is frozen at tag `v1.0-archival`. To cut a future
release: ensure `make reproduce` is green from a clean clone, update
`CITATION.cff` (`version`, `date-released`), commit, then

```bash
git tag -a vX.Y-name -m "one-line description"
git push origin vX.Y-name
```

## Draft release note for v1.0-archival (paste into the GitHub Release UI)

> **v1.0-archival — the archival null and its bound**
>
> Pre-registered joint-level extended no-signaling check on public
> loophole-free Bell data: 12/12 tests null; pooled Delft heralding-channel
> bound **L_exp ≲ 0.105 (95%)**. Published S values of Delft 2015/2016 and
> ETH 2023 reproduced exactly. Every number re-derives with one command:
> `pip install -r requirements.txt && python3 reproduce.py` (~2 min).
> Pre-registration commit hashes and the full append-only lab record
> (corpses included) are in the README's "How to audit us".

## Zenodo DOI (recommended, not yet executed)

So the preprint and data-request emails can cite an immutable DOI rather
than a mutable URL:

1. Log in to https://zenodo.org with the GitHub account that owns the repo.
2. Zenodo → GitHub integration page → flip the toggle for
   `tzafrir/bell-witness`.
3. Publish the GitHub Release for tag `v1.0-archival` (the draft note
   above). Zenodo archives the tagged tree automatically and mints a DOI
   (plus a concept-DOI that always resolves to the latest version).
4. Copy the DOI badge into README.md and add the DOI to `CITATION.cff`
   (`identifiers:` block); commit that as a docs-only follow-up.
5. Use the *version* DOI in the preprint and emails; the repo URL + tag
   remains the human-browsable mirror.

Note: Zenodo archives what is in the tagged tree — which here is code,
prose, and checksums only. The datasets are not ours to archive; their own
DOIs (in `data/SOURCES.md`) are the citable objects for the data.
