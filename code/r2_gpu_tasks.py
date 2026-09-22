
"""Round-2 GPU tasks (inference only; no training).
Imports the audited 03b script, so datasets, transforms, prediction and fold construction
are identical to the cross-validation runs that produced the checkpoints."""
import argparse, importlib.util, json, sys, time
from pathlib import Path
import numpy as np
import pandas as pd
import torch
import timm
from PIL import Image


def load_module(path, name="exp2b"):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def tload(path, device):
    try:
        return torch.load(str(path), map_location=device, weights_only=False)
    except TypeError:
        return torch.load(str(path), map_location=device)


def device_of():
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def build_model(m, key, ckpt, device):
    model = timm.create_model(m.MODELS[key], pretrained=False, num_classes=1)
    state = tload(ckpt, device)
    sd = state["model_state_dict"] if isinstance(state, dict) and "model_state_dict" in state else state
    model.load_state_dict(sd)
    return model.to(device).eval()


def free(model):
    del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


def with_labels(df):
    df = df.reset_index(drop=True).copy()
    if "label" not in df.columns:
        df["label"] = -1
    df["label"] = pd.to_numeric(df["label"], errors="coerce").fillna(-1)
    return df


def cmd_cv_innerval(a):
    m = load_module(a.script03b)
    dev = device_of()
    manifest = pd.read_csv(a.manifest, low_memory=False)
    manifest["_component_uid"] = (manifest["modality"].astype(str).str.lower()
                                  + "::component" + manifest["component_id"].astype(str))
    devset = manifest[manifest["split"].isin(["train", "val"])].copy()
    mdev = devset[devset["modality"].astype(str).str.lower().eq(a.modality)].copy().reset_index(drop=True)
    outer = m.make_outer_splits(mdev, m.SEED)
    _, eval_tf = m.transforms_for_run()
    ref = None
    if a.fold_assignment and Path(a.fold_assignment).exists():
        ref = pd.read_csv(a.fold_assignment)
        ref = ref[ref["modality"].astype(str).str.lower().eq(a.modality)]
    for fold, (tr_idx, ho_idx) in enumerate(outer, 1):
        fold_seed = m.SEED + fold * 100
        outer_train = mdev.iloc[tr_idx].reset_index(drop=True)
        hold = mdev.iloc[ho_idx]
        if ref is not None and len(ref):
            r = set(ref.loc[ref["outer_fold"].eq(fold), "image_path"])
            if r != set(hold["image_path"]):
                raise RuntimeError(f"{a.modality} fold {fold}: replicated holdout differs from fold_assignment.csv")
        _, iv_idx = m.make_inner_split(outer_train, fold_seed + 1)
        inner_val = outer_train.iloc[iv_idx].reset_index(drop=True)
        loader = m.make_loader(inner_val, eval_tf, a.batch_size, 0)
        for key in a.models:
            dst = Path(a.out) / a.modality / key / f"fold_{fold}_innerval_predictions.csv"
            if dst.exists():
                print("[skip]", dst, flush=True)
                continue
            ckpt = Path(a.cv_dir) / a.modality / key / f"fold_{fold}" / "best_model.pt"
            if not ckpt.exists():
                raise FileNotFoundError(ckpt)
            model = build_model(m, key, ckpt, dev)
            pred = m.predict(model, loader, inner_val, dev)
            thr = float(m.youden(pred["label"], pred["prob_malignant"]))
            out = pred[["image_path", "label", "source_group", "component_id", "prob_malignant"]].copy()
            out["outer_fold"] = fold
            out["model_key"] = key
            out["recomputed_threshold"] = thr
            dst.parent.mkdir(parents=True, exist_ok=True)
            out.to_csv(dst, index=False)
            print(f"{a.modality} fold {fold} {key}: inner-val n={len(out)} threshold={thr:.6f}", flush=True)
            free(model)


def cmd_check_folds(a):
    """Exit 0 if 03b in THIS environment reproduces the saved fold assignment exactly (both modalities), else exit 3."""
    import sklearn
    m = load_module(a.script03b)
    manifest = pd.read_csv(a.manifest, low_memory=False)
    manifest["_component_uid"] = (manifest["modality"].astype(str).str.lower()
                                  + "::component" + manifest["component_id"].astype(str))
    devset = manifest[manifest["split"].isin(["train", "val"])]
    ref = pd.read_csv(a.fold_assignment)
    report = {}
    for mo in ["ultrasound", "cytology"]:
        r = ref[ref["modality"].astype(str).str.lower().eq(mo)]
        if r.empty:
            continue
        mdev = devset[devset["modality"].astype(str).str.lower().eq(mo)].copy().reset_index(drop=True)
        outer = m.make_outer_splits(mdev, m.SEED)
        report[mo] = all(set(r.loc[r["outer_fold"].eq(f), "image_path"]) == set(mdev.iloc[h]["image_path"])
                         for f, (_, h) in enumerate(outer, 1))
    ok = bool(report) and all(report.values())
    print(json.dumps({"sklearn": sklearn.__version__, "folds_reproduced": report, "ok": ok}), flush=True)
    sys.exit(0 if ok else 3)


def cmd_predict(a):
    m = load_module(a.script03b)
    dev = device_of()
    df = with_labels(pd.read_csv(a.manifest))
    _, eval_tf = m.transforms_for_run()
    loader = m.make_loader(df, eval_tf, a.batch_size, 0)
    outdir = Path(a.out)
    outdir.mkdir(parents=True, exist_ok=True)
    for key in a.models:
        dst = outdir / f"{key}_predictions.csv"
        if dst.exists():
            print("[skip]", dst, flush=True)
            continue
        ckpt = Path(a.exp1b_dir) / a.modality / key / "best_model.pt"
        if not ckpt.exists():
            raise FileNotFoundError(ckpt)
        t0 = time.time()
        model = build_model(m, key, ckpt, dev)
        pred = m.predict(model, loader, df, dev)
        out = df.copy()
        out["prob_malignant"] = pred["prob_malignant"].values
        out["model_key"] = key
        out.to_csv(dst, index=False)
        print(f"{Path(a.manifest).name} {key}: n={len(out)} in {time.time() - t0:.0f}s", flush=True)
        free(model)


def cmd_embed(a):
    m = load_module(a.script03b)
    dev = device_of()
    df = with_labels(pd.read_csv(a.manifest))
    outdir = Path(a.out)
    outdir.mkdir(parents=True, exist_ok=True)
    ckpt = Path(a.exp1b_dir) / a.modality / a.model / "best_model.pt"
    model = build_model(m, a.model, ckpt, dev)
    model.reset_classifier(0)
    _, eval_tf = m.transforms_for_run()
    loader = m.make_loader(df, eval_tf, a.batch_size, 0)
    feats = None
    with torch.no_grad():
        for images, _, idx in loader:
            f = model(images.to(dev)).float().cpu().numpy()
            if feats is None:
                feats = np.zeros((len(df), f.shape[1]), np.float32)
            feats[idx.numpy()] = f
    np.save(outdir / "embeddings.npy", feats)
    df.to_csv(outdir / "embeddings_index.csv", index=False)
    print("embeddings:", feats.shape, flush=True)


def cmd_gradcam(a):
    m = load_module(a.script03b)
    dev = device_of()
    df = pd.read_csv(a.manifest).reset_index(drop=True)
    outdir = Path(a.out)
    outdir.mkdir(parents=True, exist_ok=True)
    ckpt = Path(a.exp1b_dir) / a.modality / a.model / "best_model.pt"
    model = build_model(m, a.model, ckpt, dev)
    modules = dict(model.named_modules())
    if a.layer not in modules:
        raise KeyError(f"layer {a.layer} not in model; candidates end with: {list(modules)[-8:]}")
    store = {}

    def hook(mod, inp, out):
        store["act"] = out
        out.register_hook(lambda g: store.__setitem__("grad", g))

    handle = modules[a.layer].register_forward_hook(hook)
    _, eval_tf = m.transforms_for_run()
    S = 224
    cams = np.zeros((len(df), S, S), np.float16)
    rows = []
    for i, r in df.iterrows():
        rec = {"image_path": r["image_path"]}
        try:
            with Image.open(r["image_path"]) as im:
                x = eval_tf(im.convert("RGB")).unsqueeze(0).to(dev)
            model.zero_grad(set_to_none=True)
            logit = model(x).reshape(-1)[0]
            logit.backward()
            A, G = store["act"].detach(), store["grad"].detach()
            cam = torch.relu((G.mean(dim=(2, 3), keepdim=True) * A).sum(1, keepdim=True))
            cam = torch.nn.functional.interpolate(cam.float(), size=(S, S), mode="bilinear", align_corners=False)[0, 0]
            cam = cam.cpu().numpy()
            X0, Y0 = int(r["box_x0"] * S), int(r["box_y0"] * S)
            X1, Y1 = int(np.ceil(r["box_x1"] * S)), int(np.ceil(r["box_y1"] * S))
            total = float(cam.sum())
            inside = float(cam[Y0:Y1, X0:X1].sum())
            py, px = np.unravel_index(int(cam.argmax()), cam.shape)
            rec.update(prob_malignant=float(torch.sigmoid(logit).item()),
                       cam_mass_outside_sector=(1 - inside / total) if total > 0 else np.nan,
                       sector_area_outside=1 - ((X1 - X0) * (Y1 - Y0)) / float(S * S),
                       peak_outside_sector=not (X0 <= px < X1 and Y0 <= py < Y1),
                       status="ok")
            cams[i] = (cam / cam.max() if cam.max() > 0 else cam).astype(np.float16)
        except Exception as e:
            rec.update(status=f"error: {e}")
        rows.append(rec)
    handle.remove()
    np.savez_compressed(outdir / "cams.npz", cams=cams)
    pd.DataFrame(rows).to_csv(outdir / "gradcam_per_image.csv", index=False)
    print("grad-cam images:", len(rows), "errors:", sum(1 for r in rows if r["status"] != "ok"), flush=True)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("cv-innerval")
    p.add_argument("--script03b", required=True); p.add_argument("--manifest", required=True)
    p.add_argument("--cv-dir", required=True); p.add_argument("--fold-assignment", default="")
    p.add_argument("--modality", required=True); p.add_argument("--models", nargs="+", required=True)
    p.add_argument("--out", required=True); p.add_argument("--batch-size", type=int, default=16)
    p = sub.add_parser("check-folds")
    p.add_argument("--script03b", required=True); p.add_argument("--manifest", required=True)
    p.add_argument("--fold-assignment", required=True)
    p = sub.add_parser("predict")
    p.add_argument("--script03b", required=True); p.add_argument("--manifest", required=True)
    p.add_argument("--exp1b-dir", required=True); p.add_argument("--modality", default="ultrasound")
    p.add_argument("--models", nargs="+", required=True); p.add_argument("--out", required=True)
    p.add_argument("--batch-size", type=int, default=16)
    p = sub.add_parser("embed")
    p.add_argument("--script03b", required=True); p.add_argument("--manifest", required=True)
    p.add_argument("--exp1b-dir", required=True); p.add_argument("--modality", default="ultrasound")
    p.add_argument("--model", default="efficientnet_b3"); p.add_argument("--out", required=True)
    p.add_argument("--batch-size", type=int, default=16)
    p = sub.add_parser("gradcam")
    p.add_argument("--script03b", required=True); p.add_argument("--manifest", required=True)
    p.add_argument("--exp1b-dir", required=True); p.add_argument("--modality", default="ultrasound")
    p.add_argument("--model", default="efficientnet_b3"); p.add_argument("--layer", default="conv_head")
    p.add_argument("--out", required=True)
    a = ap.parse_args()
    {"cv-innerval": cmd_cv_innerval, "check-folds": cmd_check_folds, "predict": cmd_predict, "embed": cmd_embed, "gradcam": cmd_gradcam}[a.cmd](a)


if __name__ == "__main__":
    main()
