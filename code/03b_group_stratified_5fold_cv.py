r"""
BHI 2026 REVISION — EXPERIMENT 2B
Leakage-safe 5-fold group-stratified cross-validation.

Uses ONLY frozen train+val data. Frozen test is never touched.
Outer and inner splits use StratifiedGroupKFold with duplicate-connected
component_id as the grouping unit.

Default: ConvNeXt-Small, both cytology and ultrasound.
"""

from __future__ import annotations
import argparse, hashlib, json, math, os, platform, random, sys, time
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageFile

import torch
import torch.nn as nn
from torch.cuda.amp import GradScaler, autocast
from torch.utils.data import Dataset, DataLoader, WeightedRandomSampler

import timm
from torchvision import transforms
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.metrics import (
    roc_auc_score, average_precision_score, roc_curve,
    confusion_matrix, accuracy_score
)

ROOT = Path(r"D:\Thyroid-BHI-26")
MANIFEST = ROOT / "revision_final_frozen_70_15_15" / "04_frozen_manifest.csv"
EXPECTED_SHA = "83e656eff33e272020d85f8faf4004285a67768d3ef79e040c59ee13ea1575f5"
DEFAULT_OUT = ROOT / "revision_exp2b_group_cv"

SEED = 2026
OUTER_FOLDS = 5
EPOCHS = 40
LR = 3e-4
WD = 1e-4
IMAGE_SIZE = 224

MODELS = {
    "convnext_small": "convnext_small",
    "efficientnet_b3": "efficientnet_b3",
    "swin_tiny": "swin_tiny_patch4_window7_224",
    "resnet50": "resnet50",
    "densenet121": "densenet121",
}
DISPLAY = {
    "convnext_small": "ConvNeXt-Small",
    "efficientnet_b3": "EfficientNet-B3",
    "swin_tiny": "Swin-Tiny",
    "resnet50": "ResNet50",
    "densenet121": "DenseNet121",
}
MODALITIES = ["cytology", "ultrasound"]

ImageFile.LOAD_TRUNCATED_IMAGES = True


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def seed_all(seed):
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True


def safe_auc(y, p):
    y = np.asarray(y, int)
    if len(np.unique(y)) < 2:
        return np.nan
    return float(roc_auc_score(y, p))


def safe_ap(y, p):
    y = np.asarray(y, int)
    if len(np.unique(y)) < 2:
        return np.nan
    return float(average_precision_score(y, p))


def youden(y, p):
    fpr, tpr, thr = roc_curve(np.asarray(y, int), np.asarray(p, float))
    finite = np.where(np.isfinite(thr))[0]
    if len(finite) == 0:
        return 0.5
    j = tpr[finite] - fpr[finite]
    return float(thr[finite[np.argmax(j)]])


def threshold_metrics(y, p, threshold):
    y = np.asarray(y, int)
    pred = (np.asarray(p, float) >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()
    return {
        "accuracy": float(accuracy_score(y, pred)),
        "sensitivity": float(tp/(tp+fn)) if tp+fn else np.nan,
        "specificity": float(tn/(tn+fp)) if tn+fp else np.nan,
        "tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp),
    }


class ThyroidDataset(Dataset):
    def __init__(self, df, transform):
        self.df = df.reset_index(drop=True).copy()
        self.transform = transform

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        path = Path(str(row["image_path"]))
        if not path.exists():
            raise FileNotFoundError(path)
        with Image.open(path) as im:
            image = im.convert("RGB")
        image = self.transform(image)
        y = torch.tensor(float(row["label"]), dtype=torch.float32)
        return image, y, idx


def transforms_for_run():
    mean = (0.485, 0.456, 0.406)
    std = (0.229, 0.224, 0.225)
    train_tf = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.RandomHorizontalFlip(0.5),
        transforms.RandomVerticalFlip(0.5),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.10, contrast=0.10,
                               saturation=0.05, hue=0.02),
        transforms.ToTensor(),
        transforms.Normalize(mean, std),
    ])
    eval_tf = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean, std),
    ])
    return train_tf, eval_tf


def make_sampler(df, seed):
    y = df["label"].astype(int).to_numpy()
    classes, counts = np.unique(y, return_counts=True)
    cw = {int(c): len(y)/(len(classes)*int(n))
          for c, n in zip(classes, counts)}
    weights = torch.tensor([cw[int(v)] for v in y], dtype=torch.double)
    g = torch.Generator()
    g.manual_seed(seed)
    return WeightedRandomSampler(weights, len(weights), replacement=True,
                                 generator=g)


def make_loader(df, transform, batch, workers, sampler=None):
    return DataLoader(
        ThyroidDataset(df, transform),
        batch_size=batch,
        sampler=sampler,
        shuffle=False,
        num_workers=workers,
        pin_memory=torch.cuda.is_available(),
        drop_last=False,
    )


def create_model(key):
    try:
        return timm.create_model(MODELS[key], pretrained=True, num_classes=1)
    except Exception as e:
        raise RuntimeError(
            f"Could not create ImageNet-pretrained {MODELS[key]}: {e}"
        ) from e


@torch.no_grad()
def predict(model, loader, df, device):
    model.eval()
    probs = np.zeros(len(df), float)
    labels = np.zeros(len(df), int)
    for images, y, idx in loader:
        images = images.to(device, non_blocking=True)
        p = torch.sigmoid(model(images).reshape(-1)).cpu().numpy()
        idxn = idx.numpy()
        probs[idxn] = p
        labels[idxn] = y.numpy().astype(int)
    out = df.reset_index(drop=True).copy()
    out["label"] = labels
    out["prob_malignant"] = probs
    return out


def assert_disjoint(a, b, name):
    overlap = set(a["_component_uid"]).intersection(set(b["_component_uid"]))
    if overlap:
        raise RuntimeError(f"{name}: {len(overlap)} components overlap.")


def make_outer_splits(df, seed):
    sgkf = StratifiedGroupKFold(
        n_splits=OUTER_FOLDS, shuffle=True, random_state=seed
    )
    return list(sgkf.split(
        df, df["label"].astype(int), groups=df["_component_uid"]
    ))


def make_inner_split(df, seed):
    sgkf = StratifiedGroupKFold(
        n_splits=5, shuffle=True, random_state=seed
    )
    return next(sgkf.split(
        df, df["label"].astype(int), groups=df["_component_uid"]
    ))


def run_fold(dev_df, outer_train_idx, outer_hold_idx, modality, model_key,
             fold, run_dir, batch, workers):

    fold_seed = SEED + fold * 100
    seed_all(fold_seed)

    outer_train = dev_df.iloc[outer_train_idx].reset_index(drop=True)
    outer_hold = dev_df.iloc[outer_hold_idx].reset_index(drop=True)

    inner_train_idx, inner_val_idx = make_inner_split(
        outer_train, fold_seed + 1
    )
    inner_train = outer_train.iloc[inner_train_idx].reset_index(drop=True)
    inner_val = outer_train.iloc[inner_val_idx].reset_index(drop=True)

    assert_disjoint(inner_train, inner_val, "inner train/val")
    assert_disjoint(outer_train, outer_hold, "outer train/holdout")

    fold_dir = run_dir / f"fold_{fold}"
    fold_dir.mkdir(parents=True, exist_ok=True)

    train_tf, eval_tf = transforms_for_run()

    train_loader = make_loader(
        inner_train, train_tf, batch, workers,
        sampler=make_sampler(inner_train, fold_seed)
    )
    val_loader = make_loader(inner_val, eval_tf, batch, workers)
    hold_loader = make_loader(outer_hold, eval_tf, batch, workers)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = create_model(model_key).to(device)

    vc = inner_train["label"].astype(int).value_counts().to_dict()
    n_neg, n_pos = int(vc.get(0, 0)), int(vc.get(1, 0))
    if not n_neg or not n_pos:
        raise RuntimeError("Inner training split lacks a class.")

    pos_weight = torch.tensor(
        [n_neg / n_pos], dtype=torch.float32, device=device
    )
    criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
    optimizer = torch.optim.AdamW(model.parameters(), lr=LR, weight_decay=WD)
    scaler = GradScaler(enabled=device.type == "cuda")

    ckpt = fold_dir / "best_model.pt"
    best_auc = -math.inf
    best_epoch = None
    log = []

    print(
        f"\n{modality.upper()} | {DISPLAY[model_key]} | "
        f"OUTER FOLD {fold}/{OUTER_FOLDS}"
    )
    print(
        f"inner_train={len(inner_train)} "
        f"inner_val={len(inner_val)} outer_holdout={len(outer_hold)} | "
        f"component groups="
        f"{inner_train['_component_uid'].nunique()}/"
        f"{inner_val['_component_uid'].nunique()}/"
        f"{outer_hold['_component_uid'].nunique()}"
    )

    for epoch in range(1, EPOCHS + 1):
        t0 = time.time()
        model.train()
        loss_sum, n_seen = 0.0, 0

        for images, y, _ in train_loader:
            images = images.to(device, non_blocking=True)
            y = y.to(device, non_blocking=True)
            optimizer.zero_grad(set_to_none=True)

            with autocast(enabled=device.type == "cuda"):
                logits = model(images).reshape(-1)
                loss = criterion(logits, y)

            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()

            n = int(y.numel())
            loss_sum += float(loss.item()) * n
            n_seen += n

        val_pred = predict(model, val_loader, inner_val, device)
        val_auc = safe_auc(val_pred["label"], val_pred["prob_malignant"])
        val_ap = safe_ap(val_pred["label"], val_pred["prob_malignant"])
        improved = np.isfinite(val_auc) and val_auc > best_auc

        if improved:
            best_auc = val_auc
            best_epoch = epoch
            torch.save({
                "model_state_dict": model.state_dict(),
                "model_key": model_key,
                "modality": modality,
                "outer_fold": fold,
                "best_epoch": epoch,
                "inner_val_auroc": val_auc,
                "seed": fold_seed,
                "manifest_sha256": EXPECTED_SHA,
            }, ckpt)

        row = {
            "epoch": epoch,
            "train_loss": loss_sum/max(1, n_seen),
            "inner_val_auroc": val_auc,
            "inner_val_auprc": val_ap,
            "best_inner_val_auroc": best_auc,
            "best_epoch": best_epoch,
            "seconds": time.time()-t0,
        }
        log.append(row)
        pd.DataFrame(log).to_csv(fold_dir / "train_log.csv", index=False)

        mark = " *BEST*" if improved else ""
        print(
            f"fold {fold} epoch {epoch:02d}/{EPOCHS} "
            f"loss={row['train_loss']:.4f} "
            f"inner_auc={val_auc:.4f} "
            f"time={row['seconds']:.1f}s{mark}",
            flush=True,
        )

    if not ckpt.exists():
        raise RuntimeError("No checkpoint was created.")

    saved = torch.load(ckpt, map_location=device)
    model.load_state_dict(saved["model_state_dict"])

    val_pred = predict(model, val_loader, inner_val, device)
    threshold = youden(val_pred["label"], val_pred["prob_malignant"])

    hold_pred = predict(model, hold_loader, outer_hold, device)
    hold_pred["outer_fold"] = fold
    hold_pred["threshold_from_inner_val"] = threshold
    hold_pred["best_epoch"] = best_epoch
    hold_pred["model_key"] = model_key

    hold_pred.to_csv(
        fold_dir / "outer_holdout_predictions.csv", index=False
    )

    fold_auc = safe_auc(hold_pred["label"], hold_pred["prob_malignant"])
    fold_ap = safe_ap(hold_pred["label"], hold_pred["prob_malignant"])
    tm = threshold_metrics(
        hold_pred["label"], hold_pred["prob_malignant"], threshold
    )

    fm = {
        "modality": modality,
        "model_key": model_key,
        "model": DISPLAY[model_key],
        "outer_fold": fold,
        "n_images": len(hold_pred),
        "n_source_groups": hold_pred["source_group"].nunique(),
        "n_components": hold_pred["_component_uid"].nunique(),
        "auroc": fold_auc,
        "auprc": fold_ap,
        "threshold_from_inner_val": threshold,
        "best_epoch": best_epoch,
        "inner_best_val_auroc": best_auc,
        **tm,
    }

    with open(fold_dir / "fold_metrics.json", "w", encoding="utf-8") as f:
        json.dump(fm, f, indent=2)

    print(
        f"FOLD {fold} OUTER RESULT: AUROC={fold_auc:.4f}, "
        f"AUPRC={fold_ap:.4f}, threshold={threshold:.4f}"
    )

    del model
    torch.cuda.empty_cache()
    return hold_pred, fm


def aggregate_source_groups(oof):
    return (
        oof.groupby(["source_group", "outer_fold"], as_index=False)
        .agg(
            label=("label", "first"),
            prob_malignant=("prob_malignant", "mean"),
            component_id=("component_id", "first"),
            n_images=("image_path", "size"),
        )
    )


def summarize_cv(oof, fold_metrics, modality, model_key):
    fm = pd.DataFrame(fold_metrics)
    group_oof = aggregate_source_groups(oof)

    summary = {
        "modality": modality,
        "model_key": model_key,
        "model": DISPLAY[model_key],
        "n_outer_folds": OUTER_FOLDS,
        "development_images": len(oof),
        "development_source_groups": oof["source_group"].nunique(),
        "development_components": oof["_component_uid"].nunique(),
        "fold_auroc_mean": float(fm["auroc"].mean()),
        "fold_auroc_sd": float(fm["auroc"].std(ddof=1)),
        "fold_auprc_mean": float(fm["auprc"].mean()),
        "fold_auprc_sd": float(fm["auprc"].std(ddof=1)),
        "pooled_oof_image_auroc": safe_auc(
            oof["label"], oof["prob_malignant"]
        ),
        "pooled_oof_image_auprc": safe_ap(
            oof["label"], oof["prob_malignant"]
        ),
        "pooled_oof_source_group_auroc": safe_auc(
            group_oof["label"], group_oof["prob_malignant"]
        ),
        "pooled_oof_source_group_auprc": safe_ap(
            group_oof["label"], group_oof["prob_malignant"]
        ),
        "manifest_sha256": EXPECTED_SHA,
    }
    return summary, group_oof, fm


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--models", nargs="+", choices=list(MODELS),
        default=["convnext_small"]
    )
    ap.add_argument(
        "--modality", choices=["all", "cytology", "ultrasound"],
        default="all"
    )
    ap.add_argument("--batch-size", type=int, default=16)
    ap.add_argument("--num-workers", type=int, default=4)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()

    actual = sha256_file(MANIFEST)
    if actual != EXPECTED_SHA:
        raise RuntimeError(
            f"Frozen manifest SHA mismatch.\nExpected: {EXPECTED_SHA}\n"
            f"Actual:   {actual}"
        )

    manifest = pd.read_csv(MANIFEST, low_memory=False)
    manifest["_component_uid"] = (
        manifest["modality"].astype(str).str.lower()
        + "::component" + manifest["component_id"].astype(str)
    )

    dev = manifest[manifest["split"].isin(["train", "val"])].copy()
    frozen_test = manifest[manifest["split"].eq("test")].copy()

    if set(dev["_component_uid"]).intersection(
        set(frozen_test["_component_uid"])
    ):
        raise RuntimeError("Frozen test overlaps development components.")

    outdir = args.out.resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    modalities = MODALITIES if args.modality == "all" else [args.modality]

    env = {
        "python": sys.version,
        "platform": platform.platform(),
        "torch": torch.__version__,
        "timm": getattr(timm, "__version__", "unknown"),
        "cuda_available": torch.cuda.is_available(),
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "manifest_sha256": actual,
        "outer_cv": "StratifiedGroupKFold",
        "outer_folds": OUTER_FOLDS,
        "group_variable": "component_id",
        "cv_data": "frozen train+val only",
        "frozen_test_used": False,
        "inner_validation": "StratifiedGroupKFold first fold",
        "epochs": EPOCHS,
        "seed": SEED,
        "models": args.models,
    }
    with open(outdir / "environment.json", "w", encoding="utf-8") as f:
        json.dump(env, f, indent=2)

    print("=" * 94)
    print("BHI 2026 REVISION — GROUP-STRATIFIED 5-FOLD CV")
    print("=" * 94)
    print("Manifest SHA256 :", actual)
    print("Outer splitter  : StratifiedGroupKFold")
    print("Grouping unit   : duplicate-connected component_id")
    print("CV data         : frozen train + val only")
    print("Frozen test     : excluded from all CV folds")
    print("Models          :", ", ".join(args.models))
    print("Modalities      :", ", ".join(modalities))

    master = []
    assignments = []

    for modality in modalities:
        mdev = (
            dev[dev["modality"].astype(str).str.lower().eq(modality)]
            .copy().reset_index(drop=True)
        )
        outer_splits = make_outer_splits(mdev, SEED)

        for fold, (_, hold_idx) in enumerate(outer_splits, 1):
            a = mdev.iloc[hold_idx][
                ["image_path", "label", "source_group",
                 "component_id", "_component_uid"]
            ].copy()
            a["modality"] = modality
            a["outer_fold"] = fold
            assignments.append(a)

        for model_key in args.models:
            run_dir = outdir / modality / model_key
            run_dir.mkdir(parents=True, exist_ok=True)

            oof_parts, fold_metrics = [], []

            for fold, (train_idx, hold_idx) in enumerate(outer_splits, 1):
                pred, fm = run_fold(
                    mdev, train_idx, hold_idx, modality, model_key,
                    fold, run_dir, args.batch_size, args.num_workers
                )
                oof_parts.append(pred)
                fold_metrics.append(fm)

            oof = pd.concat(oof_parts, ignore_index=True)

            if len(oof) != len(mdev):
                raise RuntimeError("OOF rows do not cover development set.")
            if oof["image_path"].duplicated().any():
                raise RuntimeError("OOF image appears more than once.")
            if set(oof["image_path"]) != set(mdev["image_path"]):
                raise RuntimeError("OOF image set differs from development set.")

            summary, group_oof, fm_df = summarize_cv(
                oof, fold_metrics, modality, model_key
            )

            oof.to_csv(run_dir / "oof_predictions.csv", index=False)
            group_oof.to_csv(
                run_dir / "oof_source_group_predictions.csv", index=False
            )
            fm_df.to_csv(run_dir / "fold_metrics.csv", index=False)

            with open(run_dir / "cv_summary.json", "w", encoding="utf-8") as f:
                json.dump(summary, f, indent=2)

            master.append(summary)

            print(
                f"\nCV SUMMARY | {modality} | {DISPLAY[model_key]}\n"
                f"Fold AUROC = {summary['fold_auroc_mean']:.4f} ± "
                f"{summary['fold_auroc_sd']:.4f}\n"
                f"Pooled OOF image AUROC = "
                f"{summary['pooled_oof_image_auroc']:.4f}\n"
                f"Pooled OOF source-group AUROC = "
                f"{summary['pooled_oof_source_group_auroc']:.4f}"
            )

    if assignments:
        pd.concat(assignments, ignore_index=True).to_csv(
            outdir / "fold_assignment.csv", index=False
        )

    master_df = pd.DataFrame(master)
    master_df.to_csv(outdir / "master_cv_summary.csv", index=False)

    print("\n" + "=" * 94)
    print("COPY/PASTE THIS BLOCK")
    print("=" * 94)

    cols = [
        "modality", "model",
        "development_images", "development_source_groups",
        "development_components",
        "fold_auroc_mean", "fold_auroc_sd",
        "fold_auprc_mean", "fold_auprc_sd",
        "pooled_oof_image_auroc", "pooled_oof_image_auprc",
        "pooled_oof_source_group_auroc",
        "pooled_oof_source_group_auprc",
    ]
    print(master_df[cols].to_string(index=False))
    print("\nSaved:", outdir / "master_cv_summary.csv")
    print("\nSUCCESS — frozen test set remained outside all CV folds.")


if __name__ == "__main__":
    main()
