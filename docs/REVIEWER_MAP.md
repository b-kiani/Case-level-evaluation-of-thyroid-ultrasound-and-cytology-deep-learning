# Where each reviewer request is answered

| Request | Manuscript | Repository files |
|---|---|---|
| TN3K population and labels (R2-1, R3-1, R6-6) | 3.8, 3.9, Table 14 | `manifests/external_TN3K_test.csv`, `manifests/external_TN3K_trainval.csv`, `predictions/external/TN3K_*_all_models.csv` |
| DDTI endpoint and TI-RADS field (R1-1, R2-7, R3-5, R5) | 3.8, Tables 6 and 15 | `manifests/external_DDTI_original.csv`, `predictions/external/DDTI_original_all_models.csv`, `results/tables/H0_ddti_tirads_distribution.csv` |
| Internal denominator and confusion matrices (R2-2, R3-4) | Tables 8–10 | `predictions/frozen_split/**`, `results/tables/F1_*.csv`, `F2_*.csv`, `F3_*.csv` |
| Case identifiers, patient-level split, previous 384-patient study (R1-2, R2-5, R3-2, R5, R6-1) | 3.1, 3.3, 4.6, Tables 1, 4, 17 | `manifests/04_frozen_manifest.csv` (+ `.sha256`), `manifests/05_*`, `manifests/06_*`, `results/tables/A7_prior_paper_reconciliation.csv` |
| Duplicates, label conflicts, pHash specification (R5, R6-3) | 3.2, Tables 2–3, Additional file 2 | `manifests/duplicate_groups_exact_md5.csv`, `manifests/phash_pairs_*.csv`, `manifests/01_excluded_cross_label_conflicts.csv`, `code/00c_*` |
| Fold-level results, fold assignment, threshold separation (R2-5) | 3.5, Table 7, Additional file 1 | `manifests/cv_fold_assignment.csv`, `predictions/grouped_cv/**`, `thresholds/grouped_cv_fold_thresholds.csv` |
| Ensemble construction (R2-4, R6-4) | 3.4, 3.9 | `code/02_*` (`build_ensemble`), `predictions/grouped_cv/*_all_models_oof.csv` |
| Split-design sensitivity analysis (R1-2, R4, R5) | 3.6, 4.3, Table 11, Fig. 4 | `code/03b_imagelevel_cv.py`, `predictions/imagelevel_cv/**` |
| Masking control (R5) | 3.7, 4.4, Tables 12–13, Figs 5–6 | `code/03b_shortcut_cv.py`, `predictions/shortcut_cv/**`, `results/figure_source_data/G2_gradcam_per_image.csv` |
| Cross-dataset overlap and distributions (R1-1, R1-3) | 4.5, Table 16, Fig. 8 | `results/tables/H1_*.csv`, `I1_mmd.csv`, `I2_image_statistics.csv`, `results/figure_source_data/I3_tsne_source.csv` |
| Calibration, ECE definition, thresholds (R2-6) | 3.10, 4.2, Table 10 | `results/tables/F3_temperature_scaling.csv`, `thresholds/*` |
| All backbones reported (R2-8, R5, R7-6) | Tables 7–9, 14–15 | `predictions/frozen_split/*/*`, `predictions/grouped_cv/*` |
| Head, input size, training recipe, class weighting (R2-8, R6-2, R6-9) | 3.4 | `code/02_*`, `environment/training_environment.json` |
| Reproducibility, versions, seeds, checkpoint identity (R3-3, R5, R6-7, R7-7) | Declarations | `environment/`, `requirements.txt`, `checkpoints/checkpoint_sha256.csv`, `code/Revision_Round2_Runs.ipynb` |
| Figures and source data (R5, R6-10, R7-2) | Figs 1–8 | `results/figures/`, `results/figure_source_data/` |
