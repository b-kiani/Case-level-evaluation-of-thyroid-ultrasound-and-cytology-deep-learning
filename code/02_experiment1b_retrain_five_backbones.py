r"""
BHI 2026 REVISION — EXPERIMENT 1B
Frozen-manifest retraining of five ImageNet backbones
====================================================

Project root
------------
D:\Thyroid-BHI-26

Frozen manifest
---------------
D:\Thyroid-BHI-26\revision_final_frozen_70_15_15\04_frozen_manifest.csv

Required SHA-256
---------------
83e656eff33e272020d85f8faf4004285a67768d3ef79e040c59ee13ea1575f5

Models
------
1. ConvNeXt-Small
2. EfficientNet-B3
3. Swin-Tiny
4. ResNet50
5. DenseNet121

Modalities
----------
- cytology
- ultrasound

Protocol
--------
- ImageNet initialization via timm
- 224 x 224 input for every backbone
- AdamW
- learning rate 3e-4
- weight decay 1e-4
- 40 epochs
- weighted BCEWithLogitsLoss
- weighted random sampler
- fixed seed 2026
- mixed precision when CUDA is available
- best checkpoint chosen by validation AUROC
- Youden threshold selected on VALIDATION only
- frozen threshold transferred unchanged to TEST
- no test-set model selection

Outputs
-------
D:\Thyroid-BHI-26\revision_exp1b\

    environment.json
    run_manifest.csv
    <modality>\<model>\
        train_log.csv
        best_model.pt
        val_predictions.csv
        test_predictions.csv
        val_source_group_predictions.csv
        test_source_group_predictions.csv
        metrics.json
    <modality>\ensemble\
        val_predictions.csv
        test_predictions.csv
        val_source_group_predictions.csv
        test_source_group_predictions.csv
        metrics.json
    master_metrics.csv

Notes
-----
- All prediction tables retain source_group and component_id.
- This enables cluster-aware bootstrap and source-group aggregation later.
- Ensemble predictions are merged by image_path, NEVER by row order.
- Existing completed runs are skipped unless --force is supplied.

Examples
--------
Run everything:
C:\Users\admin\miniconda3\envs\nnunet\python.exe ^
  "D:\Thyroid-BHI-26\Rivision scripts\02_experiment1b_retrain_five_backbones.py"

Run cytology only:
...python.exe ...py --modality cytology

Run one model only:
...python.exe ...py --modality cytology --models convnext_small

Smaller batch if GPU memory is limited:
...python.exe ...py --batch-size 8
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import random
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

import torch
import torch.nn as nn
from torch.cuda.amp import GradScaler, autocast
from torch.utils.data import DataLoader, Dataset, WeightedRandomSampler

from PIL import Image, ImageFile

import timm

from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    precision_score,
    roc_auc_score,
    roc_curve,
)

try:
    from torchvision import transforms
except Exception as e:
    raise RuntimeError(
        "torchvision is required for Experiment 1B."
    ) from e


# =============================================================================
# CONFIG
# =============================================================================

ROOT = Path(r"D:\Thyroid-BHI-26").resolve()

FROZEN_MANIFEST = (
    ROOT
    / "revision_final_frozen_70_15_15"
    / "04_frozen_manifest.csv"
)

EXPECTED_MANIFEST_SHA256 = (
    "83e656eff33e272020d85f8faf4004285a67768d3ef79e040c59ee13ea1575f5"
)

DEFAULT_OUT = ROOT / "revision_exp1b"

SEED = 2026
EPOCHS = 40
LR = 3e-4
WEIGHT_DECAY = 1e-4
IMAGE_SIZE = 224
DEFAULT_BATCH_SIZE = 16
DEFAULT_NUM_WORKERS = 4

MODEL_REGISTRY = {
    "convnext_small": "convnext_small",
    "efficientnet_b3": "efficientnet_b3",
    "swin_tiny": "swin_tiny_patch4_window7_224",
    "resnet50": "resnet50",
    "densenet121": "densenet121",
}

MODEL_DISPLAY = {
    "convnext_small": "ConvNeXt-Small",
    "efficientnet_b3": "EfficientNet-B3",
    "swin_tiny": "Swin-Tiny",
    "resnet50": "ResNet50",
    "densenet121": "DenseNet121",
}

MODALITIES = ["cytology", "ultrasound"]

ImageFile.LOAD_TRUNCATED_IMAGES = True


# =============================================================================
# REPRODUCIBILITY
# =============================================================================

def seed_everything(seed: int):

    os.environ["PYTHONHASHSEED"] = str(seed)

    random.seed(seed)
    np.random.seed(seed)

    torch.manual_seed(seed)

    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    # Reproducible convolution choices.
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True


def sha256_file(path: Path) -> str:

    h = hashlib.sha256()

    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)

    return h.hexdigest()


# =============================================================================
# DATA
# =============================================================================

class ThyroidImageDataset(Dataset):

    def __init__(self, frame: pd.DataFrame, transform=None):

        self.df = frame.reset_index(drop=True).copy()
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

        if self.transform is not None:
            image = self.transform(image)

        label = torch.tensor(
            float(row["label"]),
            dtype=torch.float32,
        )

        return image, label, idx


def make_transforms():

    # Same 224x224 preprocessing for every architecture.
    imagenet_mean = (0.485, 0.456, 0.406)
    imagenet_std = (0.229, 0.224, 0.225)

    train_tf = transforms.Compose([
        transforms.Resize(
            (IMAGE_SIZE, IMAGE_SIZE),
            interpolation=transforms.InterpolationMode.BILINEAR,
        ),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomVerticalFlip(p=0.5),
        transforms.RandomRotation(degrees=15),
        transforms.ColorJitter(
            brightness=0.10,
            contrast=0.10,
            saturation=0.05,
            hue=0.02,
        ),
        transforms.ToTensor(),
        transforms.Normalize(
            imagenet_mean,
            imagenet_std,
        ),
    ])

    eval_tf = transforms.Compose([
        transforms.Resize(
            (IMAGE_SIZE, IMAGE_SIZE),
            interpolation=transforms.InterpolationMode.BILINEAR,
        ),
        transforms.ToTensor(),
        transforms.Normalize(
            imagenet_mean,
            imagenet_std,
        ),
    ])

    return train_tf, eval_tf


def make_loaders(
    manifest: pd.DataFrame,
    modality: str,
    batch_size: int,
    num_workers: int,
):

    m = manifest[
        manifest["modality"]
        .astype(str)
        .str.lower()
        .eq(modality)
    ].copy()

    train_df = m[m["split"].eq("train")].copy()
    val_df = m[m["split"].eq("val")].copy()
    test_df = m[m["split"].eq("test")].copy()

    if min(len(train_df), len(val_df), len(test_df)) == 0:
        raise RuntimeError(
            f"{modality}: train/val/test must all be non-empty."
        )

    train_tf, eval_tf = make_transforms()

    train_ds = ThyroidImageDataset(
        train_df,
        transform=train_tf,
    )

    val_ds = ThyroidImageDataset(
        val_df,
        transform=eval_tf,
    )

    test_ds = ThyroidImageDataset(
        test_df,
        transform=eval_tf,
    )

    # ------------------------------------------------------------------
    # Weighted sampler
    # ------------------------------------------------------------------

    y_train = train_df["label"].astype(int).to_numpy()

    classes, counts = np.unique(
        y_train,
        return_counts=True,
    )

    class_count = dict(
        zip(classes.tolist(), counts.tolist())
    )

    # inverse-frequency weight
    class_weights = {
        c: len(y_train) / (len(classes) * count)
        for c, count in class_count.items()
    }

    sample_weights = np.array(
        [
            class_weights[int(y)]
            for y in y_train
        ],
        dtype=np.float64,
    )

    generator = torch.Generator()
    generator.manual_seed(SEED)

    sampler = WeightedRandomSampler(
        weights=torch.from_numpy(sample_weights),
        num_samples=len(sample_weights),
        replacement=True,
        generator=generator,
    )

    pin_memory = torch.cuda.is_available()

    train_loader = DataLoader(
        train_ds,
        batch_size=batch_size,
        sampler=sampler,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=pin_memory,
        drop_last=False,
    )

    val_loader = DataLoader(
        val_ds,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=pin_memory,
        drop_last=False,
    )

    test_loader = DataLoader(
        test_ds,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=pin_memory,
        drop_last=False,
    )

    return (
        train_df,
        val_df,
        test_df,
        train_loader,
        val_loader,
        test_loader,
    )


# =============================================================================
# MODEL
# =============================================================================

def create_model(model_key: str):

    timm_name = MODEL_REGISTRY[model_key]

    try:
        model = timm.create_model(
            timm_name,
            pretrained=True,
            num_classes=1,
        )

    except Exception as e:

        raise RuntimeError(
            f"\nCould not initialize pretrained timm model '{timm_name}'.\n"
            f"Do NOT silently fall back to random initialization because the "
            f"revision protocol specifies ImageNet initialization.\n"
            f"Original error:\n{e}"
        ) from e

    return model


# =============================================================================
# METRICS
# =============================================================================

def safe_auc(y, p):

    y = np.asarray(y, dtype=int)
    p = np.asarray(p, dtype=float)

    if len(np.unique(y)) < 2:
        return np.nan

    return float(
        roc_auc_score(y, p)
    )


def safe_auprc(y, p):

    y = np.asarray(y, dtype=int)
    p = np.asarray(p, dtype=float)

    if len(np.unique(y)) < 2:
        return np.nan

    return float(
        average_precision_score(y, p)
    )


def youden_threshold(y, p):

    y = np.asarray(y, dtype=int)
    p = np.asarray(p, dtype=float)

    if len(np.unique(y)) < 2:
        raise RuntimeError(
            "Cannot compute Youden threshold with one class."
        )

    fpr, tpr, thresholds = roc_curve(y, p)

    j = tpr - fpr

    # Avoid inf threshold when possible.
    finite = np.isfinite(thresholds)

    if finite.any():
        valid_indices = np.where(finite)[0]
        best_local = int(
            np.argmax(j[valid_indices])
        )
        idx = valid_indices[best_local]
    else:
        idx = int(np.argmax(j))

    return float(thresholds[idx])


def classification_metrics(y, p, threshold):

    y = np.asarray(y, dtype=int)
    p = np.asarray(p, dtype=float)

    pred = (
        p >= threshold
    ).astype(int)

    tn, fp, fn, tp = confusion_matrix(
        y,
        pred,
        labels=[0, 1],
    ).ravel()

    sensitivity = (
        tp / (tp + fn)
        if (tp + fn)
        else np.nan
    )

    specificity = (
        tn / (tn + fp)
        if (tn + fp)
        else np.nan
    )

    return {
        "n": int(len(y)),
        "n_negative": int((y == 0).sum()),
        "n_positive": int((y == 1).sum()),
        "auroc": safe_auc(y, p),
        "auprc": safe_auprc(y, p),
        "threshold": float(threshold),
        "accuracy": float(
            accuracy_score(y, pred)
        ),
        "sensitivity": float(sensitivity),
        "specificity": float(specificity),
        "precision": float(
            precision_score(
                y,
                pred,
                zero_division=0,
            )
        ),
        "f1": float(
            f1_score(
                y,
                pred,
                zero_division=0,
            )
        ),
        "brier": float(
            brier_score_loss(y, p)
        ),
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
    }


# =============================================================================
# TRAIN / PREDICT
# =============================================================================

@torch.no_grad()
def predict_loader(
    model,
    loader,
    frame,
    device,
):

    model.eval()

    probs = np.zeros(
        len(frame),
        dtype=np.float64,
    )

    labels = np.zeros(
        len(frame),
        dtype=np.int64,
    )

    for images, y, idx in loader:

        images = images.to(
            device,
            non_blocking=True,
        )

        logits = model(images).reshape(-1)

        p = torch.sigmoid(
            logits
        ).detach().cpu().numpy()

        idx_np = idx.numpy()

        probs[idx_np] = p
        labels[idx_np] = y.numpy().astype(int)

    out = frame.reset_index(drop=True).copy()

    out["prob_malignant"] = probs
    out["label"] = labels

    return out


def train_one_model(
    manifest,
    modality,
    model_key,
    outdir,
    batch_size,
    num_workers,
    force=False,
):

    run_dir = (
        outdir
        / modality
        / model_key
    )

    run_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    metrics_path = (
        run_dir
        / "metrics.json"
    )

    if metrics_path.exists() and not force:

        print(
            f"[SKIP] {modality} / {model_key}: "
            f"metrics.json already exists."
        )

        with metrics_path.open(
            "r",
            encoding="utf-8",
        ) as f:
            return json.load(f)

    seed_everything(SEED)

    (
        train_df,
        val_df,
        test_df,
        train_loader,
        val_loader,
        test_loader,
    ) = make_loaders(
        manifest,
        modality,
        batch_size,
        num_workers,
    )

    device = torch.device(
        "cuda"
        if torch.cuda.is_available()
        else "cpu"
    )

    model = create_model(
        model_key
    ).to(device)

    # Weighted BCE:
    # pos_weight = N_negative / N_positive
    train_counts = (
        train_df["label"]
        .astype(int)
        .value_counts()
        .to_dict()
    )

    n_neg = int(
        train_counts.get(0, 0)
    )

    n_pos = int(
        train_counts.get(1, 0)
    )

    if n_neg == 0 or n_pos == 0:
        raise RuntimeError(
            f"{modality}: training split lacks one class."
        )

    pos_weight = torch.tensor(
        [n_neg / n_pos],
        dtype=torch.float32,
        device=device,
    )

    criterion = nn.BCEWithLogitsLoss(
        pos_weight=pos_weight,
    )

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=LR,
        weight_decay=WEIGHT_DECAY,
    )

    scaler = GradScaler(
        enabled=(
            device.type == "cuda"
        )
    )

    best_val_auc = -math.inf
    best_epoch = None

    checkpoint_path = (
        run_dir
        / "best_model.pt"
    )

    log_rows = []

    print(
        "\n"
        + "=" * 80
    )

    print(
        f"TRAINING {modality.upper()} | "
        f"{MODEL_DISPLAY[model_key]}"
    )

    print(
        "=" * 80
    )

    print(
        f"train={len(train_df)} "
        f"val={len(val_df)} "
        f"test={len(test_df)} "
        f"batch={batch_size} "
        f"device={device}"
    )

    if device.type == "cuda":
        print(
            "GPU:",
            torch.cuda.get_device_name(0),
        )

    for epoch in range(
        1,
        EPOCHS + 1,
    ):

        started = time.time()

        model.train()

        running_loss = 0.0
        n_seen = 0

        for step, (
            images,
            y,
            _,
        ) in enumerate(
            train_loader,
            1,
        ):

            images = images.to(
                device,
                non_blocking=True,
            )

            y = y.to(
                device,
                non_blocking=True,
            )

            optimizer.zero_grad(
                set_to_none=True,
            )

            with autocast(
                enabled=(
                    device.type == "cuda"
                )
            ):

                logits = model(
                    images
                ).reshape(-1)

                loss = criterion(
                    logits,
                    y,
                )

            scaler.scale(
                loss
            ).backward()

            scaler.step(
                optimizer
            )

            scaler.update()

            batch_n = int(
                y.numel()
            )

            running_loss += (
                float(loss.item())
                * batch_n
            )

            n_seen += batch_n

        train_loss = (
            running_loss
            / max(1, n_seen)
        )

        val_pred = predict_loader(
            model,
            val_loader,
            val_df,
            device,
        )

        val_auc = safe_auc(
            val_pred["label"],
            val_pred["prob_malignant"],
        )

        val_auprc = safe_auprc(
            val_pred["label"],
            val_pred["prob_malignant"],
        )

        elapsed = (
            time.time()
            - started
        )

        improved = (
            np.isfinite(val_auc)
            and val_auc > best_val_auc
        )

        if improved:

            best_val_auc = val_auc
            best_epoch = epoch

            torch.save(
                {
                    "model_state_dict": model.state_dict(),
                    "model_key": model_key,
                    "timm_model_name": MODEL_REGISTRY[model_key],
                    "modality": modality,
                    "epoch": epoch,
                    "val_auroc": val_auc,
                    "seed": SEED,
                    "image_size": IMAGE_SIZE,
                    "lr": LR,
                    "weight_decay": WEIGHT_DECAY,
                    "manifest_sha256": EXPECTED_MANIFEST_SHA256,
                },
                checkpoint_path,
            )

        log_rows.append({
            "epoch": epoch,
            "train_loss": train_loss,
            "val_auroc": val_auc,
            "val_auprc": val_auprc,
            "best_val_auroc": best_val_auc,
            "best_epoch": best_epoch,
            "seconds": elapsed,
        })

        pd.DataFrame(
            log_rows
        ).to_csv(
            run_dir
            / "train_log.csv",
            index=False,
        )

        star = " *BEST*" if improved else ""

        print(
            f"epoch {epoch:02d}/{EPOCHS} "
            f"loss={train_loss:.5f} "
            f"val_auc={val_auc:.5f} "
            f"val_ap={val_auprc:.5f} "
            f"time={elapsed:.1f}s"
            f"{star}",
            flush=True,
        )

    if not checkpoint_path.exists():
        raise RuntimeError(
            f"No best checkpoint saved for {modality}/{model_key}."
        )

    checkpoint = torch.load(
        checkpoint_path,
        map_location=device,
    )

    model.load_state_dict(
        checkpoint["model_state_dict"]
    )

    # ------------------------------------------------------------------
    # Frozen post-training predictions
    # ------------------------------------------------------------------

    val_pred = predict_loader(
        model,
        val_loader,
        val_df,
        device,
    )

    test_pred = predict_loader(
        model,
        test_loader,
        test_df,
        device,
    )

    threshold = youden_threshold(
        val_pred["label"],
        val_pred["prob_malignant"],
    )

    val_metrics = classification_metrics(
        val_pred["label"],
        val_pred["prob_malignant"],
        threshold,
    )

    test_metrics = classification_metrics(
        test_pred["label"],
        test_pred["prob_malignant"],
        threshold,
    )

    val_pred["operating_threshold"] = threshold
    test_pred["operating_threshold"] = threshold

    val_pred.to_csv(
        run_dir
        / "val_predictions.csv",
        index=False,
    )

    test_pred.to_csv(
        run_dir
        / "test_predictions.csv",
        index=False,
    )

    # ------------------------------------------------------------------
    # Source-group aggregated predictions
    # ------------------------------------------------------------------

    agg_spec = {
        "label": "first",
        "prob_malignant": "mean",
        "component_id": "first",
    }

    val_group = (
        val_pred.groupby(
            "source_group",
            as_index=False,
        )
        .agg(agg_spec)
    )

    test_group = (
        test_pred.groupby(
            "source_group",
            as_index=False,
        )
        .agg(agg_spec)
    )

    val_group["n_images"] = (
        val_pred.groupby(
            "source_group"
        ).size().reindex(
            val_group["source_group"]
        ).to_numpy()
    )

    test_group["n_images"] = (
        test_pred.groupby(
            "source_group"
        ).size().reindex(
            test_group["source_group"]
        ).to_numpy()
    )

    val_group.to_csv(
        run_dir
        / "val_source_group_predictions.csv",
        index=False,
    )

    test_group.to_csv(
        run_dir
        / "test_source_group_predictions.csv",
        index=False,
    )

    group_threshold = youden_threshold(
        val_group["label"],
        val_group["prob_malignant"],
    )

    val_group_metrics = classification_metrics(
        val_group["label"],
        val_group["prob_malignant"],
        group_threshold,
    )

    test_group_metrics = classification_metrics(
        test_group["label"],
        test_group["prob_malignant"],
        group_threshold,
    )

    result = {
        "modality": modality,
        "model_key": model_key,
        "model_display": MODEL_DISPLAY[model_key],
        "timm_model_name": MODEL_REGISTRY[model_key],
        "best_epoch": int(best_epoch),
        "best_val_auroc": float(best_val_auc),
        "image_level_threshold_from_val": float(threshold),
        "source_group_threshold_from_val": float(group_threshold),
        "image_level_val": val_metrics,
        "image_level_test": test_metrics,
        "source_group_val": val_group_metrics,
        "source_group_test": test_group_metrics,
        "manifest_sha256": EXPECTED_MANIFEST_SHA256,
        "seed": SEED,
        "epochs": EPOCHS,
        "lr": LR,
        "weight_decay": WEIGHT_DECAY,
        "image_size": IMAGE_SIZE,
        "batch_size": batch_size,
        "pos_weight": float(
            pos_weight.item()
        ),
    }

    with metrics_path.open(
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            result,
            f,
            indent=2,
        )

    print(
        f"\nFINAL {modality}/{model_key}: "
        f"test AUROC={test_metrics['auroc']:.4f}, "
        f"AUPRC={test_metrics['auprc']:.4f}, "
        f"threshold={threshold:.4f}"
    )

    print(
        f"SOURCE-GROUP test AUROC="
        f"{test_group_metrics['auroc']:.4f}, "
        f"AUPRC={test_group_metrics['auprc']:.4f}"
    )

    # release GPU memory between models
    del model
    torch.cuda.empty_cache()

    return result


# =============================================================================
# ENSEMBLE
# =============================================================================

def build_ensemble(
    outdir,
    modality,
    model_keys,
):

    ens_dir = (
        outdir
        / modality
        / "ensemble"
    )

    ens_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    merged = {}

    for split_name in [
        "val",
        "test",
    ]:

        base = None

        for model_key in model_keys:

            path = (
                outdir
                / modality
                / model_key
                / f"{split_name}_predictions.csv"
            )

            if not path.exists():
                raise FileNotFoundError(
                    f"Missing prediction file for ensemble: {path}"
                )

            df = pd.read_csv(
                path,
                low_memory=False,
            )

            keep = [
                "image_path",
                "label",
                "source_group",
                "component_id",
                "prob_malignant",
            ]

            missing = [
                c for c in keep
                if c not in df.columns
            ]

            if missing:
                raise RuntimeError(
                    f"{path} missing ensemble columns: {missing}"
                )

            d = df[
                keep
            ].copy()

            d = d.rename(
                columns={
                    "prob_malignant":
                    f"prob_{model_key}"
                }
            )

            if base is None:
                base = d

            else:
                base = base.merge(
                    d,
                    on=[
                        "image_path",
                        "label",
                        "source_group",
                        "component_id",
                    ],
                    how="inner",
                    validate="one_to_one",
                )

        prob_cols = [
            f"prob_{k}"
            for k in model_keys
        ]

        base[
            "prob_malignant"
        ] = base[
            prob_cols
        ].mean(
            axis=1
        )

        merged[
            split_name
        ] = base

    val = merged["val"]
    test = merged["test"]

    threshold = youden_threshold(
        val["label"],
        val["prob_malignant"],
    )

    val_metrics = classification_metrics(
        val["label"],
        val["prob_malignant"],
        threshold,
    )

    test_metrics = classification_metrics(
        test["label"],
        test["prob_malignant"],
        threshold,
    )

    val[
        "operating_threshold"
    ] = threshold

    test[
        "operating_threshold"
    ] = threshold

    val.to_csv(
        ens_dir
        / "val_predictions.csv",
        index=False,
    )

    test.to_csv(
        ens_dir
        / "test_predictions.csv",
        index=False,
    )

    # group means
    prob_cols = [
        c for c in val.columns
        if c.startswith("prob_")
        and c != "prob_malignant"
    ]

    agg = {
        "label": "first",
        "component_id": "first",
        "prob_malignant": "mean",
    }

    for c in prob_cols:
        agg[c] = "mean"

    val_group = (
        val.groupby(
            "source_group",
            as_index=False,
        )
        .agg(agg)
    )

    test_group = (
        test.groupby(
            "source_group",
            as_index=False,
        )
        .agg(agg)
    )

    val_group["n_images"] = (
        val.groupby(
            "source_group"
        ).size().reindex(
            val_group["source_group"]
        ).to_numpy()
    )

    test_group["n_images"] = (
        test.groupby(
            "source_group"
        ).size().reindex(
            test_group["source_group"]
        ).to_numpy()
    )

    group_threshold = youden_threshold(
        val_group["label"],
        val_group["prob_malignant"],
    )

    val_group_metrics = classification_metrics(
        val_group["label"],
        val_group["prob_malignant"],
        group_threshold,
    )

    test_group_metrics = classification_metrics(
        test_group["label"],
        test_group["prob_malignant"],
        group_threshold,
    )

    val_group.to_csv(
        ens_dir
        / "val_source_group_predictions.csv",
        index=False,
    )

    test_group.to_csv(
        ens_dir
        / "test_source_group_predictions.csv",
        index=False,
    )

    result = {
        "modality": modality,
        "model_key": "ensemble",
        "model_display": "Mean-probability Ensemble",
        "ensemble_members": model_keys,
        "image_level_threshold_from_val": float(threshold),
        "source_group_threshold_from_val": float(group_threshold),
        "image_level_val": val_metrics,
        "image_level_test": test_metrics,
        "source_group_val": val_group_metrics,
        "source_group_test": test_group_metrics,
        "manifest_sha256": EXPECTED_MANIFEST_SHA256,
    }

    with (
        ens_dir
        / "metrics.json"
    ).open(
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            result,
            f,
            indent=2,
        )

    print(
        f"\nENSEMBLE {modality}: "
        f"test AUROC={test_metrics['auroc']:.4f}, "
        f"AUPRC={test_metrics['auprc']:.4f}"
    )

    return result


# =============================================================================
# MASTER TABLE
# =============================================================================

def flatten_result(result):

    row = {
        "modality": result["modality"],
        "model": result["model_display"],
        "model_key": result["model_key"],
        "manifest_sha256": result["manifest_sha256"],
    }

    for section_key, prefix in [
        ("image_level_val", "val_img"),
        ("image_level_test", "test_img"),
        ("source_group_val", "val_group"),
        ("source_group_test", "test_group"),
    ]:

        section = result.get(
            section_key,
            {}
        )

        for k, v in section.items():
            row[f"{prefix}_{k}"] = v

    row["image_threshold"] = result.get(
        "image_level_threshold_from_val",
        np.nan,
    )

    row["group_threshold"] = result.get(
        "source_group_threshold_from_val",
        np.nan,
    )

    row["best_epoch"] = result.get(
        "best_epoch",
        np.nan,
    )

    return row


# =============================================================================
# MAIN
# =============================================================================

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--manifest",
        type=Path,
        default=FROZEN_MANIFEST,
    )

    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT,
    )

    parser.add_argument(
        "--modality",
        choices=[
            "all",
            "cytology",
            "ultrasound",
        ],
        default="all",
    )

    parser.add_argument(
        "--models",
        nargs="+",
        choices=list(
            MODEL_REGISTRY.keys()
        ),
        default=list(
            MODEL_REGISTRY.keys()
        ),
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=DEFAULT_BATCH_SIZE,
    )

    parser.add_argument(
        "--num-workers",
        type=int,
        default=DEFAULT_NUM_WORKERS,
    )

    parser.add_argument(
        "--force",
        action="store_true",
    )

    args = parser.parse_args()

    manifest_path = args.manifest.resolve()
    outdir = args.out.resolve()

    if not manifest_path.exists():
        raise FileNotFoundError(
            manifest_path
        )

    actual_hash = sha256_file(
        manifest_path
    )

    if actual_hash != EXPECTED_MANIFEST_SHA256:

        raise RuntimeError(
            "\nFROZEN MANIFEST HASH MISMATCH.\n"
            f"Expected: {EXPECTED_MANIFEST_SHA256}\n"
            f"Actual  : {actual_hash}\n"
            "Do not train until the manifest is reconciled."
        )

    manifest = pd.read_csv(
        manifest_path,
        low_memory=False,
    )

    required = {
        "image_path",
        "modality",
        "label",
        "split",
        "source_group",
        "component_id",
    }

    missing = sorted(
        required
        - set(manifest.columns)
    )

    if missing:
        raise RuntimeError(
            f"Frozen manifest is missing columns: {missing}"
        )

    # ------------------------------------------------------------------
    # Environment provenance
    # ------------------------------------------------------------------

    outdir.mkdir(
        parents=True,
        exist_ok=True,
    )

    environment = {
        "python": sys.version,
        "platform": platform.platform(),
        "torch": torch.__version__,
        "timm": getattr(
            timm,
            "__version__",
            "unknown",
        ),
        "numpy": np.__version__,
        "pandas": pd.__version__,
        "cuda_available": torch.cuda.is_available(),
        "cuda_version": torch.version.cuda,
        "gpu": (
            torch.cuda.get_device_name(0)
            if torch.cuda.is_available()
            else None
        ),
        "manifest": str(manifest_path),
        "manifest_sha256": actual_hash,
        "seed": SEED,
        "epochs": EPOCHS,
        "lr": LR,
        "weight_decay": WEIGHT_DECAY,
        "image_size": IMAGE_SIZE,
        "batch_size": args.batch_size,
        "num_workers": args.num_workers,
        "models": args.models,
        "modality_arg": args.modality,
    }

    with (
        outdir
        / "environment.json"
    ).open(
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            environment,
            f,
            indent=2,
        )

    modalities = (
        MODALITIES
        if args.modality == "all"
        else [args.modality]
    )

    print("=" * 88)
    print("BHI 2026 REVISION — EXPERIMENT 1B")
    print("=" * 88)
    print("Manifest:", manifest_path)
    print("SHA256  :", actual_hash)
    print("Output  :", outdir)
    print("Models  :", ", ".join(args.models))
    print("Modalities:", ", ".join(modalities))
    print("Batch   :", args.batch_size)
    print("Epochs  :", EPOCHS)
    print("Seed    :", SEED)

    if torch.cuda.is_available():
        print("GPU     :", torch.cuda.get_device_name(0))
    else:
        print("WARNING : CUDA not available; training will be very slow.")

    # ------------------------------------------------------------------
    # Train
    # ------------------------------------------------------------------

    results = []

    for modality in modalities:

        for model_key in args.models:

            result = train_one_model(
                manifest=manifest,
                modality=modality,
                model_key=model_key,
                outdir=outdir,
                batch_size=args.batch_size,
                num_workers=args.num_workers,
                force=args.force,
            )

            results.append(
                result
            )

        # Build ensemble only when all five requested canonical models exist.
        canonical = list(
            MODEL_REGISTRY.keys()
        )

        all_available = all(
            (
                outdir
                / modality
                / k
                / "test_predictions.csv"
            ).exists()
            and
            (
                outdir
                / modality
                / k
                / "val_predictions.csv"
            ).exists()
            for k in canonical
        )

        if all_available:

            ensemble_result = build_ensemble(
                outdir,
                modality,
                canonical,
            )

            results.append(
                ensemble_result
            )

        else:

            print(
                f"\n[INFO] Ensemble for {modality} not built yet "
                f"because not all five canonical model prediction files exist."
            )

    # ------------------------------------------------------------------
    # Collect all existing metrics into one master table
    # ------------------------------------------------------------------

    master_results = []

    for modality in MODALITIES:

        for model_key in (
            list(MODEL_REGISTRY.keys())
            + ["ensemble"]
        ):

            path = (
                outdir
                / modality
                / model_key
                / "metrics.json"
            )

            if not path.exists():
                continue

            with path.open(
                "r",
                encoding="utf-8",
            ) as f:

                r = json.load(f)

            master_results.append(
                flatten_result(r)
            )

    master_df = pd.DataFrame(
        master_results
    )

    master_path = (
        outdir
        / "master_metrics.csv"
    )

    master_df.to_csv(
        master_path,
        index=False,
    )

    print("\n" + "=" * 88)
    print("EXPERIMENT 1B CURRENT SUMMARY")
    print("=" * 88)

    if master_df.empty:
        print("No completed metrics found.")
    else:

        cols = [
            c for c in [
                "modality",
                "model",
                "test_img_n",
                "test_img_auroc",
                "test_img_auprc",
                "test_img_sensitivity",
                "test_img_specificity",
                "test_group_n",
                "test_group_auroc",
                "test_group_auprc",
            ]
            if c in master_df.columns
        ]

        print(
            master_df[
                cols
            ].to_string(
                index=False
            )
        )

    print("\nMaster metrics:")
    print(master_path)

    print(
        "\nWhen all 10 backbone runs + both ensembles are complete, "
        "send me master_metrics.csv or paste this summary."
    )


if __name__ == "__main__":
    main()
