# Model checkpoints

Checkpoints are too large for GitHub and are not stored in this repository.

- `checkpoint_sha256.csv` lists every checkpoint used in the manuscript (frozen split, grouped cross-validation folds, split-design and masking experiments) with its size, modification time and SHA-256, so any archived copy can be verified.
- The frozen-split checkpoints (five backbones × two modalities) used for all external evaluations are archived on Zenodo: [Zenodo DOI for checkpoints].

Each file is a PyTorch dictionary with `model_state_dict` for `timm.create_model(<name>, pretrained=False, num_classes=1)`; see `code/r2_gpu_tasks.py`, function `build_model`.
