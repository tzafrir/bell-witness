"""Acquire the Delft open datasets into data/raw/ and verify checksums.
Idempotent. See data/SOURCES.md for provenance; URLs verified 2026-06-10."""
import hashlib
import io
import sys
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
}


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    ok = True
    for name, spec in DATASETS.items():
        zpath = RAW / spec["zip_name"]
        if not zpath.exists():
            print(f"[{name}] downloading {spec['url']}")
            urllib.request.urlretrieve(spec["url"], zpath)
        md5 = hashlib.md5(zpath.read_bytes()).hexdigest()
        match = md5 == spec["md5"]
        ok &= match
        print(f"[{name}] md5 {md5} {'OK' if match else 'MISMATCH (expected %s)' % spec['md5']}")
        dest = RAW / name
        if match and not dest.exists():
            with zipfile.ZipFile(zpath) as z:
                z.extractall(dest)
            print(f"[{name}] extracted to {dest}")
    if not ok:
        print("\nChecksum mismatch: delete the bad zip and re-run, or download "
              "manually from the URLs in data/SOURCES.md into data/raw/.")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
