r"""
BHI 2026 REVISION — CROSS-LABEL DUPLICATE AUDIT
================================================

Project:
    D:\Thyroid-BHI-26

Purpose
-------
Audit ultrasound images that share an MD5 / pHash / leakage-group signature
across opposite diagnostic labels.

This script is diagnostic only:
- no training
- no relabelling
- no deletion
- no modification of source images

It verifies exact duplicate conflicts using:
1. manifest MD5
2. recomputed MD5
3. recomputed SHA256
4. decoded pixel equality when possible

It separately reports pHash-only conflicts.

It also creates contact-sheet PNGs for manual review.

Outputs
-------
D:\Thyroid-BHI-26\revision_cross_label_duplicate_audit\

    01_exact_md5_conflict_members.csv
    02_exact_md5_conflict_summary.csv
    03_phash_only_conflict_members.csv
    04_phash_only_conflict_summary.csv
    05_all_cross_label_conflict_members.csv
    exact_md5_contact_sheets\
    phash_only_contact_sheets\
    06_audit_report.txt

Run
---
C:\Users\admin\miniconda3\envs\nnunet\python.exe ^
  "D:\Thyroid-BHI-26\Rivision scripts\00c_audit_cross_label_duplicates.py"
"""

from __future__ import annotations

import hashlib
import math
import re
from pathlib import Path

import numpy as np
import pandas as pd

try:
    from PIL import Image, ImageOps, ImageDraw
except ImportError as e:
    raise RuntimeError(
        "Pillow is required. Install with: pip install pillow"
    ) from e


ROOT = Path(r"D:\Thyroid-BHI-26").resolve()
MANIFEST = ROOT / "data" / "metadata_unpaired_leakage_safe.csv"
OUT = ROOT / "revision_cross_label_duplicate_audit"

OUT.mkdir(parents=True, exist_ok=True)

EXACT_DIR = OUT / "exact_md5_contact_sheets"
PHASH_DIR = OUT / "phash_only_contact_sheets"

EXACT_DIR.mkdir(parents=True, exist_ok=True)
PHASH_DIR.mkdir(parents=True, exist_ok=True)


def read_csv_safe(path):
    try:
        return pd.read_csv(path, low_memory=False)
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="cp1252", low_memory=False)


def md5_file(path, block=1024 * 1024):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(block), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_file(path, block=1024 * 1024):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(block), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize_label(x):
    if pd.isna(x):
        return np.nan
    s = str(x).strip().lower()
    if s in {"0", "0.0", "benign", "negative"}:
        return 0
    if s in {
        "1", "1.0", "ptc", "malignant", "positive",
        "papillary", "papillary thyroid carcinoma"
    }:
        return 1
    try:
        v = int(float(s))
        return v if v in (0, 1) else np.nan
    except Exception:
        return np.nan


def basename(x):
    if pd.isna(x):
        return ""
    return str(x).replace("\\", "/").rsplit("/", 1)[-1]


def cyto_group(filename):
    stem = Path(basename(filename)).stem
    m = re.match(r"^\s*(\d+)[_-](\d+)", stem)
    return int(m.group(1)) if m else np.nan


def us_group(filename):
    stem = Path(basename(filename)).stem.strip()
    if stem.isdigit():
        return int(stem)
    hits = re.findall(r"\d+", stem)
    return int(hits[0]) if len(hits) == 1 else np.nan


def derive_source_group(df):
    out = df.copy()

    if "filename" not in out.columns:
        out["filename"] = out["image_path"].map(basename)

    out["_label"] = out["label"].map(normalize_label)
    mod = out["modality"].astype(str).str.lower().str.strip()

    out["_source_num"] = np.nan

    cmask = mod.eq("cytology")
    umask = mod.eq("ultrasound")

    out.loc[cmask, "_source_num"] = (
        out.loc[cmask, "filename"].map(cyto_group)
    )

    out.loc[umask, "_source_num"] = (
        out.loc[umask, "filename"].map(us_group)
    )

    if out["_source_num"].isna().any():
        raise RuntimeError(
            f"Could not derive source group for "
            f"{int(out['_source_num'].isna().sum())} rows."
        )

    out["_source_num"] = out["_source_num"].astype(int)

    out["source_group"] = (
        mod
        + "::label"
        + out["_label"].astype(int).astype(str)
        + "::group"
        + out["_source_num"].astype(str)
    )

    return out


def clean_sig(s):
    return (
        s.astype(str)
        .str.strip()
        .replace({
            "": np.nan,
            "nan": np.nan,
            "None": np.nan,
            "<NA>": np.nan,
        })
    )


def decode_image(path):
    with Image.open(path) as im:
        return np.array(im.convert("RGB"))


def pixel_equal(path_a, path_b):
    try:
        a = decode_image(path_a)
        b = decode_image(path_b)

        if a.shape != b.shape:
            return False

        return bool(np.array_equal(a, b))
    except Exception:
        return np.nan


def phash_hamming(hex_a, hex_b):
    try:
        a = int(str(hex_a), 16)
        b = int(str(hex_b), 16)
        return int((a ^ b).bit_count())
    except Exception:
        return np.nan


def sanitize(text):
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", str(text))[:120]


def contact_sheet(group_df, outfile, title):
    thumb_w = 360
    thumb_h = 300
    text_h = 105
    margin = 16

    n = len(group_df)
    cols = min(3, max(1, n))
    rows = math.ceil(n / cols)

    canvas_w = cols * (thumb_w + margin) + margin
    canvas_h = 55 + rows * (thumb_h + text_h + margin) + margin

    canvas = Image.new("RGB", (canvas_w, canvas_h), "white")
    draw = ImageDraw.Draw(canvas)

    draw.text((margin, 16), title, fill="black")

    for idx, (_, row) in enumerate(group_df.reset_index(drop=True).iterrows()):
        r = idx // cols
        c = idx % cols

        x = margin + c * (thumb_w + margin)
        y = 50 + margin + r * (thumb_h + text_h + margin)

        path = Path(str(row["image_path"]))

        try:
            with Image.open(path) as im:
                im = im.convert("RGB")
                fitted = ImageOps.contain(im, (thumb_w, thumb_h))
                bg = Image.new("RGB", (thumb_w, thumb_h), "white")
                xx = (thumb_w - fitted.width) // 2
                yy = (thumb_h - fitted.height) // 2
                bg.paste(fitted, (xx, yy))
        except Exception:
            bg = Image.new("RGB", (thumb_w, thumb_h), "white")
            d2 = ImageDraw.Draw(bg)
            d2.text((10, 10), "IMAGE LOAD FAILED", fill="black")

        canvas.paste(bg, (x, y))

        text = (
            f"label={row.get('_label','')}  group={row.get('source_group','')}\n"
            f"{row.get('filename','')}\n"
            f"MD5={str(row.get('md5',''))[:18]}...\n"
            f"pHash={row.get('phash','')}"
        )

        draw.multiline_text(
            (x, y + thumb_h + 5),
            text,
            fill="black",
            spacing=3,
        )

    canvas.save(outfile)


if not MANIFEST.exists():
    raise FileNotFoundError(MANIFEST)

df = derive_source_group(read_csv_safe(MANIFEST))

# Focus on ultrasound first because that is where current cross-label conflicts appeared.
us = df[
    df["modality"].astype(str).str.lower().eq("ultrasound")
].copy()

for col in ["md5", "phash", "leakage_group"]:
    if col not in us.columns:
        us[col] = np.nan
    us[col] = clean_sig(us[col])


# ---------------------------------------------------------------------------
# 1. Exact-MD5 cross-label groups
# ---------------------------------------------------------------------------

md5_label_counts = (
    us.dropna(subset=["md5"])
    .groupby("md5")["_label"]
    .nunique()
)

cross_md5 = set(
    md5_label_counts[md5_label_counts > 1].index
)

exact_members = us[
    us["md5"].isin(cross_md5)
].copy()

verify_rows = []

for md5sig, g in exact_members.groupby("md5", sort=True):
    reference_path = Path(str(g.iloc[0]["image_path"]))

    ref_sha = None
    ref_md5 = None

    if reference_path.exists():
        ref_md5 = md5_file(reference_path)
        ref_sha = sha256_file(reference_path)

    for _, row in g.iterrows():
        path = Path(str(row["image_path"]))

        exists = path.exists()
        actual_md5 = md5_file(path) if exists else ""
        actual_sha = sha256_file(path) if exists else ""

        verify_rows.append({
            "conflict_type": "exact_md5_cross_label",
            "signature": md5sig,
            "label": int(row["_label"]),
            "source_group": row["source_group"],
            "filename": row["filename"],
            "image_path": row["image_path"],
            "file_exists": exists,
            "manifest_md5": row["md5"],
            "recomputed_md5": actual_md5,
            "recomputed_sha256": actual_sha,
            "same_md5_as_reference": (
                bool(actual_md5 == ref_md5)
                if exists and ref_md5 else False
            ),
            "same_sha256_as_reference": (
                bool(actual_sha == ref_sha)
                if exists and ref_sha else False
            ),
            "pixel_equal_to_reference": (
                pixel_equal(reference_path, path)
                if exists and reference_path.exists()
                else np.nan
            ),
            "phash": row.get("phash", np.nan),
            "leakage_group": row.get("leakage_group", np.nan),
        })

exact_verified = pd.DataFrame(verify_rows)

exact_verified.to_csv(
    OUT / "01_exact_md5_conflict_members.csv",
    index=False,
)

exact_summary_rows = []

for sig, g in exact_verified.groupby("signature", sort=True):
    exact_summary_rows.append({
        "md5": sig,
        "n_rows": len(g),
        "labels": ";".join(map(str, sorted(g["label"].unique()))),
        "source_groups": ";".join(sorted(g["source_group"].unique())),
        "filenames": ";".join(map(str, g["filename"])),
        "all_recomputed_md5_same": bool(g["same_md5_as_reference"].all()),
        "all_sha256_same": bool(g["same_sha256_as_reference"].all()),
        "all_pixels_equal": bool(
            g["pixel_equal_to_reference"].dropna().astype(bool).all()
        ) if g["pixel_equal_to_reference"].notna().any() else np.nan,
    })

exact_summary = pd.DataFrame(exact_summary_rows)

exact_summary.to_csv(
    OUT / "02_exact_md5_conflict_summary.csv",
    index=False,
)


# Contact sheets for exact conflicts
for sig, g in exact_members.groupby("md5", sort=True):
    outfile = EXACT_DIR / f"md5_{sanitize(sig)}.png"

    contact_sheet(
        g,
        outfile,
        title=f"Cross-label exact MD5 conflict: {sig}",
    )


# ---------------------------------------------------------------------------
# 2. pHash-only cross-label conflicts
#    Exclude any members already part of exact-MD5 cross-label groups.
# ---------------------------------------------------------------------------

phash_label_counts = (
    us.dropna(subset=["phash"])
    .groupby("phash")["_label"]
    .nunique()
)

cross_phash = set(
    phash_label_counts[phash_label_counts > 1].index
)

phash_members_all = us[
    us["phash"].isin(cross_phash)
].copy()

# Keep only pHash conflicts whose members are not all already explained by a
# cross-label exact-MD5 conflict.
phash_only_groups = []

for phash_sig, g in phash_members_all.groupby("phash", sort=True):
    if g["md5"].notna().any() and set(g["md5"].dropna()).intersection(cross_md5):
        # Still include if some pair has different MD5 values; this is useful
        # for checking additional near-duplicate relations.
        if g["md5"].nunique(dropna=True) <= 1:
            continue

    phash_only_groups.append(g)

if phash_only_groups:
    phash_only = pd.concat(phash_only_groups, ignore_index=True)
else:
    phash_only = pd.DataFrame(columns=us.columns)

phash_rows = []

for phash_sig, g in phash_only.groupby("phash", sort=True):
    # pairwise reference distances
    ref_hash = g.iloc[0]["phash"]

    for _, row in g.iterrows():
        path = Path(str(row["image_path"]))

        phash_rows.append({
            "conflict_type": "phash_only_cross_label",
            "signature": phash_sig,
            "label": int(row["_label"]),
            "source_group": row["source_group"],
            "filename": row["filename"],
            "image_path": row["image_path"],
            "file_exists": path.exists(),
            "md5": row.get("md5", np.nan),
            "phash": row.get("phash", np.nan),
            "phash_hamming_to_reference": phash_hamming(
                row.get("phash", ""),
                ref_hash,
            ),
            "leakage_group": row.get("leakage_group", np.nan),
        })

phash_members = pd.DataFrame(phash_rows)

phash_members.to_csv(
    OUT / "03_phash_only_conflict_members.csv",
    index=False,
)

phash_summary_rows = []

if not phash_members.empty:
    for sig, g in phash_members.groupby("signature", sort=True):
        phash_summary_rows.append({
            "phash": sig,
            "n_rows": len(g),
            "labels": ";".join(map(str, sorted(g["label"].unique()))),
            "source_groups": ";".join(sorted(g["source_group"].unique())),
            "filenames": ";".join(map(str, g["filename"])),
            "unique_md5_count": int(g["md5"].nunique(dropna=True)),
        })

phash_summary = pd.DataFrame(phash_summary_rows)

phash_summary.to_csv(
    OUT / "04_phash_only_conflict_summary.csv",
    index=False,
)


for sig, g in phash_only.groupby("phash", sort=True):
    outfile = PHASH_DIR / f"phash_{sanitize(sig)}.png"

    contact_sheet(
        g,
        outfile,
        title=f"Cross-label pHash-only conflict: {sig}",
    )


# ---------------------------------------------------------------------------
# 3. Combined member table
# ---------------------------------------------------------------------------

combined_parts = []

if not exact_verified.empty:
    a = exact_verified.copy()
    combined_parts.append(a)

if not phash_members.empty:
    b = phash_members.copy()
    combined_parts.append(b)

if combined_parts:
    combined = pd.concat(
        combined_parts,
        ignore_index=True,
        sort=False,
    )
else:
    combined = pd.DataFrame()

combined.to_csv(
    OUT / "05_all_cross_label_conflict_members.csv",
    index=False,
)


# ---------------------------------------------------------------------------
# 4. Report
# ---------------------------------------------------------------------------

exact_groups = len(exact_summary)
exact_rows = len(exact_verified)

phash_groups = len(phash_summary)
phash_rows_n = len(phash_members)

all_exact_verified = (
    not exact_summary.empty
    and exact_summary["all_sha256_same"].astype(bool).all()
    and exact_summary["all_recomputed_md5_same"].astype(bool).all()
)

report_lines = [
    "BHI 2026 — cross-label duplicate audit",
    "=" * 72,
    "",
    f"Ultrasound rows examined: {len(us)}",
    f"Cross-label exact-MD5 groups: {exact_groups}",
    f"Rows involved in exact-MD5 conflicts: {exact_rows}",
    f"Cross-label pHash-only groups: {phash_groups}",
    f"Rows involved in pHash-only conflicts: {phash_rows_n}",
    "",
    f"All exact-MD5 conflicts verified by recomputed SHA256: {all_exact_verified}",
    "",
    "Interpretation:",
    "  Exact MD5 + SHA256 identity across opposite labels is a definitive",
    "  source-label contradiction. These observations should not be",
    "  arbitrarily relabelled. A conservative benchmark should exclude the",
    "  entire conflicting exact-duplicate component from training, validation,",
    "  and testing.",
    "",
    "  pHash-only conflicts are not automatically definitive duplicates.",
    "  Review the generated contact sheets before deciding whether to exclude",
    "  those components.",
]

(OUT / "06_audit_report.txt").write_text(
    "\n".join(report_lines),
    encoding="utf-8",
)


# ---------------------------------------------------------------------------
# Console summary
# ---------------------------------------------------------------------------

print("=" * 96)
print("BHI REVISION — CROSS-LABEL DUPLICATE AUDIT")
print("=" * 96)

print("\n[EXACT MD5 CROSS-LABEL CONFLICTS]")
if exact_summary.empty:
    print("none")
else:
    print(exact_summary.to_string(index=False))

print("\n[pHash-ONLY CROSS-LABEL CONFLICTS]")
if phash_summary.empty:
    print("none")
else:
    print(phash_summary.to_string(index=False))

print("\n" + "=" * 96)
print("COPY/PASTE THIS BLOCK")
print("=" * 96)

print(f"Ultrasound rows examined                : {len(us)}")
print(f"Cross-label exact-MD5 groups            : {exact_groups}")
print(f"Rows in exact-MD5 conflicts             : {exact_rows}")
print(f"All exact groups SHA256-confirmed        : {all_exact_verified}")
print(f"Cross-label pHash-only groups           : {phash_groups}")
print(f"Rows in pHash-only conflicts            : {phash_rows_n}")

if not exact_summary.empty:
    print("\nExact conflict source groups:")
    for _, r in exact_summary.iterrows():
        print(
            f"{r['md5']} | rows={r['n_rows']} | "
            f"{r['source_groups']} | "
            f"sha256_same={r['all_sha256_same']} | "
            f"pixels_equal={r['all_pixels_equal']}"
        )

if not phash_summary.empty:
    print("\npHash-only conflict source groups:")
    for _, r in phash_summary.iterrows():
        print(
            f"{r['phash']} | rows={r['n_rows']} | "
            f"{r['source_groups']} | "
            f"unique_md5={r['unique_md5_count']}"
        )

print("\nContact sheets:")
print("  exact :", EXACT_DIR)
print("  pHash :", PHASH_DIR)

print("\nReport:")
print(" ", OUT / "06_audit_report.txt")

print(
    "\nDo not create the final frozen split until these conflicts are reviewed."
)
