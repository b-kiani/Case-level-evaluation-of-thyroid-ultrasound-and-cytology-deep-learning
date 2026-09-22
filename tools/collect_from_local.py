"""
Fill this repository with the files that exist only on the analysis machine.

Run once, from the repository folder, after the final Stage I rerun:

    python tools/collect_from_local.py --root "D:\\Thyroid-BHI-26"

Standard library only. It copies (never moves) and never touches the project folders' contents.
  1. split-design and masking-control out-of-fold predictions      -> predictions/imagelevel_cv, predictions/shortcut_cv
  2. inner-validation predictions used for CV ensemble thresholds    -> predictions/grouped_cv/inner_validation
  3. package list and GPU details                                   -> environment/, and exact pins in requirements.txt
  4. SHA-256 of every model checkpoint                              -> checkpoints/checkpoint_sha256.csv
  5. the latest result tables, RESULTS.md and Figure 8              -> results/
Optional:  --zip-checkpoints  writes the frozen-split checkpoints to one zip for Zenodo.
"""
import argparse, csv, datetime, hashlib, re, shutil, subprocess, sys, zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MODELS = ["convnext_small", "efficientnet_b3", "swin_tiny", "resnet50", "densenet121"]
PIN = ["torch", "torchvision", "timm", "numpy", "pandas", "scikit-learn", "scipy", "pillow", "matplotlib", "imagehash"]


def copy(src, dst, report):
    src, dst = Path(src), Path(dst)
    if src.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        report.append(f"copied   {dst.relative_to(REPO)}")
        return True
    report.append(f"MISSING  {src}")
    return False


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 22), b""):
            h.update(block)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help=r'project root, e.g. "D:\Thyroid-BHI-26"')
    ap.add_argument("--torch-python", default=r"C:\Users\admin\miniconda3\envs\nnunet\python.exe",
                    help="python of the training environment (used only if no pip freeze file exists)")
    ap.add_argument("--zip-checkpoints", action="store_true")
    a = ap.parse_args()
    root = Path(a.root); r2 = root / "revision_round2"; report = []
    if not r2.exists():
        sys.exit(f"{r2} not found")

    # 1. split-design and masking-control predictions
    for k in ["convnext_small", "efficientnet_b3"]:
        base = r2 / "imagelevel_cv" / "cytology" / k
        for f in ["oof_predictions.csv", "fold_metrics.csv", "cv_summary.json"]:
            copy(base / f, REPO / "predictions" / "imagelevel_cv" / f"cytology_{k}_{f}", report)
    for mode in ["surround_only", "center_only"]:
        base = r2 / "shortcut_cv" / mode / "ultrasound" / "efficientnet_b3"
        for f in ["oof_predictions.csv", "fold_metrics.csv", "cv_summary.json"]:
            copy(base / f, REPO / "predictions" / "shortcut_cv" / f"{mode}_efficientnet_b3_{f}", report)

    # 2. inner-validation predictions
    for f in sorted((r2 / "cv_innerval").rglob("*.csv")):
        copy(f, REPO / "predictions" / "grouped_cv" / "inner_validation" / f.relative_to(r2 / "cv_innerval"), report)

    # 3. environment
    env_dir = REPO / "environment"
    freeze = r2 / "release" / "environment" / "pip_freeze.txt"
    if freeze.exists():
        copy(freeze, env_dir / "pip_freeze.txt", report)
    else:
        try:
            out = subprocess.run([a.torch_python, "-m", "pip", "freeze"], capture_output=True, text=True, check=True).stdout
            (env_dir / "pip_freeze.txt").write_text(out, encoding="utf-8"); report.append("written  environment/pip_freeze.txt")
        except Exception as e:
            report.append(f"MISSING  pip freeze ({e})")
    copy(r2 / "release" / "environment" / "nvidia_smi.txt", env_dir / "nvidia_smi.txt", report)
    if (env_dir / "pip_freeze.txt").exists():
        frozen = {}
        for line in (env_dir / "pip_freeze.txt").read_text(encoding="utf-8", errors="ignore").splitlines():
            m = re.match(r"^([A-Za-z0-9_.\-]+)==([^\s;]+)", line.strip())
            if m: frozen[m.group(1).lower().replace("_", "-")] = m.group(2)
        lines = ["# Exact versions of the training environment (from environment/pip_freeze.txt).",
                 "# PyTorch wheels with CUDA 12.1: pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu121"]
        for p in PIN:
            v = frozen.get(p)
            lines.append(f"{p}=={v}" if v else f"{p}  # not found in pip freeze")
        (REPO / "requirements.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
        report.append("written  requirements.txt (exact pins)")

    # 4. checkpoint hashes
    rows = []
    candidates = [root / "revision_exp1b" / mo / k / "best_model.pt" for mo in ["cytology", "ultrasound"] for k in MODELS]
    candidates += sorted((root / "revision_exp2b_group_cv").rglob("best_model.pt"))
    candidates += sorted((r2 / "imagelevel_cv").rglob("best_model.pt")) + sorted((r2 / "shortcut_cv").rglob("best_model.pt"))
    for c in candidates:
        if c.exists():
            st = c.stat()
            rows.append(dict(checkpoint=str(c.relative_to(root)).replace("\\", "/"), bytes=st.st_size,
                             modified=datetime.datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M"), sha256=sha256(c)))
            print(f"hashed {rows[-1]['checkpoint']}", flush=True)
    with open(REPO / "checkpoints" / "checkpoint_sha256.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["checkpoint", "bytes", "modified", "sha256"]); w.writeheader(); w.writerows(rows)
    report.append(f"written  checkpoints/checkpoint_sha256.csv ({len(rows)} checkpoints)")

    # 5. latest results (after the Stage I rerun)
    for f in sorted((r2 / "tables").glob("*.csv")):
        if not f.name.startswith("PRE_"):
            copy(f, REPO / "results" / "tables" / f.name, report)
    for f in ["I3_tsne_source.csv"]:
        copy(r2 / "tables" / f, REPO / "results" / "figure_source_data" / f, report)
    if (r2 / "RESULTS.md").exists():
        parts = re.split(r"(?m)^(?=## )", (r2 / "RESULTS.md").read_text(encoding="utf-8"))
        (REPO / "results" / "RESULTS.md").write_text("".join(p for p in parts if not p.startswith("## PRE_")), encoding="utf-8")
        report.append("written  results/RESULTS.md")
    copy(r2 / "figures" / "Fig_tsne_cohorts.png", REPO / "results" / "figures" / "Fig8.png", report)

    if a.zip_checkpoints:
        z = r2 / "zenodo_frozen_split_checkpoints.zip"
        with zipfile.ZipFile(z, "w", zipfile.ZIP_STORED) as zf:
            for c in candidates[:10]:
                if c.exists(): zf.write(c, str(c.relative_to(root)))
        report.append(f"written  {z}  (upload to Zenodo, not GitHub)")

    print("\n".join(report))
    missing = [x for x in report if x.startswith("MISSING")]
    print(f"\n{len(report) - len(missing)} items done, {len(missing)} missing")


if __name__ == "__main__":
    main()
