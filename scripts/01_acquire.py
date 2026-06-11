"""Acquire the public datasets into data/raw/ and verify checksums.
Idempotent; skips gracefully (with manual instructions) if a host is
unreachable. See data/SOURCES.md for provenance; URLs verified 2026-06-10/11.
"""
import hashlib
import urllib.request
import zipfile
from pathlib import Path

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"

DATASETS = {
    "delft1": dict(
        url="https://data.4tu.nl/file/e8cf2991-3153-48ad-b67d-dfd7d7d97fd3/289c4850-6ed5-45a3-8b19-de8671f873a8",
        md5="342f29f8288c46575818acd2acebd535",
        zip_name="delft1_data.zip"),
    "delft2": dict(
        url="https://data.4tu.nl/file/86781ed5-3d14-4ac1-89a9-5e5cddecd748/3ef090cd-4426-48e7-8e77-44d545491667",
        md5="de565fc8e550cdd6684b4182d4235d1f",
        zip_name="delft2_data.zip"),
    "eth2023": dict(
        url="https://www.research-collection.ethz.ch/server/api/core/bitstreams/88466bab-6aba-46e8-bd18-9a62c2c45ea5/content",
        md5="aa308b354b78d4ba4d8ef5a5457dae1a",
        zip_name="eth2023_data.zip"),
}


def acquire(name, spec):
    """Returns 'ok', 'skipped' (host unreachable), or 'mismatch'."""
    zpath = RAW / spec["zip_name"]
    if not zpath.exists():
        print(f"[{name}] downloading {spec['url']}")
        req = urllib.request.Request(spec["url"],
                                     headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                zpath.write_bytes(r.read())
        except Exception as e:  # noqa: BLE001 - any network failure -> manual path
            print(f"[{name}] DOWNLOAD FAILED ({e}).\n"
                  f"  Fetch manually from the URL above (or the landing page in\n"
                  f"  data/SOURCES.md) and place the file at {zpath}, then re-run.")
            return "skipped"
    md5 = hashlib.md5(zpath.read_bytes()).hexdigest()
    if md5 != spec["md5"]:
        print(f"[{name}] md5 {md5} MISMATCH (expected {spec['md5']}). "
              f"Delete {zpath} and re-run, or fetch manually per data/SOURCES.md.")
        return "mismatch"
    print(f"[{name}] md5 {md5} OK")
    dest = RAW / name
    if not dest.exists():
        with zipfile.ZipFile(zpath) as z:
            z.extractall(dest)
        print(f"[{name}] extracted to {dest}")
    return "ok"


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    status = {name: acquire(name, spec) for name, spec in DATASETS.items()}
    print("acquisition status:", status)
    return 0 if all(v == "ok" for v in status.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
