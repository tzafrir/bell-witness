# bell-witness — Witness Evidence in Archival Bell Data (M-RETRO)

Search public loophole-free Bell-test data for a b-dependence in the joint
statistics of Alice's outcome and an environment witness (`L_exp`) — a signal
that quantum mechanics forbids exactly but a class of classical-substrate
models requires (see `CONTEXT.md` for the full brief, `PREREGISTRATION.md`
for the locked analysis plan). A clean null with a believable sensitivity
bound is a success; truth over progress.

## How to run

```bash
pip install numpy pytest
python scripts/01_acquire.py            # download Delft open data, verify MD5
python scripts/03_validate_pipeline.py  # synthetic known-answer tests (must pass first)
python scripts/02_calibrate_parser.py   # reproduce published S; marginal NS
python scripts/04_witness_search.py     # the pre-registered L_exp hunt
pytest tests/                           # same known-answer tests, as a suite
```

Results land in `results/` (`LAB_NOTES.md` is the append-only run record,
`RETRO_REPORT.md` the final per-dataset verdict). Raw data lives in
`data/raw/` (gitignored); provenance and checksums in `data/SOURCES.md`.
