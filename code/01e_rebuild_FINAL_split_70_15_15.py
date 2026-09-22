r"""
BHI 2026 REVISION — FINAL 70/15/15 GROUP-SAFE FROZEN SPLIT
==========================================================

Project root
------------
D:\Thyroid-BHI-26

This script corrects the allocation proportions from the previous frozen split.

It keeps the SAME conservative cleaning policy:
- filename-derived modality-specific source groups;
- exclude both sides of cross-label MD5 / identical-pHash / leakage-group conflicts;
- no relabelling;
- same-label duplicate-linked source groups are merged into connected components.

The ONLY major change is how connected components are assigned:
    70% train
    15% validation
    15% test

Assignment is performed with a two-stage stratified split on connected
components, separately for cytology and ultrasound.

Because components are indivisible and occasionally contain >1 source group,
fractions may not be mathematically exact, but source-group/component
proportions should be close to 70/15/15.

The script FAILS if:
- any cross-label conflict remains;
- any source group / component / MD5 / pHash / leakage group crosses splits;
- component/source-group split proportions deviate too far from target.

Output
------
D:\Thyroid-BHI-26\revision_final_frozen_70_15_15\

    01_excluded_cross_label_conflicts.csv
    02_exclusion_summary.csv
    03_component_table.csv
    04_frozen_manifest.csv
    05_frozen_manifest_cytology.csv
    06_frozen_manifest_ultrasound.csv
    07_split_summary.csv
    08_split_fraction_audit.csv
    09_integrity_checks.csv
    10_integrity_report.txt
    11_manifest_sha256.txt

Run
---
C:\Users\admin\miniconda3\envs\nnunet\python.exe ^
  "D:\Thyroid-BHI-26\Rivision scripts\01e_rebuild_FINAL_split_70_15_15.py"
"""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


ROOT = Path(r"D:\Thyroid-BHI-26").resolve()
DEFAULT_MANIFEST = ROOT / "data" / "metadata_unpaired_leakage_safe.csv"
DEFAULT_OUT = ROOT / "revision_final_frozen_70_15_15"

SEED = 2026

TARGET = {
    "train": 0.70,
    "val": 0.15,
    "test": 0.15,
}

# Accept small deviations caused by indivisible duplicate-connected components.
MAX_SOURCE_GROUP_DEVIATION = 0.025   # 2.5 percentage points
MAX_COMPONENT_DEVIATION = 0.025      # 2.5 percentage points
MAX_IMAGE_DEVIATION = 0.060          # 6 percentage points


# =============================================================================
# HELPERS
# =============================================================================

def read_csv_safe(path):
    try:
        return pd.read_csv(path, low_memory=False)
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="cp1252", low_memory=False)


def basename(x):
    if pd.isna(x):
        return ""
    return str(x).replace("\\", "/").rsplit("/", 1)[-1]


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


def sha256_file(path):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)

    return h.hexdigest()


class UnionFind:

    def __init__(self):
        self.parent = {}
        self.rank = {}

    def add(self, x):
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0

    def find(self, x):
        self.add(x)

        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])

        return self.parent[x]

    def union(self, a, b):
        ra = self.find(a)
        rb = self.find(b)

        if ra == rb:
            return

        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra

        self.parent[rb] = ra

        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1


# =============================================================================
# SOURCE GROUPS
# =============================================================================

def derive_source_groups(df):

    out = df.copy()

    if "filename" not in out.columns:
        out["filename"] = out["image_path"].map(basename)

    out["_label"] = out["label"].map(normalize_label)

    if out["_label"].isna().any():
        raise RuntimeError(
            f"Unrecognized labels in {int(out['_label'].isna().sum())} rows."
        )

    mod = out["modality"].astype(str).str.lower().str.strip()

    out["_source_num"] = np.nan

    cyto = mod.eq("cytology")
    us = mod.eq("ultrasound")

    out.loc[cyto, "_source_num"] = (
        out.loc[cyto, "filename"].map(cyto_group)
    )

    out.loc[us, "_source_num"] = (
        out.loc[us, "filename"].map(us_group)
    )

    if out["_source_num"].isna().any():
        bad = out[out["_source_num"].isna()][
            ["image_path", "filename", "modality", "label"]
        ]
        print(bad.head(40).to_string(index=False))
        raise RuntimeError(
            f"Unable to derive source group for {len(bad)} rows."
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


# =============================================================================
# CROSS-LABEL EXCLUSIONS
# =============================================================================

def cross_label_values(df, sig_col):

    if sig_col not in df.columns:
        return set()

    tmp = df[[sig_col, "_label"]].copy()
    tmp[sig_col] = clean_sig(tmp[sig_col])
    tmp = tmp.dropna(subset=[sig_col])

    if tmp.empty:
        return set()

    n = tmp.groupby(sig_col)["_label"].nunique()

    return set(n[n > 1].index)


def mark_exclusions(df):

    out = df.copy()

    out["exclude_cross_label_conflict"] = False
    out["exclusion_reason"] = ""

    reasons = {
        idx: []
        for idx in out.index
    }

    for _, mdf in out.groupby(
        out["modality"].astype(str).str.lower(),
        sort=True,
    ):

        for sig_col, reason in [
            ("md5", "cross_label_exact_md5"),
            ("phash", "cross_label_identical_phash"),
            ("leakage_group", "cross_label_leakage_group"),
        ]:

            if sig_col not in mdf.columns:
                continue

            bad_values = cross_label_values(mdf, sig_col)

            if not bad_values:
                continue

            cleaned = clean_sig(mdf[sig_col])

            for idx in mdf.index[cleaned.isin(bad_values)]:
                reasons[idx].append(reason)

    for idx, rr in reasons.items():

        if rr:
            out.at[idx, "exclude_cross_label_conflict"] = True
            out.at[idx, "exclusion_reason"] = ";".join(sorted(set(rr)))

    return out


def cross_label_conflict_count(df, sig_col):

    if sig_col not in df.columns:
        return 0

    return len(cross_label_values(df, sig_col))


# =============================================================================
# CONNECTED COMPONENTS
# =============================================================================

def build_components(df_mod):

    uf = UnionFind()

    groups = sorted(df_mod["source_group"].unique())

    for g in groups:
        uf.add(g)

    for sig_col in [
        c for c in ("md5", "phash", "leakage_group")
        if c in df_mod.columns
    ]:

        tmp = df_mod[
            ["source_group", "_label", sig_col]
        ].copy()

        tmp[sig_col] = clean_sig(tmp[sig_col])
        tmp = tmp.dropna(subset=[sig_col])

        for sig, part in tmp.groupby(sig_col, sort=False):

            labels = sorted(part["_label"].astype(int).unique())

            if len(labels) > 1:
                raise RuntimeError(
                    f"Cross-label {sig_col} remained after cleaning: {sig}"
                )

            src_groups = sorted(part["source_group"].unique())

            if len(src_groups) > 1:

                first = src_groups[0]

                for other in src_groups[1:]:
                    uf.union(first, other)

    root_to_id = {}
    group_to_component = {}
    next_id = 1

    for group in groups:

        root = uf.find(group)

        if root not in root_to_id:
            root_to_id[root] = next_id
            next_id += 1

        group_to_component[group] = root_to_id[root]

    work = df_mod.copy()

    work["component_id"] = (
        work["source_group"]
        .map(group_to_component)
        .astype(int)
    )

    rows = []

    for cid, part in work.groupby("component_id", sort=True):

        labels = sorted(part["_label"].astype(int).unique())

        if len(labels) != 1:
            raise RuntimeError(
                f"Component {cid} has mixed labels {labels}"
            )

        rows.append({
            "component_id": int(cid),
            "modality": str(part["modality"].iloc[0]).lower(),
            "label": int(labels[0]),
            "n_images": int(len(part)),
            "n_source_groups": int(part["source_group"].nunique()),
            "source_groups": ";".join(
                sorted(part["source_group"].unique())
            ),
        })

    return pd.DataFrame(rows)


# =============================================================================
# 70 / 15 / 15 COMPONENT SPLIT
# =============================================================================

def stratified_70_15_15(comp, seed):

    # Stage 1: 70% train, 30% temporary.
    train, temp = train_test_split(
        comp,
        test_size=0.30,
        random_state=seed,
        stratify=comp["label"],
    )

    # Stage 2: split the temporary 30% equally into 15% val and 15% test.
    val, test = train_test_split(
        temp,
        test_size=0.50,
        random_state=seed + 1,
        stratify=temp["label"],
    )

    train = train.copy()
    val = val.copy()
    test = test.copy()

    train["split"] = "train"
    val["split"] = "val"
    test["split"] = "test"

    out = pd.concat(
        [train, val, test],
        ignore_index=True,
    )

    return out


# =============================================================================
# INTEGRITY / FRACTION AUDIT
# =============================================================================

def crossing_count(df, group_col):

    n = df.groupby(group_col)["split"].nunique()

    return int((n > 1).sum())


def signature_crossing(df, sig_col):

    if sig_col not in df.columns:
        return 0

    tmp = df[[sig_col, "split"]].copy()
    tmp[sig_col] = clean_sig(tmp[sig_col])
    tmp = tmp.dropna(subset=[sig_col])

    if tmp.empty:
        return 0

    n = tmp.groupby(sig_col)["split"].nunique()

    return int((n > 1).sum())


def make_fraction_audit(df, component_table):

    rows = []

    for modality, mdf in df.groupby(
        df["modality"].astype(str).str.lower(),
        sort=True,
    ):

        total_images = len(mdf)
        total_groups = mdf["source_group"].nunique()
        total_components = mdf["component_id"].nunique()

        for split_name in ("train", "val", "test"):

            s = mdf[mdf["split"].eq(split_name)]

            image_frac = len(s) / total_images
            group_frac = s["source_group"].nunique() / total_groups
            comp_frac = s["component_id"].nunique() / total_components

            rows.append({
                "modality": modality,
                "split": split_name,
                "target_fraction": TARGET[split_name],
                "images": len(s),
                "image_fraction": image_frac,
                "image_abs_deviation": abs(image_frac - TARGET[split_name]),
                "source_groups": s["source_group"].nunique(),
                "source_group_fraction": group_frac,
                "source_group_abs_deviation": abs(group_frac - TARGET[split_name]),
                "components": s["component_id"].nunique(),
                "component_fraction": comp_frac,
                "component_abs_deviation": abs(comp_frac - TARGET[split_name]),
            })

    return pd.DataFrame(rows)


# =============================================================================
# MAIN
# =============================================================================

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--manifest",
        type=Path,
        default=DEFAULT_MANIFEST,
    )

    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT,
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=SEED,
    )

    args = parser.parse_args()

    manifest = args.manifest.resolve()
    outdir = args.out.resolve()

    outdir.mkdir(parents=True, exist_ok=True)

    df = derive_source_groups(
        read_csv_safe(manifest)
    )

    print("=" * 96)
    print("BHI 2026 REVISION — FINAL 70/15/15 GROUP-SAFE SPLIT")
    print("=" * 96)
    print("Input :", manifest)
    print("Output:", outdir)
    print("Rows  :", len(df))
    print("Seed  :", args.seed)

    # ------------------------------------------------------------------
    # Clean cross-label duplicate conflicts
    # ------------------------------------------------------------------

    marked = mark_exclusions(df)

    excluded = marked[
        marked["exclude_cross_label_conflict"]
    ].copy()

    clean = marked[
        ~marked["exclude_cross_label_conflict"]
    ].copy()

    excluded.to_csv(
        outdir / "01_excluded_cross_label_conflicts.csv",
        index=False,
    )

    exclusion_summary = (
        excluded.groupby(
            ["modality", "_label", "exclusion_reason"],
            dropna=False,
        )
        .agg(
            rows=("image_path", "size"),
            source_groups=("source_group", "nunique"),
        )
        .reset_index()
        .rename(columns={"_label": "label"})
    )

    exclusion_summary.to_csv(
        outdir / "02_exclusion_summary.csv",
        index=False,
    )

    print("\n[EXCLUSIONS]")
    print(
        exclusion_summary.to_string(index=False)
        if not exclusion_summary.empty
        else "none"
    )

    print(f"\nExcluded rows: {len(excluded)}")
    print(f"Remaining rows: {len(clean)}")

    # Expected result from independently verified audit.
    if len(excluded) != 23:
        raise RuntimeError(
            f"Expected 23 conservative cross-label exclusions, "
            f"but found {len(excluded)}. Stop and investigate."
        )

    # Zero conflict check after cleaning.
    for modality, mdf in clean.groupby(
        clean["modality"].astype(str).str.lower(),
        sort=True,
    ):

        for sig in ("md5", "phash", "leakage_group"):

            n = cross_label_conflict_count(mdf, sig)

            if n:
                raise RuntimeError(
                    f"{modality}: {n} cross-label {sig} conflicts remain."
                )

    # ------------------------------------------------------------------
    # Build components and perform stratified 70/15/15 split
    # ------------------------------------------------------------------

    assigned_components = []

    for modality, mdf in clean.groupby(
        clean["modality"].astype(str).str.lower(),
        sort=True,
    ):

        comp = build_components(mdf)

        print(f"\n[{modality.upper()} COMPONENTS BEFORE SPLIT]")
        print(
            comp.groupby("label")
            .agg(
                components=("component_id", "size"),
                source_groups=("n_source_groups", "sum"),
                images=("n_images", "sum"),
            )
            .to_string()
        )

        assigned = stratified_70_15_15(
            comp,
            seed=args.seed,
        )

        assigned_components.append(assigned)

        print(f"\n[{modality.upper()} COMPONENT ALLOCATION]")
        print(
            assigned.groupby(["split", "label"])
            .agg(
                components=("component_id", "size"),
                source_groups=("n_source_groups", "sum"),
                images=("n_images", "sum"),
            )
            .to_string()
        )

    component_table = pd.concat(
        assigned_components,
        ignore_index=True,
    )

    component_table.to_csv(
        outdir / "03_component_table.csv",
        index=False,
    )

    # ------------------------------------------------------------------
    # Map component assignment back to rows
    # ------------------------------------------------------------------

    lookup = {}

    for _, row in component_table.iterrows():

        modality = str(row["modality"]).lower()

        for source_group in str(row["source_groups"]).split(";"):
            lookup[(modality, source_group)] = (
                int(row["component_id"]),
                str(row["split"]),
            )

    component_ids = []
    splits = []

    for _, row in clean.iterrows():

        key = (
            str(row["modality"]).lower(),
            str(row["source_group"]),
        )

        if key not in lookup:
            raise RuntimeError(
                f"Missing component assignment for {key}"
            )

        cid, split = lookup[key]

        component_ids.append(cid)
        splits.append(split)

    clean["component_id"] = component_ids
    clean["original_split"] = clean["split"]
    clean["split"] = splits

    # ------------------------------------------------------------------
    # Integrity
    # ------------------------------------------------------------------

    integrity_rows = []

    for modality, mdf in clean.groupby(
        clean["modality"].astype(str).str.lower(),
        sort=True,
    ):

        integrity_rows.append({
            "modality": modality,
            "source_group_crossing": crossing_count(mdf, "source_group"),
            "component_crossing": crossing_count(mdf, "component_id"),
            "md5_crossing": signature_crossing(mdf, "md5"),
            "phash_crossing": signature_crossing(mdf, "phash"),
            "leakage_group_crossing": signature_crossing(mdf, "leakage_group"),
            "cross_label_md5": cross_label_conflict_count(mdf, "md5"),
            "cross_label_phash": cross_label_conflict_count(mdf, "phash"),
            "cross_label_leakage_group": cross_label_conflict_count(
                mdf, "leakage_group"
            ),
        })

    integrity = pd.DataFrame(integrity_rows)

    print("\n[INTEGRITY]")
    print(integrity.to_string(index=False))

    numeric = [c for c in integrity.columns if c != "modality"]

    if integrity[numeric].fillna(0).astype(int).to_numpy().sum() != 0:
        raise RuntimeError(
            "Non-zero leakage/conflict count in final integrity audit."
        )

    # ------------------------------------------------------------------
    # Split summary + fraction audit
    # ------------------------------------------------------------------

    summary = (
        clean.groupby(["modality", "split", "_label"])
        .agg(
            images=("image_path", "size"),
            source_groups=("source_group", "nunique"),
            components=("component_id", "nunique"),
        )
        .reset_index()
        .rename(columns={"_label": "label"})
    )

    fraction_audit = make_fraction_audit(
        clean,
        component_table,
    )

    print("\n[SPLIT SUMMARY]")
    print(summary.to_string(index=False))

    print("\n[SPLIT FRACTION AUDIT]")
    display_cols = [
        "modality",
        "split",
        "target_fraction",
        "image_fraction",
        "source_group_fraction",
        "component_fraction",
    ]

    print(
        fraction_audit[display_cols]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}")
    )

    # Fail if the group/component allocation is materially off target.
    bad_groups = fraction_audit[
        fraction_audit["source_group_abs_deviation"]
        > MAX_SOURCE_GROUP_DEVIATION
    ]

    bad_components = fraction_audit[
        fraction_audit["component_abs_deviation"]
        > MAX_COMPONENT_DEVIATION
    ]

    bad_images = fraction_audit[
        fraction_audit["image_abs_deviation"]
        > MAX_IMAGE_DEVIATION
    ]

    if len(bad_groups):
        raise RuntimeError(
            "Source-group fractions deviate too far from 70/15/15:\n"
            + bad_groups.to_string(index=False)
        )

    if len(bad_components):
        raise RuntimeError(
            "Component fractions deviate too far from 70/15/15:\n"
            + bad_components.to_string(index=False)
        )

    if len(bad_images):
        raise RuntimeError(
            "Image fractions deviate too far from target:\n"
            + bad_images.to_string(index=False)
        )

    # ------------------------------------------------------------------
    # Save frozen manifest
    # ------------------------------------------------------------------

    frozen = clean[
        [c for c in clean.columns if not c.startswith("_")]
    ].copy()

    frozen_path = outdir / "04_frozen_manifest.csv"

    frozen.to_csv(
        frozen_path,
        index=False,
    )

    for modality, filename in [
        ("cytology", "05_frozen_manifest_cytology.csv"),
        ("ultrasound", "06_frozen_manifest_ultrasound.csv"),
    ]:

        frozen[
            frozen["modality"].astype(str).str.lower().eq(modality)
        ].to_csv(
            outdir / filename,
            index=False,
        )

    summary.to_csv(
        outdir / "07_split_summary.csv",
        index=False,
    )

    fraction_audit.to_csv(
        outdir / "08_split_fraction_audit.csv",
        index=False,
    )

    integrity.to_csv(
        outdir / "09_integrity_checks.csv",
        index=False,
    )

    digest = sha256_file(frozen_path)

    (outdir / "11_manifest_sha256.txt").write_text(
        digest + "\n",
        encoding="utf-8",
    )

    report = [
        "BHI 2026 revision — final 70/15/15 group-safe split",
        "=" * 72,
        "",
        f"Original rows: {len(df)}",
        f"Excluded cross-label duplicate/near-duplicate rows: {len(excluded)}",
        f"Final rows: {len(frozen)}",
        "",
        "Integrity:",
        integrity.to_string(index=False),
        "",
        "Split summary:",
        summary.to_string(index=False),
        "",
        "Split fractions:",
        fraction_audit[display_cols].to_string(index=False),
        "",
        f"Frozen manifest: {frozen_path}",
        f"SHA256: {digest}",
    ]

    (outdir / "10_integrity_report.txt").write_text(
        "\n".join(report),
        encoding="utf-8",
    )

    print("\n" + "=" * 96)
    print("COPY/PASTE THIS BLOCK")
    print("=" * 96)

    print(f"Original rows : {len(df)}")
    print(f"Excluded rows : {len(excluded)}")
    print(f"Final rows    : {len(frozen)}")

    print("\n[INTEGRITY]")
    print(integrity.to_string(index=False))

    print("\n[SPLIT SUMMARY]")
    print(summary.to_string(index=False))

    print("\n[SPLIT FRACTIONS]")
    print(
        fraction_audit[display_cols]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}")
    )

    print("\n[FROZEN MANIFEST]")
    print(frozen_path)
    print("SHA256:", digest)

    print(
        "\nSUCCESS — this 70/15/15 manifest is ready for GPU retraining."
    )


if __name__ == "__main__":
    main()
