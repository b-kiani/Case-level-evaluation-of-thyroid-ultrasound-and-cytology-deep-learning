"""
Write copies of the manifests and prediction files with the original machine's path prefix replaced.

    python tools/relocate_paths.py --old "D:\\Thyroid-BHI-26" --new "/data/thyroid" [--out relocated]

Originals are never modified (the frozen manifest's SHA-256 refers to the original file).
"""
import argparse, csv
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ap = argparse.ArgumentParser()
ap.add_argument("--old", required=True); ap.add_argument("--new", required=True); ap.add_argument("--out", default="relocated")
a = ap.parse_args()
out_root = REPO / a.out; n = 0
for f in list((REPO / "manifests").glob("*.csv")) + list((REPO / "predictions").rglob("*.csv")):
    with open(f, newline="", encoding="utf-8") as fh:
        rows = list(csv.reader(fh))
    fixed = [[c.replace(a.old, a.new).replace("\\", "/") if c.startswith(a.old) else c for c in r] for r in rows]
    dst = out_root / f.relative_to(REPO); dst.parent.mkdir(parents=True, exist_ok=True)
    with open(dst, "w", newline="", encoding="utf-8") as fh:
        csv.writer(fh).writerows(fixed)
    n += 1
print(f"wrote {n} relocated copies under {out_root}")
