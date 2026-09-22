# Round-2 revision results


## A1_archive: Pang archive as released (all files)

| modality   |   images |   benign_images |   ptc_images |   cases |   benign_cases |   ptc_cases |
|:-----------|---------:|----------------:|-------------:|--------:|---------------:|------------:|
| cytology   |     1332 |             635 |          697 |     384 |            165 |         219 |
| ultrasound |      387 |             165 |          222 |     387 |            165 |         222 |

- Cytology blocks per case: {2: 16, 3: 243, 4: 77, 5: 26, 6: 21, 7: 1} (mean 3.47); cases with both modalities: 384; ultrasound-only cases: ['PTC_0043', 'PTC_0112', 'PTC_0113']; case numbers reused across the two class folders: 165.


## A2_exact_duplicates: Exact (MD5) duplicate groups, including label conflicts

| modality   | conflict_type               | case_key   |   label | id                                                            | md5                              | may_split   | in_frozen_manifest   | frozen_split   |
|:-----------|:----------------------------|:-----------|--------:|:--------------------------------------------------------------|:---------------------------------|:------------|:---------------------|:---------------|
| cytology   | same label, different cases | PTC_0199   |       1 | cytological images of papillary thyroid carcinoma/199_001.tif | 2293d9cbc381e9b3b1797ecfaeacf66f | train       | True                 | train          |
| cytology   | same label, different cases | PTC_0201   |       1 | cytological images of papillary thyroid carcinoma/201_001.tif | 2293d9cbc381e9b3b1797ecfaeacf66f | train       | True                 | train          |
| cytology   | same label, different cases | BEN_0116   |       0 | cytological images of benign thyroid lesions/116_003.tif      | 3af2a01d518cbab3d1155aafcfe8c848 | train       | True                 | train          |
| cytology   | same label, different cases | BEN_0117   |       0 | cytological images of benign thyroid lesions/117_002.tif      | 3af2a01d518cbab3d1155aafcfe8c848 | train       | True                 | train          |
| cytology   | same label, different cases | PTC_0081   |       1 | cytological images of papillary thyroid carcinoma/81_002.tif  | af62e040024b7f5ed7575628992c9a06 | train       | True                 | train          |
| cytology   | same label, different cases | PTC_0082   |       1 | cytological images of papillary thyroid carcinoma/82_002.tif  | af62e040024b7f5ed7575628992c9a06 | train       | True                 | train          |
| cytology   | same label, different cases | PTC_0199   |       1 | cytological images of papillary thyroid carcinoma/199_003.tif | f4494ae13aa6cf0d76db7fd3ceddf401 | train       | True                 | train          |
| cytology   | same label, different cases | PTC_0201   |       1 | cytological images of papillary thyroid carcinoma/201_003.tif | f4494ae13aa6cf0d76db7fd3ceddf401 | train       | True                 | train          |
| ultrasound | cross-label                 | BEN_0039   |       0 | ultrasound images of benign thyroid lesions/39.jpg            | 2017d24c7ea7064164b107ed3b279ea7 | val         | False                | nan            |
| ultrasound | cross-label                 | PTC_0103   |       1 | ultrasound images of papillary thyroid carcinoma/103.jpg      | 2017d24c7ea7064164b107ed3b279ea7 | val         | False                | nan            |
| ultrasound | cross-label                 | BEN_0036   |       0 | ultrasound images of benign thyroid lesions/36.jpg            | 2ce2868b2042d681ed2ffedd6fa077d7 | val         | False                | nan            |
| ultrasound | cross-label                 | PTC_0093   |       1 | ultrasound images of papillary thyroid carcinoma/93.jpg       | 2ce2868b2042d681ed2ffedd6fa077d7 | val         | False                | nan            |
| ultrasound | cross-label                 | BEN_0003   |       0 | ultrasound images of benign thyroid lesions/3.jpg             | 5a252403dec58e49f8384225223900ea | train       | False                | nan            |
| ultrasound | cross-label                 | BEN_0055   |       0 | ultrasound images of benign thyroid lesions/55.jpg            | 5a252403dec58e49f8384225223900ea | train       | False                | nan            |
| ultrasound | cross-label                 | PTC_0139   |       1 | ultrasound images of papillary thyroid carcinoma/139.jpg      | 5a252403dec58e49f8384225223900ea | train       | False                | nan            |
| ultrasound | cross-label                 | BEN_0061   |       0 | ultrasound images of benign thyroid lesions/61.jpg            | 71164f281603d442bf5808a4febfd03c | train       | False                | nan            |
| ultrasound | cross-label                 | PTC_0160   |       1 | ultrasound images of papillary thyroid carcinoma/160.jpg      | 71164f281603d442bf5808a4febfd03c | train       | False                | nan            |
| ultrasound | cross-label                 | BEN_0044   |       0 | ultrasound images of benign thyroid lesions/44.jpg            | 83728c1b56f165f0024ed92aa2d4ca83 | test        | False                | nan            |
| ultrasound | cross-label                 | PTC_0112   |       1 | ultrasound images of papillary thyroid carcinoma/112.jpg      | 83728c1b56f165f0024ed92aa2d4ca83 | test        | False                | nan            |
| ultrasound | cross-label                 | BEN_0019   |       0 | ultrasound images of benign thyroid lesions/19.jpg            | 925e32aba60228a11330d17e00d26c52 | test        | False                | nan            |
| ultrasound | cross-label                 | PTC_0027   |       1 | ultrasound images of papillary thyroid carcinoma/27.jpg       | 925e32aba60228a11330d17e00d26c52 | test        | False                | nan            |
| ultrasound | cross-label                 | BEN_0025   |       0 | ultrasound images of benign thyroid lesions/25.jpg            | acef77b7e8e42fe3173fe0a7521e2e30 | train       | False                | nan            |
| ultrasound | cross-label                 | PTC_0044   |       1 | ultrasound images of papillary thyroid carcinoma/44.jpg       | acef77b7e8e42fe3173fe0a7521e2e30 | train       | False                | nan            |
| ultrasound | cross-label                 | BEN_0038   |       0 | ultrasound images of benign thyroid lesions/38.jpg            | b23899ff958e2e0777e17ea8d601e7d3 | train       | False                | nan            |
| ultrasound | cross-label                 | PTC_0099   |       1 | ultrasound images of papillary thyroid carcinoma/99.jpg       | b23899ff958e2e0777e17ea8d601e7d3 | train       | False                | nan            |
| ultrasound | cross-label                 | BEN_0020   |       0 | ultrasound images of benign thyroid lesions/20.jpg            | e8f7705cd05f793d14068efbae5fd71b | test        | False                | nan            |
| ultrasound | cross-label                 | PTC_0037   |       1 | ultrasound images of papillary thyroid carcinoma/37.jpg       | e8f7705cd05f793d14068efbae5fd71b | test        | False                | nan            |
| ultrasound | same label, different cases | PTC_0114   |       1 | ultrasound images of papillary thyroid carcinoma/114.jpg      | 1bfd41702c0e7e637950961a76ff6c9f | val         | True                 | val            |
| ultrasound | same label, different cases | PTC_0115   |       1 | ultrasound images of papillary thyroid carcinoma/115.jpg      | 1bfd41702c0e7e637950961a76ff6c9f | val         | True                 | val            |


## A2b_duplicate_summary: Duplicate groups by type

| modality   | conflict_type               |   groups |   images |   kept_in_frozen |
|:-----------|:----------------------------|---------:|---------:|-----------------:|
| cytology   | same label, different cases |        4 |        8 |                8 |
| ultrasound | cross-label                 |        9 |       19 |                0 |
| ultrasound | same label, different cases |        1 |        2 |                2 |


## A3_exclusions: Images excluded from the frozen manifest

| exclusion_reason                                                            |   images |
|:----------------------------------------------------------------------------|---------:|
| cross_label_exact_md5;cross_label_identical_phash;cross_label_leakage_group |       19 |
| cross_label_identical_phash;cross_label_leakage_group                       |        4 |


## A4_phash_sensitivity: Perceptual-hash (DCT pHash, 64-bit) near-duplicate pairs by Hamming threshold

The original pipeline grouped identical pHash values only (Hamming 0). Pairs crossing frozen partitions are listed for visual review.

| modality   |   hamming_max |   pairs |   cross_case |   cross_label |   cross_frozen_partition |
|:-----------|--------------:|--------:|-------------:|--------------:|-------------------------:|
| cytology   |             0 |       4 |            4 |             0 |                        0 |
| cytology   |             2 |       5 |            5 |             0 |                        1 |
| cytology   |             4 |       5 |            5 |             0 |                        1 |
| cytology   |             6 |       7 |            6 |             0 |                        1 |
| cytology   |             8 |       8 |            7 |             0 |                        1 |
| cytology   |            10 |       8 |            7 |             0 |                        1 |
| ultrasound |             0 |      14 |           14 |            12 |                        0 |
| ultrasound |             2 |      14 |           14 |            12 |                        0 |
| ultrasound |             4 |      21 |           21 |            15 |                        0 |
| ultrasound |             6 |      41 |           41 |            25 |                        9 |
| ultrasound |             8 |     184 |          184 |            69 |                       69 |
| ultrasound |            10 |     818 |          818 |           293 |                      355 |


## A5_leakage_original_split: Measured case-level leakage in the original image-level split (Tables 3–13 of the submitted manuscript)

| modality   | partition   |   images |   cases |   images_with_same_case_in_train |   cases_with_images_in_train |   cross_label_conflict_images |
|:-----------|:------------|---------:|--------:|---------------------------------:|-----------------------------:|------------------------------:|
| cytology   | val         |      200 |     160 |                            0.925 |                        0.944 |                             0 |
| cytology   | test        |      200 |     160 |                            0.89  |                        0.931 |                             0 |
| ultrasound | val         |       59 |      59 |                            0     |                        0     |                             4 |
| ultrasound | test        |       60 |      60 |                            0     |                        0     |                             6 |


## A6_original_image_level_results: Original (leaky, image-level) test results, recomputed from files

| model                      |   n |   auroc |   auprc |   brier |
|:---------------------------|----:|--------:|--------:|--------:|
| Cytology ConvNeXt-Small    | 200 |  0.9884 |  0.99   |  0.0296 |
| Cytology Ensemble (v2)     | 200 |  0.9862 |  0.9889 |  0.0307 |
| Cytology ConvNeXt-Tiny     | 200 |  0.9825 |  0.9879 |  0.0342 |
| Cytology Swin-Tiny         | 200 |  0.9797 |  0.9821 |  0.0446 |
| Cytology EfficientNet-B3   | 200 |  0.9755 |  0.9724 |  0.0617 |
| Ultrasound EfficientNet-B3 |  60 |  0.7449 |  0.8018 |  0.2647 |


## A7_prior_paper_reconciliation: Reconciliation with the published BMC Medical Imaging analysis

| item                                                                                 | value                                                                        |
|:-------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------|
| patients                                                                             | 384                                                                          |
| benign / PTC                                                                         | 165 / 219                                                                    |
| linkage                                                                              | class folder + case number (ultrasound <n>.jpg <-> cytology <n>_<block>.tif) |
| split                                                                                | {'development': 307, 'holdout': 77}                                          |
| patients carrying a cross-label duplicated ultrasound image                          | 18                                                                           |
| holdout patients whose ultrasound image is byte-identical to a development patient's | 4                                                                            |
| holdout patients involved                                                            | BEN_0038, BEN_0055, PTC_0027, PTC_0093                                       |


## A8_frozen_partitions: Frozen case-level partitions used for all new analyses

| modality   | split   |   images |   cases |   benign |   ptc |
|:-----------|:--------|---------:|--------:|---------:|------:|
| cytology   | test    |      214 |      58 |      102 |   112 |
| cytology   | train   |      907 |     269 |      427 |   480 |
| cytology   | val     |      211 |      57 |      106 |   105 |
| ultrasound | test    |       55 |      55 |       23 |    32 |
| ultrasound | train   |      254 |     254 |      107 |   147 |
| ultrasound | val     |       55 |      55 |       23 |    32 |


## F1_frozen_test_image_level: Frozen test set, image level; thresholds selected on validation; case-clustered 95% CIs

| modality   | model                | level   |   n |   benign |   ptc |   val_auroc | auroc               | auprc               |   no_skill_auprc |   threshold_from_val |   tn |   fp |   fn |   tp | sensitivity         | specificity         | accuracy            |    f1 |   brier |   ece15 |
|:-----------|:---------------------|:--------|----:|---------:|------:|------------:|:--------------------|:--------------------|-----------------:|---------------------:|-----:|-----:|-----:|-----:|:--------------------|:--------------------|:--------------------|------:|--------:|--------:|
| ultrasound | ConvNeXt-Small       | image   |  55 |       23 |    32 |       0.628 | 0.736 (0.595–0.864) | 0.829 (0.701–0.925) |            0.582 |               0.4721 |   18 |    5 |   11 |   21 | 0.656 (0.484–0.816) | 0.783 (0.593–0.947) | 0.709 (0.582–0.818) | 0.724 |   0.255 |   0.11  |
| ultrasound | EfficientNet-B3      | image   |  55 |       23 |    32 |       0.792 | 0.859 (0.745–0.952) | 0.857 (0.714–0.972) |            0.582 |               0.0062 |   16 |    7 |    4 |   28 | 0.875 (0.742–0.971) | 0.696 (0.500–0.875) | 0.800 (0.691–0.891) | 0.836 |   0.214 |   0.244 |
| ultrasound | Swin-Tiny            | image   |  55 |       23 |    32 |       0.655 | 0.735 (0.589–0.868) | 0.758 (0.602–0.922) |            0.582 |               0.4198 |   21 |    2 |   20 |   12 | 0.375 (0.212–0.543) | 0.913 (0.789–1.000) | 0.600 (0.473–0.727) | 0.522 |   0.268 |   0.225 |
| ultrasound | ResNet-50            | image   |  55 |       23 |    32 |       0.855 | 0.827 (0.696–0.930) | 0.871 (0.758–0.955) |            0.582 |               0.144  |   17 |    6 |   11 |   21 | 0.656 (0.485–0.812) | 0.739 (0.542–0.909) | 0.691 (0.564–0.800) | 0.712 |   0.396 |   0.439 |
| ultrasound | DenseNet-121         | image   |  55 |       23 |    32 |       0.81  | 0.852 (0.740–0.942) | 0.887 (0.784–0.965) |            0.582 |               0.3966 |   20 |    3 |   14 |   18 | 0.562 (0.393–0.731) | 0.870 (0.714–1.000) | 0.691 (0.564–0.800) | 0.679 |   0.246 |   0.292 |
| ultrasound | Ensemble (mean of 5) | image   |  55 |       23 |    32 |       0.842 | 0.909 (0.811–0.978) | 0.918 (0.810–0.987) |            0.582 |               0.3507 |   21 |    2 |   10 |   22 | 0.688 (0.519–0.846) | 0.913 (0.782–1.000) | 0.782 (0.673–0.891) | 0.786 |   0.223 |   0.289 |
| cytology   | ConvNeXt-Small       | image   | 214 |      102 |   112 |       0.968 | 0.984 (0.966–0.996) | 0.985 (0.966–0.997) |            0.523 |               0.3789 |   93 |    9 |    7 |  105 | 0.938 (0.893–0.974) | 0.912 (0.836–0.973) | 0.925 (0.886–0.962) | 0.929 |   0.061 |   0.096 |
| cytology   | EfficientNet-B3      | image   | 214 |      102 |   112 |       0.988 | 0.990 (0.978–0.998) | 0.991 (0.978–0.999) |            0.523 |               0.5993 |  100 |    2 |   17 |   95 | 0.848 (0.753–0.935) | 0.980 (0.951–1.000) | 0.911 (0.854–0.959) | 0.909 |   0.065 |   0.072 |
| cytology   | Swin-Tiny            | image   | 214 |      102 |   112 |       0.989 | 0.995 (0.985–1.000) | 0.995 (0.987–1.000) |            0.523 |               0.4947 |   99 |    3 |    9 |  103 | 0.920 (0.830–0.991) | 0.971 (0.924–1.000) | 0.944 (0.891–0.986) | 0.945 |   0.037 |   0.087 |
| cytology   | ResNet-50            | image   | 214 |      102 |   112 |       0.989 | 0.997 (0.991–1.000) | 0.997 (0.992–1.000) |            0.523 |               0.8486 |  102 |    0 |   15 |   97 | 0.866 (0.759–0.957) | 1.000 (1.000–1.000) | 0.930 (0.867–0.978) | 0.928 |   0.028 |   0.043 |
| cytology   | DenseNet-121         | image   | 214 |      102 |   112 |       0.99  | 0.982 (0.959–0.997) | 0.987 (0.969–0.997) |            0.523 |               0.1767 |   97 |    5 |    9 |  103 | 0.920 (0.850–0.976) | 0.951 (0.884–1.000) | 0.935 (0.888–0.975) | 0.936 |   0.061 |   0.07  |
| cytology   | Ensemble (mean of 5) | image   | 214 |      102 |   112 |       0.992 | 0.996 (0.990–1.000) | 0.996 (0.990–1.000) |            0.523 |               0.5924 |  102 |    0 |   13 |   99 | 0.884 (0.788–0.965) | 1.000 (1.000–1.000) | 0.939 (0.885–0.982) | 0.938 |   0.038 |   0.074 |


## F2_frozen_test_case_level: Frozen test set, case level (images aggregated per case); thresholds from validation

| modality   | model                | level   |   n |   benign |   ptc |   val_auroc | auroc               | auprc               |   no_skill_auprc |   threshold_from_val |   tn |   fp |   fn |   tp | sensitivity         | specificity         | accuracy            |    f1 |   brier |   ece15 |
|:-----------|:---------------------|:--------|----:|---------:|------:|------------:|:--------------------|:--------------------|-----------------:|---------------------:|-----:|-----:|-----:|-----:|:--------------------|:--------------------|:--------------------|------:|--------:|--------:|
| ultrasound | ConvNeXt-Small       | case    |  55 |       23 |    32 |       0.628 | 0.736 (0.595–0.864) | 0.829 (0.701–0.925) |            0.582 |               0.4721 |   18 |    5 |   11 |   21 | 0.656 (0.484–0.816) | 0.783 (0.593–0.947) | 0.709 (0.582–0.818) | 0.724 |   0.255 |   0.11  |
| ultrasound | EfficientNet-B3      | case    |  55 |       23 |    32 |       0.792 | 0.859 (0.745–0.952) | 0.857 (0.714–0.972) |            0.582 |               0.0062 |   16 |    7 |    4 |   28 | 0.875 (0.742–0.971) | 0.696 (0.500–0.875) | 0.800 (0.691–0.891) | 0.836 |   0.214 |   0.244 |
| ultrasound | Swin-Tiny            | case    |  55 |       23 |    32 |       0.655 | 0.735 (0.589–0.868) | 0.758 (0.602–0.922) |            0.582 |               0.4198 |   21 |    2 |   20 |   12 | 0.375 (0.212–0.543) | 0.913 (0.789–1.000) | 0.600 (0.473–0.727) | 0.522 |   0.268 |   0.225 |
| ultrasound | ResNet-50            | case    |  55 |       23 |    32 |       0.855 | 0.827 (0.696–0.930) | 0.871 (0.758–0.955) |            0.582 |               0.144  |   17 |    6 |   11 |   21 | 0.656 (0.485–0.812) | 0.739 (0.542–0.909) | 0.691 (0.564–0.800) | 0.712 |   0.396 |   0.439 |
| ultrasound | DenseNet-121         | case    |  55 |       23 |    32 |       0.81  | 0.852 (0.740–0.942) | 0.887 (0.784–0.965) |            0.582 |               0.3966 |   20 |    3 |   14 |   18 | 0.562 (0.393–0.731) | 0.870 (0.714–1.000) | 0.691 (0.564–0.800) | 0.679 |   0.246 |   0.292 |
| ultrasound | Ensemble (mean of 5) | case    |  55 |       23 |    32 |       0.842 | 0.909 (0.811–0.978) | 0.918 (0.810–0.987) |            0.582 |               0.3507 |   21 |    2 |   10 |   22 | 0.688 (0.519–0.846) | 0.913 (0.782–1.000) | 0.782 (0.673–0.891) | 0.786 |   0.223 |   0.289 |
| cytology   | ConvNeXt-Small       | case    |  58 |       25 |    33 |       0.962 | 0.998 (0.989–1.000) | 0.998 (0.992–1.000) |            0.569 |               0.4685 |   23 |    2 |    1 |   32 | 0.970 (0.900–1.000) | 0.920 (0.800–1.000) | 0.948 (0.896–1.000) | 0.955 |   0.052 |   0.175 |
| cytology   | EfficientNet-B3      | case    |  58 |       25 |    33 |       0.997 | 0.999 (0.993–1.000) | 0.999 (0.995–1.000) |            0.569 |               0.6178 |   25 |    0 |    5 |   28 | 0.848 (0.719–0.967) | 1.000 (1.000–1.000) | 0.914 (0.845–0.983) | 0.918 |   0.041 |   0.075 |
| cytology   | Swin-Tiny            | case    |  58 |       25 |    33 |       0.991 | 0.999 (0.993–1.000) | 0.999 (0.995–1.000) |            0.569 |               0.6461 |   25 |    0 |    2 |   31 | 0.939 (0.850–1.000) | 1.000 (1.000–1.000) | 0.966 (0.914–1.000) | 0.969 |   0.03  |   0.107 |
| cytology   | ResNet-50            | case    |  58 |       25 |    33 |       0.994 | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) |            0.569 |               0.6653 |   25 |    0 |    2 |   31 | 0.939 (0.846–1.000) | 1.000 (1.000–1.000) | 0.966 (0.914–1.000) | 0.969 |   0.018 |   0.049 |
| cytology   | DenseNet-121         | case    |  58 |       25 |    33 |       0.996 | 0.999 (0.993–1.000) | 0.999 (0.995–1.000) |            0.569 |               0.609  |   25 |    0 |    5 |   28 | 0.848 (0.714–0.960) | 1.000 (1.000–1.000) | 0.914 (0.828–0.983) | 0.918 |   0.044 |   0.089 |
| cytology   | Ensemble (mean of 5) | case    |  58 |       25 |    33 |       0.995 | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) |            0.569 |               0.5433 |   25 |    0 |    2 |   31 | 0.939 (0.850–1.000) | 1.000 (1.000–1.000) | 0.966 (0.914–1.000) | 0.969 |   0.03  |   0.106 |


## F3_temperature_scaling: Temperature scaling fitted on validation; test ECE (15 equal-width bins) and decisions

Temperature scaling is monotone: re-selecting the threshold on validation after scaling leaves every decision unchanged; reusing the old numeric threshold does not.

| modality   | model                | temperature                                    |   test_ece_before |   test_ece_after |   test_brier_before |   test_brier_after |   accuracy_original |   accuracy_scaled_same_numeric_threshold |   accuracy_scaled_threshold_reselected_on_val | decisions_identical_after_reselection   |
|:-----------|:---------------------|:-----------------------------------------------|------------------:|-----------------:|--------------------:|-------------------:|--------------------:|-----------------------------------------:|----------------------------------------------:|:----------------------------------------|
| ultrasound | ConvNeXt-Small       | >100 (search bound; near-uninformative logits) |             0.11  |            0.082 |               0.255 |              0.25  |               0.709 |                                    0.582 |                                         0.709 | True                                    |
| ultrasound | EfficientNet-B3      | 8.186                                          |             0.244 |            0.245 |               0.214 |              0.185 |               0.8   |                                    0.582 |                                         0.8   | True                                    |
| ultrasound | Swin-Tiny            | >100 (search bound; near-uninformative logits) |             0.225 |            0.083 |               0.268 |              0.25  |               0.6   |                                    0.582 |                                         0.6   | True                                    |
| ultrasound | ResNet-50            | 8.598                                          |             0.439 |            0.211 |               0.396 |              0.249 |               0.691 |                                    0.582 |                                         0.691 | True                                    |
| ultrasound | DenseNet-121         | 3.125                                          |             0.292 |            0.229 |               0.246 |              0.201 |               0.691 |                                    0.709 |                                         0.691 | True                                    |
| ultrasound | Ensemble (mean of 5) | 1.499                                          |             0.289 |            0.285 |               0.223 |              0.22  |               0.782 |                                    0.836 |                                         0.782 | True                                    |
| cytology   | ConvNeXt-Small       | 0.711                                          |             0.096 |            0.06  |               0.061 |              0.056 |               0.925 |                                    0.921 |                                         0.925 | True                                    |
| cytology   | EfficientNet-B3      | 2.635                                          |             0.072 |            0.066 |               0.065 |              0.055 |               0.911 |                                    0.907 |                                         0.911 | True                                    |
| cytology   | Swin-Tiny            | 0.74                                           |             0.087 |            0.065 |               0.037 |              0.034 |               0.944 |                                    0.944 |                                         0.944 | True                                    |
| cytology   | ResNet-50            | 1.98                                           |             0.043 |            0.049 |               0.028 |              0.029 |               0.93  |                                    0.897 |                                         0.93  | True                                    |
| cytology   | DenseNet-121         | 1.264                                          |             0.07  |            0.071 |               0.061 |              0.06  |               0.935 |                                    0.939 |                                         0.935 | True                                    |
| cytology   | Ensemble (mean of 5) | 0.7                                            |             0.074 |            0.058 |               0.038 |              0.037 |               0.939 |                                    0.939 |                                         0.939 | True                                    |

- Sector box detection on 110 ultrasound val/test images: {'detected': 78, 'fallback': 32}.


## G1_gradcam_attribution: Grad-CAM mass outside the detected ultrasound sector (EfficientNet-B3, val+test)

Expected mass under spatially uniform attribution equals the area outside the sector.

| outcome   |   images |   mean_cam_mass_outside_sector |   median_cam_mass_outside_sector |   mean_area_outside_sector |   share_peak_outside_sector |
|:----------|---------:|-------------------------------:|---------------------------------:|---------------------------:|----------------------------:|
| FN        |       10 |                          0.517 |                            0.549 |                      0.53  |                       0.5   |
| FP        |       15 |                          0.472 |                            0.395 |                      0.538 |                       0.467 |
| TN        |       31 |                          0.554 |                            0.501 |                      0.423 |                       0.71  |
| TP        |       54 |                          0.323 |                            0.246 |                      0.467 |                       0.204 |
| ALL       |      110 |                          0.426 |                            0.375 |                      0.47  |                       0.409 |


## I1_mmd: Maximum mean discrepancy between cohorts (EfficientNet-B3 features, PCA-50, RBF kernel, 500 permutations)

| comparison                          |   mmd2 |   permutation_p |
|:------------------------------------|-------:|----------------:|
| Pang train vs Pang test (reference) | 0.0159 |          0.1637 |


## I2_image_statistics: Acquisition-level image statistics by cohort

| cohort          |   images |   median_width |   median_height |   mean_intensity |   mean_contrast_sd |   share_near_black |
|:----------------|---------:|---------------:|----------------:|-----------------:|-------------------:|-------------------:|
| Pang (internal) |      364 |           1346 |             759 |             33.1 |               37.7 |              0.474 |

- Fold check: saved August folds reproduced exactly; August ConvNeXt-Small run reused.  
  `{"sklearn": "1.7.2", "folds_reproduced": {"ultrasound": true, "cytology": true}, "ok": true}`


## B1_cv_summary_from_03b: Grouped 5-fold CV summaries written by 03b

| modality   | model_key       | model           |   n_outer_folds |   development_images |   development_source_groups |   development_components |   fold_auroc_mean |   fold_auroc_sd |   fold_auprc_mean |   fold_auprc_sd |   pooled_oof_image_auroc |   pooled_oof_image_auprc |   pooled_oof_source_group_auroc |   pooled_oof_source_group_auprc |
|:-----------|:----------------|:----------------|----------------:|---------------------:|----------------------------:|-------------------------:|------------------:|----------------:|------------------:|----------------:|-------------------------:|-------------------------:|--------------------------------:|--------------------------------:|
| ultrasound | convnext_small  | ConvNeXt-Small  |               5 |                  309 |                         309 |                      308 |            0.644  |          0.1019 |            0.7219 |          0.09   |                   0.5277 |                   0.6275 |                          0.5277 |                          0.6275 |
| ultrasound | efficientnet_b3 | EfficientNet-B3 |               5 |                  309 |                         309 |                      308 |            0.7002 |          0.0797 |            0.7711 |          0.0513 |                   0.7066 |                   0.7672 |                          0.7066 |                          0.7672 |
| ultrasound | swin_tiny       | Swin-Tiny       |               5 |                  309 |                         309 |                      308 |            0.6123 |          0.0662 |            0.6815 |          0.0623 |                   0.5884 |                   0.653  |                          0.5884 |                          0.653  |
| ultrasound | resnet50        | ResNet50        |               5 |                  309 |                         309 |                      308 |            0.7429 |          0.0844 |            0.7964 |          0.0648 |                   0.7211 |                   0.7672 |                          0.7211 |                          0.7672 |
| ultrasound | densenet121     | DenseNet121     |               5 |                  309 |                         309 |                      308 |            0.796  |          0.0482 |            0.8382 |          0.0282 |                   0.7765 |                   0.8079 |                          0.7765 |                          0.8079 |
| cytology   | convnext_small  | ConvNeXt-Small  |               5 |                 1118 |                         326 |                      323 |            0.872  |          0.0711 |            0.88   |          0.0602 |                   0.8676 |                   0.8583 |                          0.8751 |                          0.8822 |
| cytology   | efficientnet_b3 | EfficientNet-B3 |               5 |                 1118 |                         326 |                      323 |            0.9595 |          0.0231 |            0.9566 |          0.0278 |                   0.9544 |                   0.9512 |                          0.9687 |                          0.9726 |
| cytology   | swin_tiny       | Swin-Tiny       |               5 |                 1118 |                         326 |                      323 |            0.963  |          0.0266 |            0.9639 |          0.0288 |                   0.9504 |                   0.9446 |                          0.9663 |                          0.9712 |
| cytology   | resnet50        | ResNet50        |               5 |                 1118 |                         326 |                      323 |            0.9581 |          0.0266 |            0.9627 |          0.0239 |                   0.9564 |                   0.9613 |                          0.968  |                          0.974  |
| cytology   | densenet121     | DenseNet121     |               5 |                 1118 |                         326 |                      323 |            0.9566 |          0.026  |            0.959  |          0.0298 |                   0.9481 |                   0.9485 |                          0.9678 |                          0.9748 |


## C1_cv_summary: Grouped 5-fold CV on the development set (train+val); frozen test untouched

Groups = duplicate-connected case components. Fold thresholds are Youden points on each fold's inner validation split; pooled OOF CIs resample components. within_cv_case_leakage = share of holdout images whose case appears in training folds.

| modality   | model                |   dev_images |   dev_cases | fold_auroc_mean_sd   | fold_auroc_range   | fold_auprc_mean_sd   | pooled_oof_auroc    | pooled_oof_auprc    |   pooled_brier |   pooled_ece15 |   sensitivity_at_fold_thresholds |   specificity_at_fold_thresholds |   within_cv_case_leakage |
|:-----------|:---------------------|-------------:|------------:|:---------------------|:-------------------|:---------------------|:--------------------|:--------------------|---------------:|---------------:|---------------------------------:|---------------------------------:|-------------------------:|
| ultrasound | ConvNeXt-Small       |          309 |         309 | 0.644 ± 0.102        | 0.508–0.758        | 0.722 ± 0.090        | 0.528 (0.463–0.595) | 0.627 (0.553–0.708) |          0.288 |          0.203 |                            0.464 |                            0.723 |                        0 |
| ultrasound | EfficientNet-B3      |          309 |         309 | 0.700 ± 0.080        | 0.584–0.800        | 0.771 ± 0.051        | 0.707 (0.647–0.764) | 0.767 (0.703–0.824) |          0.328 |          0.323 |                            0.715 |                            0.554 |                        0 |
| ultrasound | Swin-Tiny            |          309 |         309 | 0.612 ± 0.066        | 0.529–0.681        | 0.682 ± 0.062        | 0.588 (0.522–0.656) | 0.653 (0.580–0.734) |          0.259 |          0.148 |                            0.419 |                            0.738 |                        0 |
| ultrasound | ResNet-50            |          309 |         309 | 0.743 ± 0.084        | 0.604–0.833        | 0.796 ± 0.065        | 0.721 (0.664–0.777) | 0.767 (0.704–0.825) |          0.234 |          0.176 |                            0.682 |                            0.623 |                        0 |
| ultrasound | DenseNet-121         |          309 |         309 | 0.796 ± 0.048        | 0.716–0.840        | 0.838 ± 0.028        | 0.776 (0.725–0.825) | 0.808 (0.746–0.866) |          0.219 |          0.165 |                            0.693 |                            0.7   |                        0 |
| ultrasound | Ensemble (mean of 5) |          309 |         309 | 0.763 ± 0.094        | 0.599–0.829        | 0.822 ± 0.063        | 0.768 (0.716–0.819) | 0.809 (0.750–0.866) |          0.202 |          0.115 |                            0.709 |                            0.646 |                        0 |
| cytology   | ConvNeXt-Small       |         1118 |         326 | 0.872 ± 0.071        | 0.800–0.953        | 0.880 ± 0.060        | 0.868 (0.833–0.898) | 0.858 (0.810–0.904) |          0.153 |          0.041 |                            0.844 |                            0.75  |                        0 |
| cytology   | EfficientNet-B3      |         1118 |         326 | 0.960 ± 0.023        | 0.929–0.988        | 0.957 ± 0.028        | 0.954 (0.936–0.970) | 0.951 (0.927–0.971) |          0.088 |          0.081 |                            0.92  |                            0.882 |                        0 |
| cytology   | Swin-Tiny            |         1118 |         326 | 0.963 ± 0.027        | 0.935–0.998        | 0.964 ± 0.029        | 0.950 (0.929–0.969) | 0.945 (0.911–0.971) |          0.079 |          0.043 |                            0.899 |                            0.891 |                        0 |
| cytology   | ResNet-50            |         1118 |         326 | 0.958 ± 0.027        | 0.931–0.996        | 0.963 ± 0.024        | 0.956 (0.938–0.971) | 0.961 (0.944–0.976) |          0.079 |          0.034 |                            0.921 |                            0.876 |                        0 |
| cytology   | DenseNet-121         |         1118 |         326 | 0.957 ± 0.026        | 0.924–0.990        | 0.959 ± 0.030        | 0.948 (0.929–0.966) | 0.949 (0.922–0.969) |          0.087 |          0.065 |                            0.889 |                            0.887 |                        0 |
| cytology   | Ensemble (mean of 5) |         1118 |         326 | 0.964 ± 0.028        | 0.933–0.996        | 0.966 ± 0.029        | 0.958 (0.938–0.975) | 0.956 (0.928–0.977) |          0.069 |          0.045 |                            0.944 |                            0.886 |                        0 |


## C2_cv_fold_level: Fold-level results (all backbones and ensemble)

| modality   | model                |   fold |   n |   cases |   auroc |   auprc |   threshold_inner_val |   sensitivity |   specificity |   brier |
|:-----------|:---------------------|-------:|----:|--------:|--------:|--------:|----------------------:|--------------:|--------------:|--------:|
| ultrasound | ConvNeXt-Small       |      1 |  62 |      62 |  0.5085 |  0.604  |                0.3135 |         0.389 |         0.692 |  0.3149 |
| ultrasound | ConvNeXt-Small       |      2 |  63 |      63 |  0.5717 |  0.7309 |                0.4692 |         0.4   |         0.696 |  0.2596 |
| ultrasound | ConvNeXt-Small       |      3 |  61 |      61 |  0.7064 |  0.7076 |                0.3828 |         0.971 |         0.296 |  0.2772 |
| ultrasound | ConvNeXt-Small       |      4 |  61 |      61 |  0.7584 |  0.8563 |                0.3057 |         0.27  |         1     |  0.3291 |
| ultrasound | ConvNeXt-Small       |      5 |  62 |      62 |  0.675  |  0.7109 |                0.4073 |         0.312 |         0.933 |  0.2615 |
| ultrasound | EfficientNet-B3      |      1 |  62 |      62 |  0.8002 |  0.8484 |                0.0051 |         0.806 |         0.654 |  0.3245 |
| ultrasound | EfficientNet-B3      |      2 |  63 |      63 |  0.5837 |  0.7507 |                0.6974 |         0.625 |         0.435 |  0.4104 |
| ultrasound | EfficientNet-B3      |      3 |  61 |      61 |  0.7326 |  0.7561 |                0.9934 |         0.471 |         0.741 |  0.2678 |
| ultrasound | EfficientNet-B3      |      4 |  61 |      61 |  0.7106 |  0.789  |                0.2248 |         0.757 |         0.583 |  0.2879 |
| ultrasound | EfficientNet-B3      |      5 |  62 |      62 |  0.674  |  0.7111 |                0.0129 |         0.938 |         0.367 |  0.345  |
| ultrasound | Swin-Tiny            |      1 |  62 |      62 |  0.5288 |  0.5984 |                0.5155 |         0.306 |         0.654 |  0.2497 |
| ultrasound | Swin-Tiny            |      2 |  63 |      63 |  0.5685 |  0.7215 |                0.5982 |         0.475 |         0.696 |  0.2466 |
| ultrasound | Swin-Tiny            |      3 |  61 |      61 |  0.6808 |  0.7554 |                0.3256 |         0.412 |         0.889 |  0.3004 |
| ultrasound | Swin-Tiny            |      4 |  61 |      61 |  0.6081 |  0.6425 |                0.4551 |         0.324 |         0.75  |  0.2588 |
| ultrasound | Swin-Tiny            |      5 |  62 |      62 |  0.675  |  0.6899 |                0.5037 |         0.594 |         0.7   |  0.2407 |
| ultrasound | ResNet-50            |      1 |  62 |      62 |  0.7682 |  0.8388 |                0.4076 |         0.639 |         0.731 |  0.2302 |
| ultrasound | ResNet-50            |      2 |  63 |      63 |  0.6043 |  0.7291 |                0.3685 |         0.7   |         0.435 |  0.2924 |
| ultrasound | ResNet-50            |      3 |  61 |      61 |  0.744  |  0.7229 |                0.5902 |         0.588 |         0.778 |  0.2204 |
| ultrasound | ResNet-50            |      4 |  61 |      61 |  0.7646 |  0.8566 |                0.9531 |         0.595 |         0.75  |  0.2417 |
| ultrasound | ResNet-50            |      5 |  62 |      62 |  0.8333 |  0.8347 |                0.0926 |         0.906 |         0.433 |  0.1849 |
| ultrasound | DenseNet-121         |      1 |  62 |      62 |  0.8397 |  0.8785 |                0.533  |         0.611 |         0.885 |  0.2154 |
| ultrasound | DenseNet-121         |      2 |  63 |      63 |  0.7163 |  0.8108 |                0.9834 |         0.45  |         0.826 |  0.2367 |
| ultrasound | DenseNet-121         |      3 |  61 |      61 |  0.8039 |  0.8285 |                0.5421 |         0.735 |         0.63  |  0.1936 |
| ultrasound | DenseNet-121         |      4 |  61 |      61 |  0.7928 |  0.8177 |                0.1268 |         0.892 |         0.542 |  0.2649 |
| ultrasound | DenseNet-121         |      5 |  62 |      62 |  0.8271 |  0.8554 |                0.3156 |         0.812 |         0.633 |  0.1822 |
| ultrasound | Ensemble (mean of 5) |      1 |  62 |      62 |  0.7959 |  0.8513 |                0.3643 |         0.75  |         0.769 |  0.2144 |
| ultrasound | Ensemble (mean of 5) |      2 |  63 |      63 |  0.5989 |  0.7104 |                0.6206 |         0.5   |         0.652 |  0.2278 |
| ultrasound | Ensemble (mean of 5) |      3 |  61 |      61 |  0.8094 |  0.8556 |                0.4991 |         0.706 |         0.704 |  0.1884 |
| ultrasound | Ensemble (mean of 5) |      4 |  61 |      61 |  0.7838 |  0.8354 |                0.4836 |         0.73  |         0.667 |  0.2009 |
| ultrasound | Ensemble (mean of 5) |      5 |  62 |      62 |  0.8292 |  0.8581 |                0.357  |         0.906 |         0.467 |  0.1802 |
| cytology   | ConvNeXt-Small       |      1 | 217 |      64 |  0.9534 |  0.9528 |                0.5276 |         0.85  |         0.927 |  0.0918 |
| cytology   | ConvNeXt-Small       |      2 | 223 |      65 |  0.8006 |  0.8393 |                0.5702 |         0.767 |         0.65  |  0.2433 |
| cytology   | ConvNeXt-Small       |      3 | 216 |      65 |  0.8001 |  0.8212 |                0.3048 |         0.759 |         0.712 |  0.1876 |
| cytology   | ConvNeXt-Small       |      4 | 224 |      65 |  0.9298 |  0.9364 |                0.2497 |         0.927 |         0.74  |  0.103  |
| cytology   | ConvNeXt-Small       |      5 | 238 |      67 |  0.8763 |  0.8504 |                0.5902 |         0.91  |         0.716 |  0.1407 |
| cytology   | EfficientNet-B3      |      1 | 217 |      64 |  0.9551 |  0.9479 |                0.0162 |         0.963 |         0.809 |  0.097  |
| cytology   | EfficientNet-B3      |      2 | 223 |      65 |  0.9882 |  0.991  |                0.8934 |         0.908 |         0.99  |  0.0435 |
| cytology   | EfficientNet-B3      |      3 | 216 |      65 |  0.9288 |  0.9257 |                0.6218 |         0.866 |         0.894 |  0.1064 |
| cytology   | EfficientNet-B3      |      4 | 224 |      65 |  0.9757 |  0.9799 |                0.2237 |         0.919 |         0.9   |  0.0841 |
| cytology   | EfficientNet-B3      |      5 | 238 |      67 |  0.9498 |  0.9385 |                0.9314 |         0.943 |         0.828 |  0.1084 |
| cytology   | Swin-Tiny            |      1 | 217 |      64 |  0.9834 |  0.9837 |                0.6432 |         0.935 |         0.909 |  0.0647 |
| cytology   | Swin-Tiny            |      2 | 223 |      65 |  0.9975 |  0.998  |                0.9156 |         0.85  |         1     |  0.0211 |
| cytology   | Swin-Tiny            |      3 | 216 |      65 |  0.9434 |  0.9471 |                0.4394 |         0.875 |         0.913 |  0.0917 |
| cytology   | Swin-Tiny            |      4 | 224 |      65 |  0.9557 |  0.9651 |                0.1015 |         0.887 |         0.87  |  0.1138 |
| cytology   | Swin-Tiny            |      5 | 238 |      67 |  0.9349 |  0.9255 |                0.4225 |         0.951 |         0.776 |  0.1009 |
| cytology   | ResNet-50            |      1 | 217 |      64 |  0.9734 |  0.9758 |                0.4239 |         0.925 |         0.891 |  0.0668 |
| cytology   | ResNet-50            |      2 | 223 |      65 |  0.9964 |  0.997  |                0.7685 |         0.933 |         0.99  |  0.0233 |
| cytology   | ResNet-50            |      3 | 216 |      65 |  0.9311 |  0.937  |                0.308  |         0.893 |         0.865 |  0.1157 |
| cytology   | ResNet-50            |      4 | 224 |      65 |  0.9402 |  0.9478 |                0.3448 |         0.935 |         0.79  |  0.0888 |
| cytology   | ResNet-50            |      5 | 238 |      67 |  0.9495 |  0.9559 |                0.6778 |         0.918 |         0.845 |  0.1016 |
| cytology   | DenseNet-121         |      1 | 217 |      64 |  0.9633 |  0.9689 |                0.4758 |         0.879 |         0.9   |  0.0766 |
| cytology   | DenseNet-121         |      2 | 223 |      65 |  0.9895 |  0.9915 |                0.816  |         0.875 |         0.971 |  0.039  |
| cytology   | DenseNet-121         |      3 | 216 |      65 |  0.9372 |  0.9388 |                0.5787 |         0.839 |         0.933 |  0.0983 |
| cytology   | DenseNet-121         |      4 | 224 |      65 |  0.9688 |  0.9776 |                0.7419 |         0.919 |         0.9   |  0.0709 |
| cytology   | DenseNet-121         |      5 | 238 |      67 |  0.9241 |  0.9184 |                0.7091 |         0.926 |         0.75  |  0.145  |
| cytology   | Ensemble (mean of 5) |      1 | 217 |      64 |  0.9822 |  0.9842 |                0.3089 |         0.972 |         0.827 |  0.0548 |
| cytology   | Ensemble (mean of 5) |      2 | 223 |      65 |  0.9964 |  0.9972 |                0.6915 |         0.942 |         1     |  0.0329 |
| cytology   | Ensemble (mean of 5) |      3 | 216 |      65 |  0.9328 |  0.9431 |                0.4424 |         0.902 |         0.904 |  0.093  |
| cytology   | Ensemble (mean of 5) |      4 | 224 |      65 |  0.9719 |  0.978  |                0.4036 |         0.944 |         0.91  |  0.0648 |
| cytology   | Ensemble (mean of 5) |      5 | 238 |      67 |  0.9361 |  0.9274 |                0.5232 |         0.959 |         0.802 |  0.0957 |


## C3_threshold_reproducibility: Inner-validation thresholds recomputed from checkpoints vs values logged by 03b

| modality   | model           |   max_abs_threshold_difference |
|:-----------|:----------------|-------------------------------:|
| cytology   | ConvNeXt-Small  |                              0 |
| cytology   | DenseNet-121    |                              0 |
| cytology   | EfficientNet-B3 |                              0 |
| cytology   | ResNet-50       |                              0 |
| cytology   | Swin-Tiny       |                              0 |
| ultrasound | ConvNeXt-Small  |                              0 |
| ultrasound | DenseNet-121    |                              0 |
| ultrasound | EfficientNet-B3 |                              0 |
| ultrasound | ResNet-50       |                              0 |
| ultrasound | Swin-Tiny       |                              0 |


## D1_leakage_demonstration: Same code, data and seeds; only the fold grouping unit differs (cytology)

Image-level folds let blocks from the same case fall on both sides of every fold, reproducing the original design.

| model           | design             | fold_auroc_mean_sd   | pooled_oof_auroc    |   pooled_brier |   within_cv_case_leakage |
|:----------------|:-------------------|:---------------------|:--------------------|---------------:|-------------------------:|
| ConvNeXt-Small  | case-grouped folds | 0.872 ± 0.071        | 0.868 (0.833–0.898) |          0.153 |                    0     |
| ConvNeXt-Small  | image-level folds  | 0.880 ± 0.068        | 0.866 (0.836–0.894) |          0.158 |                    0.998 |
| EfficientNet-B3 | case-grouped folds | 0.960 ± 0.023        | 0.954 (0.936–0.970) |          0.088 |                    0     |
| EfficientNet-B3 | image-level folds  | 0.976 ± 0.013        | 0.974 (0.963–0.984) |          0.068 |                    0.998 |


## D2_leakage_fold_pairs: Fold AUROC by grouping unit

| model           |   fold |   case_grouped |   image_level |
|:----------------|-------:|---------------:|--------------:|
| ConvNeXt-Small  |      1 |         0.9534 |        0.9371 |
| ConvNeXt-Small  |      2 |         0.8006 |        0.7689 |
| ConvNeXt-Small  |      3 |         0.8001 |        0.862  |
| ConvNeXt-Small  |      4 |         0.9298 |        0.9135 |
| ConvNeXt-Small  |      5 |         0.8763 |        0.9174 |
| EfficientNet-B3 |      1 |         0.9551 |        0.9564 |
| EfficientNet-B3 |      2 |         0.9882 |        0.9888 |
| EfficientNet-B3 |      3 |         0.9288 |        0.9847 |
| EfficientNet-B3 |      4 |         0.9757 |        0.9727 |
| EfficientNet-B3 |      5 |         0.9498 |        0.9775 |


## E1_shortcut_control: EfficientNet-B3 grouped 5-fold CV with the sector or the surround removed (same folds and seeds)

If the surround-only model discriminates (CI above 0.5), label information is recoverable from outside the image of the thyroid.

| input                              | fold_auroc_mean_sd   | fold_aurocs                       | pooled_oof_auroc    | ci_excludes_chance   |
|:-----------------------------------|:---------------------|:----------------------------------|:--------------------|:---------------------|
| full image                         | 0.700 ± 0.080        | 0.800, 0.584, 0.733, 0.711, 0.674 | 0.707 (0.647–0.764) | True                 |
| surround only (sector blacked out) | 0.693 ± 0.057        | 0.795, 0.676, 0.672, 0.658, 0.664 | 0.685 (0.624–0.743) | True                 |
| sector only (surround blacked out) | 0.687 ± 0.054        | 0.734, 0.665, 0.739, 0.608, 0.688 | 0.697 (0.638–0.752) | True                 |

- Figures written: ['Fig1', 'Fig2', 'Fig3', 'Fig4', 'Fig5'] (+ Grad-CAM, t-SNE and supplementary sheets from stages A, G, I).

- Release folder ready: D:\Thyroid-BHI-26\revision_round2\release — push it to GitHub, tag a release, and archive it on Zenodo for a DOI.


## A1_archive: Pang archive as released (all files)

| modality   |   images |   benign_images |   ptc_images |   cases |   benign_cases |   ptc_cases |
|:-----------|---------:|----------------:|-------------:|--------:|---------------:|------------:|
| cytology   |     1332 |             635 |          697 |     384 |            165 |         219 |
| ultrasound |      387 |             165 |          222 |     387 |            165 |         222 |

- Cytology blocks per case: {2: 16, 3: 243, 4: 77, 5: 26, 6: 21, 7: 1} (mean 3.47); cases with both modalities: 384; ultrasound-only cases: ['PTC_0043', 'PTC_0112', 'PTC_0113']; case numbers reused across the two class folders: 165.


## A2_exact_duplicates: Exact (MD5) duplicate groups, including label conflicts

| modality   | conflict_type               | case_key   |   label | id                                                            | md5                              | may_split   | in_frozen_manifest   | frozen_split   |
|:-----------|:----------------------------|:-----------|--------:|:--------------------------------------------------------------|:---------------------------------|:------------|:---------------------|:---------------|
| cytology   | same label, different cases | PTC_0199   |       1 | cytological images of papillary thyroid carcinoma/199_001.tif | 2293d9cbc381e9b3b1797ecfaeacf66f | train       | True                 | train          |
| cytology   | same label, different cases | PTC_0201   |       1 | cytological images of papillary thyroid carcinoma/201_001.tif | 2293d9cbc381e9b3b1797ecfaeacf66f | train       | True                 | train          |
| cytology   | same label, different cases | BEN_0116   |       0 | cytological images of benign thyroid lesions/116_003.tif      | 3af2a01d518cbab3d1155aafcfe8c848 | train       | True                 | train          |
| cytology   | same label, different cases | BEN_0117   |       0 | cytological images of benign thyroid lesions/117_002.tif      | 3af2a01d518cbab3d1155aafcfe8c848 | train       | True                 | train          |
| cytology   | same label, different cases | PTC_0081   |       1 | cytological images of papillary thyroid carcinoma/81_002.tif  | af62e040024b7f5ed7575628992c9a06 | train       | True                 | train          |
| cytology   | same label, different cases | PTC_0082   |       1 | cytological images of papillary thyroid carcinoma/82_002.tif  | af62e040024b7f5ed7575628992c9a06 | train       | True                 | train          |
| cytology   | same label, different cases | PTC_0199   |       1 | cytological images of papillary thyroid carcinoma/199_003.tif | f4494ae13aa6cf0d76db7fd3ceddf401 | train       | True                 | train          |
| cytology   | same label, different cases | PTC_0201   |       1 | cytological images of papillary thyroid carcinoma/201_003.tif | f4494ae13aa6cf0d76db7fd3ceddf401 | train       | True                 | train          |
| ultrasound | cross-label                 | BEN_0039   |       0 | ultrasound images of benign thyroid lesions/39.jpg            | 2017d24c7ea7064164b107ed3b279ea7 | val         | False                | nan            |
| ultrasound | cross-label                 | PTC_0103   |       1 | ultrasound images of papillary thyroid carcinoma/103.jpg      | 2017d24c7ea7064164b107ed3b279ea7 | val         | False                | nan            |
| ultrasound | cross-label                 | BEN_0036   |       0 | ultrasound images of benign thyroid lesions/36.jpg            | 2ce2868b2042d681ed2ffedd6fa077d7 | val         | False                | nan            |
| ultrasound | cross-label                 | PTC_0093   |       1 | ultrasound images of papillary thyroid carcinoma/93.jpg       | 2ce2868b2042d681ed2ffedd6fa077d7 | val         | False                | nan            |
| ultrasound | cross-label                 | BEN_0003   |       0 | ultrasound images of benign thyroid lesions/3.jpg             | 5a252403dec58e49f8384225223900ea | train       | False                | nan            |
| ultrasound | cross-label                 | BEN_0055   |       0 | ultrasound images of benign thyroid lesions/55.jpg            | 5a252403dec58e49f8384225223900ea | train       | False                | nan            |
| ultrasound | cross-label                 | PTC_0139   |       1 | ultrasound images of papillary thyroid carcinoma/139.jpg      | 5a252403dec58e49f8384225223900ea | train       | False                | nan            |
| ultrasound | cross-label                 | BEN_0061   |       0 | ultrasound images of benign thyroid lesions/61.jpg            | 71164f281603d442bf5808a4febfd03c | train       | False                | nan            |
| ultrasound | cross-label                 | PTC_0160   |       1 | ultrasound images of papillary thyroid carcinoma/160.jpg      | 71164f281603d442bf5808a4febfd03c | train       | False                | nan            |
| ultrasound | cross-label                 | BEN_0044   |       0 | ultrasound images of benign thyroid lesions/44.jpg            | 83728c1b56f165f0024ed92aa2d4ca83 | test        | False                | nan            |
| ultrasound | cross-label                 | PTC_0112   |       1 | ultrasound images of papillary thyroid carcinoma/112.jpg      | 83728c1b56f165f0024ed92aa2d4ca83 | test        | False                | nan            |
| ultrasound | cross-label                 | BEN_0019   |       0 | ultrasound images of benign thyroid lesions/19.jpg            | 925e32aba60228a11330d17e00d26c52 | test        | False                | nan            |
| ultrasound | cross-label                 | PTC_0027   |       1 | ultrasound images of papillary thyroid carcinoma/27.jpg       | 925e32aba60228a11330d17e00d26c52 | test        | False                | nan            |
| ultrasound | cross-label                 | BEN_0025   |       0 | ultrasound images of benign thyroid lesions/25.jpg            | acef77b7e8e42fe3173fe0a7521e2e30 | train       | False                | nan            |
| ultrasound | cross-label                 | PTC_0044   |       1 | ultrasound images of papillary thyroid carcinoma/44.jpg       | acef77b7e8e42fe3173fe0a7521e2e30 | train       | False                | nan            |
| ultrasound | cross-label                 | BEN_0038   |       0 | ultrasound images of benign thyroid lesions/38.jpg            | b23899ff958e2e0777e17ea8d601e7d3 | train       | False                | nan            |
| ultrasound | cross-label                 | PTC_0099   |       1 | ultrasound images of papillary thyroid carcinoma/99.jpg       | b23899ff958e2e0777e17ea8d601e7d3 | train       | False                | nan            |
| ultrasound | cross-label                 | BEN_0020   |       0 | ultrasound images of benign thyroid lesions/20.jpg            | e8f7705cd05f793d14068efbae5fd71b | test        | False                | nan            |
| ultrasound | cross-label                 | PTC_0037   |       1 | ultrasound images of papillary thyroid carcinoma/37.jpg       | e8f7705cd05f793d14068efbae5fd71b | test        | False                | nan            |
| ultrasound | same label, different cases | PTC_0114   |       1 | ultrasound images of papillary thyroid carcinoma/114.jpg      | 1bfd41702c0e7e637950961a76ff6c9f | val         | True                 | val            |
| ultrasound | same label, different cases | PTC_0115   |       1 | ultrasound images of papillary thyroid carcinoma/115.jpg      | 1bfd41702c0e7e637950961a76ff6c9f | val         | True                 | val            |


## A2b_duplicate_summary: Duplicate groups by type

| modality   | conflict_type               |   groups |   images |   kept_in_frozen |
|:-----------|:----------------------------|---------:|---------:|-----------------:|
| cytology   | same label, different cases |        4 |        8 |                8 |
| ultrasound | cross-label                 |        9 |       19 |                0 |
| ultrasound | same label, different cases |        1 |        2 |                2 |


## A3_exclusions: Images excluded from the frozen manifest

| exclusion_reason                                                            |   images |
|:----------------------------------------------------------------------------|---------:|
| cross_label_exact_md5;cross_label_identical_phash;cross_label_leakage_group |       19 |
| cross_label_identical_phash;cross_label_leakage_group                       |        4 |


## A4_phash_sensitivity: Perceptual-hash (DCT pHash, 64-bit) near-duplicate pairs by Hamming threshold

The original pipeline grouped identical pHash values only (Hamming 0). Pairs crossing frozen partitions are listed for visual review.

| modality   |   hamming_max |   pairs |   cross_case |   cross_label |   cross_frozen_partition |
|:-----------|--------------:|--------:|-------------:|--------------:|-------------------------:|
| cytology   |             0 |       4 |            4 |             0 |                        0 |
| cytology   |             2 |       5 |            5 |             0 |                        1 |
| cytology   |             4 |       5 |            5 |             0 |                        1 |
| cytology   |             6 |       7 |            6 |             0 |                        1 |
| cytology   |             8 |       8 |            7 |             0 |                        1 |
| cytology   |            10 |       8 |            7 |             0 |                        1 |
| ultrasound |             0 |      14 |           14 |            12 |                        0 |
| ultrasound |             2 |      14 |           14 |            12 |                        0 |
| ultrasound |             4 |      21 |           21 |            15 |                        0 |
| ultrasound |             6 |      41 |           41 |            25 |                        9 |
| ultrasound |             8 |     184 |          184 |            69 |                       69 |
| ultrasound |            10 |     818 |          818 |           293 |                      355 |


## A5_leakage_original_split: Measured case-level leakage in the original image-level split (Tables 3–13 of the submitted manuscript)

| modality   | partition   |   images |   cases |   images_with_same_case_in_train |   cases_with_images_in_train |   cross_label_conflict_images |
|:-----------|:------------|---------:|--------:|---------------------------------:|-----------------------------:|------------------------------:|
| cytology   | val         |      200 |     160 |                            0.925 |                        0.944 |                             0 |
| cytology   | test        |      200 |     160 |                            0.89  |                        0.931 |                             0 |
| ultrasound | val         |       59 |      59 |                            0     |                        0     |                             4 |
| ultrasound | test        |       60 |      60 |                            0     |                        0     |                             6 |


## A6_original_image_level_results: Original (leaky, image-level) test results, recomputed from files

| model                      |   n |   auroc |   auprc |   brier |
|:---------------------------|----:|--------:|--------:|--------:|
| Cytology ConvNeXt-Small    | 200 |  0.9884 |  0.99   |  0.0296 |
| Cytology Ensemble (v2)     | 200 |  0.9862 |  0.9889 |  0.0307 |
| Cytology ConvNeXt-Tiny     | 200 |  0.9825 |  0.9879 |  0.0342 |
| Cytology Swin-Tiny         | 200 |  0.9797 |  0.9821 |  0.0446 |
| Cytology EfficientNet-B3   | 200 |  0.9755 |  0.9724 |  0.0617 |
| Ultrasound EfficientNet-B3 |  60 |  0.7449 |  0.8018 |  0.2647 |


## A7_prior_paper_reconciliation: Reconciliation with the published BMC Medical Imaging analysis

| item                                                                                 | value                                                                        |
|:-------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------|
| patients                                                                             | 384                                                                          |
| benign / PTC                                                                         | 165 / 219                                                                    |
| linkage                                                                              | class folder + case number (ultrasound <n>.jpg <-> cytology <n>_<block>.tif) |
| split                                                                                | {'development': 307, 'holdout': 77}                                          |
| patients carrying a cross-label duplicated ultrasound image                          | 18                                                                           |
| holdout patients whose ultrasound image is byte-identical to a development patient's | 4                                                                            |
| holdout patients involved                                                            | BEN_0038, BEN_0055, PTC_0027, PTC_0093                                       |


## A8_frozen_partitions: Frozen case-level partitions used for all new analyses

| modality   | split   |   images |   cases |   benign |   ptc |
|:-----------|:--------|---------:|--------:|---------:|------:|
| cytology   | test    |      214 |      58 |      102 |   112 |
| cytology   | train   |      907 |     269 |      427 |   480 |
| cytology   | val     |      211 |      57 |      106 |   105 |
| ultrasound | test    |       55 |      55 |       23 |    32 |
| ultrasound | train   |      254 |     254 |      107 |   147 |
| ultrasound | val     |       55 |      55 |       23 |    32 |


## F1_frozen_test_image_level: Frozen test set, image level; thresholds selected on validation; case-clustered 95% CIs

| modality   | model                | level   |   n |   benign |   ptc |   val_auroc | auroc               | auprc               |   no_skill_auprc |   threshold_from_val |   tn |   fp |   fn |   tp | sensitivity         | specificity         | accuracy            |    f1 |   brier |   ece15 |
|:-----------|:---------------------|:--------|----:|---------:|------:|------------:|:--------------------|:--------------------|-----------------:|---------------------:|-----:|-----:|-----:|-----:|:--------------------|:--------------------|:--------------------|------:|--------:|--------:|
| ultrasound | ConvNeXt-Small       | image   |  55 |       23 |    32 |       0.628 | 0.736 (0.595–0.864) | 0.829 (0.701–0.925) |            0.582 |               0.4721 |   18 |    5 |   11 |   21 | 0.656 (0.484–0.816) | 0.783 (0.593–0.947) | 0.709 (0.582–0.818) | 0.724 |   0.255 |   0.11  |
| ultrasound | EfficientNet-B3      | image   |  55 |       23 |    32 |       0.792 | 0.859 (0.745–0.952) | 0.857 (0.714–0.972) |            0.582 |               0.0062 |   16 |    7 |    4 |   28 | 0.875 (0.742–0.971) | 0.696 (0.500–0.875) | 0.800 (0.691–0.891) | 0.836 |   0.214 |   0.244 |
| ultrasound | Swin-Tiny            | image   |  55 |       23 |    32 |       0.655 | 0.735 (0.589–0.868) | 0.758 (0.602–0.922) |            0.582 |               0.4198 |   21 |    2 |   20 |   12 | 0.375 (0.212–0.543) | 0.913 (0.789–1.000) | 0.600 (0.473–0.727) | 0.522 |   0.268 |   0.225 |
| ultrasound | ResNet-50            | image   |  55 |       23 |    32 |       0.855 | 0.827 (0.696–0.930) | 0.871 (0.758–0.955) |            0.582 |               0.144  |   17 |    6 |   11 |   21 | 0.656 (0.485–0.812) | 0.739 (0.542–0.909) | 0.691 (0.564–0.800) | 0.712 |   0.396 |   0.439 |
| ultrasound | DenseNet-121         | image   |  55 |       23 |    32 |       0.81  | 0.852 (0.740–0.942) | 0.887 (0.784–0.965) |            0.582 |               0.3966 |   20 |    3 |   14 |   18 | 0.562 (0.393–0.731) | 0.870 (0.714–1.000) | 0.691 (0.564–0.800) | 0.679 |   0.246 |   0.292 |
| ultrasound | Ensemble (mean of 5) | image   |  55 |       23 |    32 |       0.842 | 0.909 (0.811–0.978) | 0.918 (0.810–0.987) |            0.582 |               0.3507 |   21 |    2 |   10 |   22 | 0.688 (0.519–0.846) | 0.913 (0.782–1.000) | 0.782 (0.673–0.891) | 0.786 |   0.223 |   0.289 |
| cytology   | ConvNeXt-Small       | image   | 214 |      102 |   112 |       0.968 | 0.984 (0.966–0.996) | 0.985 (0.966–0.997) |            0.523 |               0.3789 |   93 |    9 |    7 |  105 | 0.938 (0.893–0.974) | 0.912 (0.836–0.973) | 0.925 (0.886–0.962) | 0.929 |   0.061 |   0.096 |
| cytology   | EfficientNet-B3      | image   | 214 |      102 |   112 |       0.988 | 0.990 (0.978–0.998) | 0.991 (0.978–0.999) |            0.523 |               0.5993 |  100 |    2 |   17 |   95 | 0.848 (0.753–0.935) | 0.980 (0.951–1.000) | 0.911 (0.854–0.959) | 0.909 |   0.065 |   0.072 |
| cytology   | Swin-Tiny            | image   | 214 |      102 |   112 |       0.989 | 0.995 (0.985–1.000) | 0.995 (0.987–1.000) |            0.523 |               0.4947 |   99 |    3 |    9 |  103 | 0.920 (0.830–0.991) | 0.971 (0.924–1.000) | 0.944 (0.891–0.986) | 0.945 |   0.037 |   0.087 |
| cytology   | ResNet-50            | image   | 214 |      102 |   112 |       0.989 | 0.997 (0.991–1.000) | 0.997 (0.992–1.000) |            0.523 |               0.8486 |  102 |    0 |   15 |   97 | 0.866 (0.759–0.957) | 1.000 (1.000–1.000) | 0.930 (0.867–0.978) | 0.928 |   0.028 |   0.043 |
| cytology   | DenseNet-121         | image   | 214 |      102 |   112 |       0.99  | 0.982 (0.959–0.997) | 0.987 (0.969–0.997) |            0.523 |               0.1767 |   97 |    5 |    9 |  103 | 0.920 (0.850–0.976) | 0.951 (0.884–1.000) | 0.935 (0.888–0.975) | 0.936 |   0.061 |   0.07  |
| cytology   | Ensemble (mean of 5) | image   | 214 |      102 |   112 |       0.992 | 0.996 (0.990–1.000) | 0.996 (0.990–1.000) |            0.523 |               0.5924 |  102 |    0 |   13 |   99 | 0.884 (0.788–0.965) | 1.000 (1.000–1.000) | 0.939 (0.885–0.982) | 0.938 |   0.038 |   0.074 |


## F2_frozen_test_case_level: Frozen test set, case level (images aggregated per case); thresholds from validation

| modality   | model                | level   |   n |   benign |   ptc |   val_auroc | auroc               | auprc               |   no_skill_auprc |   threshold_from_val |   tn |   fp |   fn |   tp | sensitivity         | specificity         | accuracy            |    f1 |   brier |   ece15 |
|:-----------|:---------------------|:--------|----:|---------:|------:|------------:|:--------------------|:--------------------|-----------------:|---------------------:|-----:|-----:|-----:|-----:|:--------------------|:--------------------|:--------------------|------:|--------:|--------:|
| ultrasound | ConvNeXt-Small       | case    |  55 |       23 |    32 |       0.628 | 0.736 (0.595–0.864) | 0.829 (0.701–0.925) |            0.582 |               0.4721 |   18 |    5 |   11 |   21 | 0.656 (0.484–0.816) | 0.783 (0.593–0.947) | 0.709 (0.582–0.818) | 0.724 |   0.255 |   0.11  |
| ultrasound | EfficientNet-B3      | case    |  55 |       23 |    32 |       0.792 | 0.859 (0.745–0.952) | 0.857 (0.714–0.972) |            0.582 |               0.0062 |   16 |    7 |    4 |   28 | 0.875 (0.742–0.971) | 0.696 (0.500–0.875) | 0.800 (0.691–0.891) | 0.836 |   0.214 |   0.244 |
| ultrasound | Swin-Tiny            | case    |  55 |       23 |    32 |       0.655 | 0.735 (0.589–0.868) | 0.758 (0.602–0.922) |            0.582 |               0.4198 |   21 |    2 |   20 |   12 | 0.375 (0.212–0.543) | 0.913 (0.789–1.000) | 0.600 (0.473–0.727) | 0.522 |   0.268 |   0.225 |
| ultrasound | ResNet-50            | case    |  55 |       23 |    32 |       0.855 | 0.827 (0.696–0.930) | 0.871 (0.758–0.955) |            0.582 |               0.144  |   17 |    6 |   11 |   21 | 0.656 (0.485–0.812) | 0.739 (0.542–0.909) | 0.691 (0.564–0.800) | 0.712 |   0.396 |   0.439 |
| ultrasound | DenseNet-121         | case    |  55 |       23 |    32 |       0.81  | 0.852 (0.740–0.942) | 0.887 (0.784–0.965) |            0.582 |               0.3966 |   20 |    3 |   14 |   18 | 0.562 (0.393–0.731) | 0.870 (0.714–1.000) | 0.691 (0.564–0.800) | 0.679 |   0.246 |   0.292 |
| ultrasound | Ensemble (mean of 5) | case    |  55 |       23 |    32 |       0.842 | 0.909 (0.811–0.978) | 0.918 (0.810–0.987) |            0.582 |               0.3507 |   21 |    2 |   10 |   22 | 0.688 (0.519–0.846) | 0.913 (0.782–1.000) | 0.782 (0.673–0.891) | 0.786 |   0.223 |   0.289 |
| cytology   | ConvNeXt-Small       | case    |  58 |       25 |    33 |       0.962 | 0.998 (0.989–1.000) | 0.998 (0.992–1.000) |            0.569 |               0.4685 |   23 |    2 |    1 |   32 | 0.970 (0.900–1.000) | 0.920 (0.800–1.000) | 0.948 (0.896–1.000) | 0.955 |   0.052 |   0.175 |
| cytology   | EfficientNet-B3      | case    |  58 |       25 |    33 |       0.997 | 0.999 (0.993–1.000) | 0.999 (0.995–1.000) |            0.569 |               0.6178 |   25 |    0 |    5 |   28 | 0.848 (0.719–0.967) | 1.000 (1.000–1.000) | 0.914 (0.845–0.983) | 0.918 |   0.041 |   0.075 |
| cytology   | Swin-Tiny            | case    |  58 |       25 |    33 |       0.991 | 0.999 (0.993–1.000) | 0.999 (0.995–1.000) |            0.569 |               0.6461 |   25 |    0 |    2 |   31 | 0.939 (0.850–1.000) | 1.000 (1.000–1.000) | 0.966 (0.914–1.000) | 0.969 |   0.03  |   0.107 |
| cytology   | ResNet-50            | case    |  58 |       25 |    33 |       0.994 | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) |            0.569 |               0.6653 |   25 |    0 |    2 |   31 | 0.939 (0.846–1.000) | 1.000 (1.000–1.000) | 0.966 (0.914–1.000) | 0.969 |   0.018 |   0.049 |
| cytology   | DenseNet-121         | case    |  58 |       25 |    33 |       0.996 | 0.999 (0.993–1.000) | 0.999 (0.995–1.000) |            0.569 |               0.609  |   25 |    0 |    5 |   28 | 0.848 (0.714–0.960) | 1.000 (1.000–1.000) | 0.914 (0.828–0.983) | 0.918 |   0.044 |   0.089 |
| cytology   | Ensemble (mean of 5) | case    |  58 |       25 |    33 |       0.995 | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) |            0.569 |               0.5433 |   25 |    0 |    2 |   31 | 0.939 (0.850–1.000) | 1.000 (1.000–1.000) | 0.966 (0.914–1.000) | 0.969 |   0.03  |   0.106 |


## F3_temperature_scaling: Temperature scaling fitted on validation; test ECE (15 equal-width bins) and decisions

Temperature scaling is monotone: re-selecting the threshold on validation after scaling leaves every decision unchanged; reusing the old numeric threshold does not.

| modality   | model                | temperature                                    |   test_ece_before |   test_ece_after |   test_brier_before |   test_brier_after |   accuracy_original |   accuracy_scaled_same_numeric_threshold |   accuracy_scaled_threshold_reselected_on_val | decisions_identical_after_reselection   |
|:-----------|:---------------------|:-----------------------------------------------|------------------:|-----------------:|--------------------:|-------------------:|--------------------:|-----------------------------------------:|----------------------------------------------:|:----------------------------------------|
| ultrasound | ConvNeXt-Small       | >100 (search bound; near-uninformative logits) |             0.11  |            0.082 |               0.255 |              0.25  |               0.709 |                                    0.582 |                                         0.709 | True                                    |
| ultrasound | EfficientNet-B3      | 8.186                                          |             0.244 |            0.245 |               0.214 |              0.185 |               0.8   |                                    0.582 |                                         0.8   | True                                    |
| ultrasound | Swin-Tiny            | >100 (search bound; near-uninformative logits) |             0.225 |            0.083 |               0.268 |              0.25  |               0.6   |                                    0.582 |                                         0.6   | True                                    |
| ultrasound | ResNet-50            | 8.598                                          |             0.439 |            0.211 |               0.396 |              0.249 |               0.691 |                                    0.582 |                                         0.691 | True                                    |
| ultrasound | DenseNet-121         | 3.125                                          |             0.292 |            0.229 |               0.246 |              0.201 |               0.691 |                                    0.709 |                                         0.691 | True                                    |
| ultrasound | Ensemble (mean of 5) | 1.499                                          |             0.289 |            0.285 |               0.223 |              0.22  |               0.782 |                                    0.836 |                                         0.782 | True                                    |
| cytology   | ConvNeXt-Small       | 0.711                                          |             0.096 |            0.06  |               0.061 |              0.056 |               0.925 |                                    0.921 |                                         0.925 | True                                    |
| cytology   | EfficientNet-B3      | 2.635                                          |             0.072 |            0.066 |               0.065 |              0.055 |               0.911 |                                    0.907 |                                         0.911 | True                                    |
| cytology   | Swin-Tiny            | 0.74                                           |             0.087 |            0.065 |               0.037 |              0.034 |               0.944 |                                    0.944 |                                         0.944 | True                                    |
| cytology   | ResNet-50            | 1.98                                           |             0.043 |            0.049 |               0.028 |              0.029 |               0.93  |                                    0.897 |                                         0.93  | True                                    |
| cytology   | DenseNet-121         | 1.264                                          |             0.07  |            0.071 |               0.061 |              0.06  |               0.935 |                                    0.939 |                                         0.935 | True                                    |
| cytology   | Ensemble (mean of 5) | 0.7                                            |             0.074 |            0.058 |               0.038 |              0.037 |               0.939 |                                    0.939 |                                         0.939 | True                                    |

- Sector box detection on 110 ultrasound val/test images: {'detected': 78, 'fallback': 32}.


## G1_gradcam_attribution: Grad-CAM mass outside the detected ultrasound sector (EfficientNet-B3, val+test)

Expected mass under spatially uniform attribution equals the area outside the sector.

| outcome   |   images |   mean_cam_mass_outside_sector |   median_cam_mass_outside_sector |   mean_area_outside_sector |   share_peak_outside_sector |
|:----------|---------:|-------------------------------:|---------------------------------:|---------------------------:|----------------------------:|
| FN        |       10 |                          0.517 |                            0.549 |                      0.53  |                       0.5   |
| FP        |       15 |                          0.472 |                            0.395 |                      0.538 |                       0.467 |
| TN        |       31 |                          0.554 |                            0.501 |                      0.423 |                       0.71  |
| TP        |       54 |                          0.323 |                            0.246 |                      0.467 |                       0.204 |
| ALL       |      110 |                          0.426 |                            0.375 |                      0.47  |                       0.409 |


## I1_mmd: Maximum mean discrepancy between cohorts (EfficientNet-B3 features, PCA-50, RBF kernel, 500 permutations)

| comparison                          |   mmd2 |   permutation_p |
|:------------------------------------|-------:|----------------:|
| Pang train vs Pang test (reference) | 0.0159 |          0.1637 |


## I2_image_statistics: Acquisition-level image statistics by cohort

| cohort          |   images |   median_width |   median_height |   mean_intensity |   mean_contrast_sd |   share_near_black |
|:----------------|---------:|---------------:|----------------:|-----------------:|-------------------:|-------------------:|
| Pang (internal) |      364 |           1346 |             759 |             33.1 |               37.7 |              0.474 |

- Fold check: saved August folds reproduced exactly; August ConvNeXt-Small run reused.  
  `{"sklearn": "1.7.2", "folds_reproduced": {"ultrasound": true, "cytology": true}, "ok": true}`


## B1_cv_summary_from_03b: Grouped 5-fold CV summaries written by 03b

| modality   | model_key       | model           |   n_outer_folds |   development_images |   development_source_groups |   development_components |   fold_auroc_mean |   fold_auroc_sd |   fold_auprc_mean |   fold_auprc_sd |   pooled_oof_image_auroc |   pooled_oof_image_auprc |   pooled_oof_source_group_auroc |   pooled_oof_source_group_auprc |
|:-----------|:----------------|:----------------|----------------:|---------------------:|----------------------------:|-------------------------:|------------------:|----------------:|------------------:|----------------:|-------------------------:|-------------------------:|--------------------------------:|--------------------------------:|
| ultrasound | convnext_small  | ConvNeXt-Small  |               5 |                  309 |                         309 |                      308 |            0.644  |          0.1019 |            0.7219 |          0.09   |                   0.5277 |                   0.6275 |                          0.5277 |                          0.6275 |
| ultrasound | efficientnet_b3 | EfficientNet-B3 |               5 |                  309 |                         309 |                      308 |            0.7002 |          0.0797 |            0.7711 |          0.0513 |                   0.7066 |                   0.7672 |                          0.7066 |                          0.7672 |
| ultrasound | swin_tiny       | Swin-Tiny       |               5 |                  309 |                         309 |                      308 |            0.6123 |          0.0662 |            0.6815 |          0.0623 |                   0.5884 |                   0.653  |                          0.5884 |                          0.653  |
| ultrasound | resnet50        | ResNet50        |               5 |                  309 |                         309 |                      308 |            0.7429 |          0.0844 |            0.7964 |          0.0648 |                   0.7211 |                   0.7672 |                          0.7211 |                          0.7672 |
| ultrasound | densenet121     | DenseNet121     |               5 |                  309 |                         309 |                      308 |            0.796  |          0.0482 |            0.8382 |          0.0282 |                   0.7765 |                   0.8079 |                          0.7765 |                          0.8079 |
| cytology   | convnext_small  | ConvNeXt-Small  |               5 |                 1118 |                         326 |                      323 |            0.872  |          0.0711 |            0.88   |          0.0602 |                   0.8676 |                   0.8583 |                          0.8751 |                          0.8822 |
| cytology   | efficientnet_b3 | EfficientNet-B3 |               5 |                 1118 |                         326 |                      323 |            0.9595 |          0.0231 |            0.9566 |          0.0278 |                   0.9544 |                   0.9512 |                          0.9687 |                          0.9726 |
| cytology   | swin_tiny       | Swin-Tiny       |               5 |                 1118 |                         326 |                      323 |            0.963  |          0.0266 |            0.9639 |          0.0288 |                   0.9504 |                   0.9446 |                          0.9663 |                          0.9712 |
| cytology   | resnet50        | ResNet50        |               5 |                 1118 |                         326 |                      323 |            0.9581 |          0.0266 |            0.9627 |          0.0239 |                   0.9564 |                   0.9613 |                          0.968  |                          0.974  |
| cytology   | densenet121     | DenseNet121     |               5 |                 1118 |                         326 |                      323 |            0.9566 |          0.026  |            0.959  |          0.0298 |                   0.9481 |                   0.9485 |                          0.9678 |                          0.9748 |


## C1_cv_summary: Grouped 5-fold CV on the development set (train+val); frozen test untouched

Groups = duplicate-connected case components. Fold thresholds are Youden points on each fold's inner validation split; pooled OOF CIs resample components. within_cv_case_leakage = share of holdout images whose case appears in training folds.

| modality   | model                |   dev_images |   dev_cases | fold_auroc_mean_sd   | fold_auroc_range   | fold_auprc_mean_sd   | pooled_oof_auroc    | pooled_oof_auprc    |   pooled_brier |   pooled_ece15 |   sensitivity_at_fold_thresholds |   specificity_at_fold_thresholds |   within_cv_case_leakage |
|:-----------|:---------------------|-------------:|------------:|:---------------------|:-------------------|:---------------------|:--------------------|:--------------------|---------------:|---------------:|---------------------------------:|---------------------------------:|-------------------------:|
| ultrasound | ConvNeXt-Small       |          309 |         309 | 0.644 ± 0.102        | 0.508–0.758        | 0.722 ± 0.090        | 0.528 (0.463–0.595) | 0.627 (0.553–0.708) |          0.288 |          0.203 |                            0.464 |                            0.723 |                        0 |
| ultrasound | EfficientNet-B3      |          309 |         309 | 0.700 ± 0.080        | 0.584–0.800        | 0.771 ± 0.051        | 0.707 (0.647–0.764) | 0.767 (0.703–0.824) |          0.328 |          0.323 |                            0.715 |                            0.554 |                        0 |
| ultrasound | Swin-Tiny            |          309 |         309 | 0.612 ± 0.066        | 0.529–0.681        | 0.682 ± 0.062        | 0.588 (0.522–0.656) | 0.653 (0.580–0.734) |          0.259 |          0.148 |                            0.419 |                            0.738 |                        0 |
| ultrasound | ResNet-50            |          309 |         309 | 0.743 ± 0.084        | 0.604–0.833        | 0.796 ± 0.065        | 0.721 (0.664–0.777) | 0.767 (0.704–0.825) |          0.234 |          0.176 |                            0.682 |                            0.623 |                        0 |
| ultrasound | DenseNet-121         |          309 |         309 | 0.796 ± 0.048        | 0.716–0.840        | 0.838 ± 0.028        | 0.776 (0.725–0.825) | 0.808 (0.746–0.866) |          0.219 |          0.165 |                            0.693 |                            0.7   |                        0 |
| ultrasound | Ensemble (mean of 5) |          309 |         309 | 0.763 ± 0.094        | 0.599–0.829        | 0.822 ± 0.063        | 0.768 (0.716–0.819) | 0.809 (0.750–0.866) |          0.202 |          0.115 |                            0.709 |                            0.646 |                        0 |
| cytology   | ConvNeXt-Small       |         1118 |         326 | 0.872 ± 0.071        | 0.800–0.953        | 0.880 ± 0.060        | 0.868 (0.833–0.898) | 0.858 (0.810–0.904) |          0.153 |          0.041 |                            0.844 |                            0.75  |                        0 |
| cytology   | EfficientNet-B3      |         1118 |         326 | 0.960 ± 0.023        | 0.929–0.988        | 0.957 ± 0.028        | 0.954 (0.936–0.970) | 0.951 (0.927–0.971) |          0.088 |          0.081 |                            0.92  |                            0.882 |                        0 |
| cytology   | Swin-Tiny            |         1118 |         326 | 0.963 ± 0.027        | 0.935–0.998        | 0.964 ± 0.029        | 0.950 (0.929–0.969) | 0.945 (0.911–0.971) |          0.079 |          0.043 |                            0.899 |                            0.891 |                        0 |
| cytology   | ResNet-50            |         1118 |         326 | 0.958 ± 0.027        | 0.931–0.996        | 0.963 ± 0.024        | 0.956 (0.938–0.971) | 0.961 (0.944–0.976) |          0.079 |          0.034 |                            0.921 |                            0.876 |                        0 |
| cytology   | DenseNet-121         |         1118 |         326 | 0.957 ± 0.026        | 0.924–0.990        | 0.959 ± 0.030        | 0.948 (0.929–0.966) | 0.949 (0.922–0.969) |          0.087 |          0.065 |                            0.889 |                            0.887 |                        0 |
| cytology   | Ensemble (mean of 5) |         1118 |         326 | 0.964 ± 0.028        | 0.933–0.996        | 0.966 ± 0.029        | 0.958 (0.938–0.975) | 0.956 (0.928–0.977) |          0.069 |          0.045 |                            0.944 |                            0.886 |                        0 |


## C2_cv_fold_level: Fold-level results (all backbones and ensemble)

| modality   | model                |   fold |   n |   cases |   auroc |   auprc |   threshold_inner_val |   sensitivity |   specificity |   brier |
|:-----------|:---------------------|-------:|----:|--------:|--------:|--------:|----------------------:|--------------:|--------------:|--------:|
| ultrasound | ConvNeXt-Small       |      1 |  62 |      62 |  0.5085 |  0.604  |                0.3135 |         0.389 |         0.692 |  0.3149 |
| ultrasound | ConvNeXt-Small       |      2 |  63 |      63 |  0.5717 |  0.7309 |                0.4692 |         0.4   |         0.696 |  0.2596 |
| ultrasound | ConvNeXt-Small       |      3 |  61 |      61 |  0.7064 |  0.7076 |                0.3828 |         0.971 |         0.296 |  0.2772 |
| ultrasound | ConvNeXt-Small       |      4 |  61 |      61 |  0.7584 |  0.8563 |                0.3057 |         0.27  |         1     |  0.3291 |
| ultrasound | ConvNeXt-Small       |      5 |  62 |      62 |  0.675  |  0.7109 |                0.4073 |         0.312 |         0.933 |  0.2615 |
| ultrasound | EfficientNet-B3      |      1 |  62 |      62 |  0.8002 |  0.8484 |                0.0051 |         0.806 |         0.654 |  0.3245 |
| ultrasound | EfficientNet-B3      |      2 |  63 |      63 |  0.5837 |  0.7507 |                0.6974 |         0.625 |         0.435 |  0.4104 |
| ultrasound | EfficientNet-B3      |      3 |  61 |      61 |  0.7326 |  0.7561 |                0.9934 |         0.471 |         0.741 |  0.2678 |
| ultrasound | EfficientNet-B3      |      4 |  61 |      61 |  0.7106 |  0.789  |                0.2248 |         0.757 |         0.583 |  0.2879 |
| ultrasound | EfficientNet-B3      |      5 |  62 |      62 |  0.674  |  0.7111 |                0.0129 |         0.938 |         0.367 |  0.345  |
| ultrasound | Swin-Tiny            |      1 |  62 |      62 |  0.5288 |  0.5984 |                0.5155 |         0.306 |         0.654 |  0.2497 |
| ultrasound | Swin-Tiny            |      2 |  63 |      63 |  0.5685 |  0.7215 |                0.5982 |         0.475 |         0.696 |  0.2466 |
| ultrasound | Swin-Tiny            |      3 |  61 |      61 |  0.6808 |  0.7554 |                0.3256 |         0.412 |         0.889 |  0.3004 |
| ultrasound | Swin-Tiny            |      4 |  61 |      61 |  0.6081 |  0.6425 |                0.4551 |         0.324 |         0.75  |  0.2588 |
| ultrasound | Swin-Tiny            |      5 |  62 |      62 |  0.675  |  0.6899 |                0.5037 |         0.594 |         0.7   |  0.2407 |
| ultrasound | ResNet-50            |      1 |  62 |      62 |  0.7682 |  0.8388 |                0.4076 |         0.639 |         0.731 |  0.2302 |
| ultrasound | ResNet-50            |      2 |  63 |      63 |  0.6043 |  0.7291 |                0.3685 |         0.7   |         0.435 |  0.2924 |
| ultrasound | ResNet-50            |      3 |  61 |      61 |  0.744  |  0.7229 |                0.5902 |         0.588 |         0.778 |  0.2204 |
| ultrasound | ResNet-50            |      4 |  61 |      61 |  0.7646 |  0.8566 |                0.9531 |         0.595 |         0.75  |  0.2417 |
| ultrasound | ResNet-50            |      5 |  62 |      62 |  0.8333 |  0.8347 |                0.0926 |         0.906 |         0.433 |  0.1849 |
| ultrasound | DenseNet-121         |      1 |  62 |      62 |  0.8397 |  0.8785 |                0.533  |         0.611 |         0.885 |  0.2154 |
| ultrasound | DenseNet-121         |      2 |  63 |      63 |  0.7163 |  0.8108 |                0.9834 |         0.45  |         0.826 |  0.2367 |
| ultrasound | DenseNet-121         |      3 |  61 |      61 |  0.8039 |  0.8285 |                0.5421 |         0.735 |         0.63  |  0.1936 |
| ultrasound | DenseNet-121         |      4 |  61 |      61 |  0.7928 |  0.8177 |                0.1268 |         0.892 |         0.542 |  0.2649 |
| ultrasound | DenseNet-121         |      5 |  62 |      62 |  0.8271 |  0.8554 |                0.3156 |         0.812 |         0.633 |  0.1822 |
| ultrasound | Ensemble (mean of 5) |      1 |  62 |      62 |  0.7959 |  0.8513 |                0.3643 |         0.75  |         0.769 |  0.2144 |
| ultrasound | Ensemble (mean of 5) |      2 |  63 |      63 |  0.5989 |  0.7104 |                0.6206 |         0.5   |         0.652 |  0.2278 |
| ultrasound | Ensemble (mean of 5) |      3 |  61 |      61 |  0.8094 |  0.8556 |                0.4991 |         0.706 |         0.704 |  0.1884 |
| ultrasound | Ensemble (mean of 5) |      4 |  61 |      61 |  0.7838 |  0.8354 |                0.4836 |         0.73  |         0.667 |  0.2009 |
| ultrasound | Ensemble (mean of 5) |      5 |  62 |      62 |  0.8292 |  0.8581 |                0.357  |         0.906 |         0.467 |  0.1802 |
| cytology   | ConvNeXt-Small       |      1 | 217 |      64 |  0.9534 |  0.9528 |                0.5276 |         0.85  |         0.927 |  0.0918 |
| cytology   | ConvNeXt-Small       |      2 | 223 |      65 |  0.8006 |  0.8393 |                0.5702 |         0.767 |         0.65  |  0.2433 |
| cytology   | ConvNeXt-Small       |      3 | 216 |      65 |  0.8001 |  0.8212 |                0.3048 |         0.759 |         0.712 |  0.1876 |
| cytology   | ConvNeXt-Small       |      4 | 224 |      65 |  0.9298 |  0.9364 |                0.2497 |         0.927 |         0.74  |  0.103  |
| cytology   | ConvNeXt-Small       |      5 | 238 |      67 |  0.8763 |  0.8504 |                0.5902 |         0.91  |         0.716 |  0.1407 |
| cytology   | EfficientNet-B3      |      1 | 217 |      64 |  0.9551 |  0.9479 |                0.0162 |         0.963 |         0.809 |  0.097  |
| cytology   | EfficientNet-B3      |      2 | 223 |      65 |  0.9882 |  0.991  |                0.8934 |         0.908 |         0.99  |  0.0435 |
| cytology   | EfficientNet-B3      |      3 | 216 |      65 |  0.9288 |  0.9257 |                0.6218 |         0.866 |         0.894 |  0.1064 |
| cytology   | EfficientNet-B3      |      4 | 224 |      65 |  0.9757 |  0.9799 |                0.2237 |         0.919 |         0.9   |  0.0841 |
| cytology   | EfficientNet-B3      |      5 | 238 |      67 |  0.9498 |  0.9385 |                0.9314 |         0.943 |         0.828 |  0.1084 |
| cytology   | Swin-Tiny            |      1 | 217 |      64 |  0.9834 |  0.9837 |                0.6432 |         0.935 |         0.909 |  0.0647 |
| cytology   | Swin-Tiny            |      2 | 223 |      65 |  0.9975 |  0.998  |                0.9156 |         0.85  |         1     |  0.0211 |
| cytology   | Swin-Tiny            |      3 | 216 |      65 |  0.9434 |  0.9471 |                0.4394 |         0.875 |         0.913 |  0.0917 |
| cytology   | Swin-Tiny            |      4 | 224 |      65 |  0.9557 |  0.9651 |                0.1015 |         0.887 |         0.87  |  0.1138 |
| cytology   | Swin-Tiny            |      5 | 238 |      67 |  0.9349 |  0.9255 |                0.4225 |         0.951 |         0.776 |  0.1009 |
| cytology   | ResNet-50            |      1 | 217 |      64 |  0.9734 |  0.9758 |                0.4239 |         0.925 |         0.891 |  0.0668 |
| cytology   | ResNet-50            |      2 | 223 |      65 |  0.9964 |  0.997  |                0.7685 |         0.933 |         0.99  |  0.0233 |
| cytology   | ResNet-50            |      3 | 216 |      65 |  0.9311 |  0.937  |                0.308  |         0.893 |         0.865 |  0.1157 |
| cytology   | ResNet-50            |      4 | 224 |      65 |  0.9402 |  0.9478 |                0.3448 |         0.935 |         0.79  |  0.0888 |
| cytology   | ResNet-50            |      5 | 238 |      67 |  0.9495 |  0.9559 |                0.6778 |         0.918 |         0.845 |  0.1016 |
| cytology   | DenseNet-121         |      1 | 217 |      64 |  0.9633 |  0.9689 |                0.4758 |         0.879 |         0.9   |  0.0766 |
| cytology   | DenseNet-121         |      2 | 223 |      65 |  0.9895 |  0.9915 |                0.816  |         0.875 |         0.971 |  0.039  |
| cytology   | DenseNet-121         |      3 | 216 |      65 |  0.9372 |  0.9388 |                0.5787 |         0.839 |         0.933 |  0.0983 |
| cytology   | DenseNet-121         |      4 | 224 |      65 |  0.9688 |  0.9776 |                0.7419 |         0.919 |         0.9   |  0.0709 |
| cytology   | DenseNet-121         |      5 | 238 |      67 |  0.9241 |  0.9184 |                0.7091 |         0.926 |         0.75  |  0.145  |
| cytology   | Ensemble (mean of 5) |      1 | 217 |      64 |  0.9822 |  0.9842 |                0.3089 |         0.972 |         0.827 |  0.0548 |
| cytology   | Ensemble (mean of 5) |      2 | 223 |      65 |  0.9964 |  0.9972 |                0.6915 |         0.942 |         1     |  0.0329 |
| cytology   | Ensemble (mean of 5) |      3 | 216 |      65 |  0.9328 |  0.9431 |                0.4424 |         0.902 |         0.904 |  0.093  |
| cytology   | Ensemble (mean of 5) |      4 | 224 |      65 |  0.9719 |  0.978  |                0.4036 |         0.944 |         0.91  |  0.0648 |
| cytology   | Ensemble (mean of 5) |      5 | 238 |      67 |  0.9361 |  0.9274 |                0.5232 |         0.959 |         0.802 |  0.0957 |


## C3_threshold_reproducibility: Inner-validation thresholds recomputed from checkpoints vs values logged by 03b

| modality   | model           |   max_abs_threshold_difference |
|:-----------|:----------------|-------------------------------:|
| cytology   | ConvNeXt-Small  |                              0 |
| cytology   | DenseNet-121    |                              0 |
| cytology   | EfficientNet-B3 |                              0 |
| cytology   | ResNet-50       |                              0 |
| cytology   | Swin-Tiny       |                              0 |
| ultrasound | ConvNeXt-Small  |                              0 |
| ultrasound | DenseNet-121    |                              0 |
| ultrasound | EfficientNet-B3 |                              0 |
| ultrasound | ResNet-50       |                              0 |
| ultrasound | Swin-Tiny       |                              0 |


## D1_leakage_demonstration: Same code, data and seeds; only the fold grouping unit differs (cytology)

Image-level folds let blocks from the same case fall on both sides of every fold, reproducing the original design.

| model           | design             | fold_auroc_mean_sd   | pooled_oof_auroc    |   pooled_brier |   within_cv_case_leakage |
|:----------------|:-------------------|:---------------------|:--------------------|---------------:|-------------------------:|
| ConvNeXt-Small  | case-grouped folds | 0.872 ± 0.071        | 0.868 (0.833–0.898) |          0.153 |                    0     |
| ConvNeXt-Small  | image-level folds  | 0.880 ± 0.068        | 0.866 (0.836–0.894) |          0.158 |                    0.998 |
| EfficientNet-B3 | case-grouped folds | 0.960 ± 0.023        | 0.954 (0.936–0.970) |          0.088 |                    0     |
| EfficientNet-B3 | image-level folds  | 0.976 ± 0.013        | 0.974 (0.963–0.984) |          0.068 |                    0.998 |


## D2_leakage_fold_pairs: Fold AUROC by grouping unit

| model           |   fold |   case_grouped |   image_level |
|:----------------|-------:|---------------:|--------------:|
| ConvNeXt-Small  |      1 |         0.9534 |        0.9371 |
| ConvNeXt-Small  |      2 |         0.8006 |        0.7689 |
| ConvNeXt-Small  |      3 |         0.8001 |        0.862  |
| ConvNeXt-Small  |      4 |         0.9298 |        0.9135 |
| ConvNeXt-Small  |      5 |         0.8763 |        0.9174 |
| EfficientNet-B3 |      1 |         0.9551 |        0.9564 |
| EfficientNet-B3 |      2 |         0.9882 |        0.9888 |
| EfficientNet-B3 |      3 |         0.9288 |        0.9847 |
| EfficientNet-B3 |      4 |         0.9757 |        0.9727 |
| EfficientNet-B3 |      5 |         0.9498 |        0.9775 |


## E1_shortcut_control: EfficientNet-B3 grouped 5-fold CV with the sector or the surround removed (same folds and seeds)

If the surround-only model discriminates (CI above 0.5), label information is recoverable from outside the image of the thyroid.

| input                              | fold_auroc_mean_sd   | fold_aurocs                       | pooled_oof_auroc    | ci_excludes_chance   |
|:-----------------------------------|:---------------------|:----------------------------------|:--------------------|:---------------------|
| full image                         | 0.700 ± 0.080        | 0.800, 0.584, 0.733, 0.711, 0.674 | 0.707 (0.647–0.764) | True                 |
| surround only (sector blacked out) | 0.693 ± 0.057        | 0.795, 0.676, 0.672, 0.658, 0.664 | 0.685 (0.624–0.743) | True                 |
| sector only (surround blacked out) | 0.687 ± 0.054        | 0.734, 0.665, 0.739, 0.608, 0.688 | 0.697 (0.638–0.752) | True                 |

- Figures written: ['Fig1', 'Fig2', 'Fig3', 'Fig4', 'Fig5'] (+ Grad-CAM, t-SNE and supplementary sheets from stages A, G, I).

- Release folder ready: D:\Thyroid-BHI-26\revision_round2\release — push it to GitHub, tag a release, and archive it on Zenodo for a DOI.


## H0_ddti_tirads_distribution: Original DDTI: TI-RADS field (<tirads>) by images and cases

XML files: 390; unparseable: 0; image files: 480; images without a parseable XML case: 0. Values outside 2–5 or empty are excluded from every endpoint.

| tirads    |   images |   cases |
|:----------|---------:|--------:|
| (missing) |      131 |      92 |
| 2         |       42 |      38 |
| 3         |       19 |      14 |
| 4a        |       96 |      85 |
| 4b        |       79 |      75 |
| 4c        |       68 |      56 |
| 5         |       45 |      30 |


## H1_cross_dataset_duplicates: Cross-dataset near-duplicate screen against the Pang ultrasound images (pHash Hamming)

| external      |   images |   min_hamming_to_pang |   n_le_4 |   n_le_8 |   n_le_10 |
|:--------------|---------:|----------------------:|---------:|---------:|----------:|
| TN3K_test     |      614 |                    10 |        0 |        0 |         1 |
| TN3K_trainval |     2879 |                    12 |        0 |        0 |         0 |
| DDTI_original |      480 |                     8 |        0 |        1 |        16 |


## H2_external_results: External evaluation of frozen ultrasound models (label direction pre-specified; never flipped)

| dataset       | endpoint                                | model                |   images |   cases |   negatives |   positives | auroc               | auprc               |   no_skill_auprc |   threshold_internal | sensitivity         | specificity         |   accuracy |   brier |   ece15 | cluster_unit                       |
|:--------------|:----------------------------------------|:---------------------|---------:|--------:|------------:|------------:|:--------------------|:--------------------|-----------------:|---------------------:|:--------------------|:--------------------|-----------:|--------:|--------:|:-----------------------------------|
| TN3K_test     | benign vs malignant (distributed label) | ConvNeXt-Small       |      614 |     614 |         378 |         236 | 0.486 (0.437–0.530) | 0.387 (0.337–0.445) |            0.384 |               0.4721 | 0.140 (0.096–0.187) | 0.860 (0.823–0.894) |      0.583 |   0.244 |   0.088 | image (no patient IDs distributed) |
| TN3K_test     | benign vs malignant (distributed label) | EfficientNet-B3      |      614 |     614 |         378 |         236 | 0.677 (0.634–0.717) | 0.523 (0.459–0.590) |            0.384 |               0.0062 | 0.936 (0.904–0.966) | 0.222 (0.181–0.265) |      0.497 |   0.354 |   0.343 | image (no patient IDs distributed) |
| TN3K_test     | benign vs malignant (distributed label) | Swin-Tiny            |      614 |     614 |         378 |         236 | 0.569 (0.523–0.615) | 0.430 (0.377–0.495) |            0.384 |               0.4198 | 0.097 (0.060–0.139) | 0.926 (0.899–0.951) |      0.607 |   0.237 |   0.062 | image (no patient IDs distributed) |
| TN3K_test     | benign vs malignant (distributed label) | ResNet-50            |      614 |     614 |         378 |         236 | 0.661 (0.617–0.703) | 0.516 (0.456–0.590) |            0.384 |               0.144  | 0.941 (0.908–0.967) | 0.220 (0.181–0.262) |      0.497 |   0.223 |   0.064 | image (no patient IDs distributed) |
| TN3K_test     | benign vs malignant (distributed label) | DenseNet-121         |      614 |     614 |         378 |         236 | 0.670 (0.625–0.709) | 0.541 (0.479–0.608) |            0.384 |               0.3966 | 0.894 (0.853–0.931) | 0.325 (0.280–0.374) |      0.544 |   0.335 |   0.309 | image (no patient IDs distributed) |
| TN3K_test     | benign vs malignant (distributed label) | Ensemble (mean of 5) |      614 |     614 |         378 |         236 | 0.700 (0.657–0.738) | 0.566 (0.499–0.636) |            0.384 |               0.3507 | 0.941 (0.909–0.969) | 0.325 (0.277–0.374) |      0.562 |   0.22  |   0.109 | image (no patient IDs distributed) |
| TN3K_trainval | benign vs malignant (distributed label) | ConvNeXt-Small       |     2879 |    2879 |        1905 |         974 | 0.549 (0.529–0.571) | 0.378 (0.352–0.406) |            0.338 |               0.4721 | 0.133 (0.113–0.155) | 0.901 (0.888–0.914) |      0.642 |   0.242 |   0.134 | image (no patient IDs distributed) |
| TN3K_trainval | benign vs malignant (distributed label) | EfficientNet-B3      |     2879 |    2879 |        1905 |         974 | 0.698 (0.678–0.717) | 0.510 (0.479–0.545) |            0.338 |               0.0062 | 0.938 (0.923–0.952) | 0.247 (0.227–0.266) |      0.481 |   0.337 |   0.325 | image (no patient IDs distributed) |
| TN3K_trainval | benign vs malignant (distributed label) | Swin-Tiny            |     2879 |    2879 |        1905 |         974 | 0.621 (0.599–0.643) | 0.421 (0.391–0.451) |            0.338 |               0.4198 | 0.085 (0.068–0.104) | 0.938 (0.926–0.948) |      0.65  |   0.22  |   0.047 | image (no patient IDs distributed) |
| TN3K_trainval | benign vs malignant (distributed label) | ResNet-50            |     2879 |    2879 |        1905 |         974 | 0.658 (0.637–0.679) | 0.496 (0.465–0.527) |            0.338 |               0.144  | 0.972 (0.961–0.982) | 0.123 (0.108–0.137) |      0.41  |   0.215 |   0.075 | image (no patient IDs distributed) |
| TN3K_trainval | benign vs malignant (distributed label) | DenseNet-121         |     2879 |    2879 |        1905 |         974 | 0.682 (0.662–0.701) | 0.516 (0.483–0.550) |            0.338 |               0.3966 | 0.862 (0.840–0.883) | 0.349 (0.327–0.370) |      0.523 |   0.339 |   0.324 | image (no patient IDs distributed) |
| TN3K_trainval | benign vs malignant (distributed label) | Ensemble (mean of 5) |     2879 |    2879 |        1905 |         974 | 0.718 (0.699–0.737) | 0.541 (0.506–0.574) |            0.338 |               0.3507 | 0.920 (0.903–0.937) | 0.327 (0.306–0.348) |      0.527 |   0.217 |   0.145 | image (no patient IDs distributed) |
| DDTI_original | TI-RADS 2–3 vs 4–5 (primary)            | ConvNeXt-Small       |      349 |     298 |          61 |         288 | 0.504 (0.427–0.584) | 0.842 (0.784–0.896) |            0.825 |               0.4721 | 0.010 (0.000–0.024) | 1.000 (1.000–1.000) |      0.183 |   0.269 |   0.353 | case (XML)                         |
| DDTI_original | TI-RADS 2–3 vs 4–5 (primary)            | EfficientNet-B3      |      349 |     298 |          61 |         288 | 0.528 (0.447–0.613) | 0.854 (0.798–0.903) |            0.825 |               0.0062 | 0.872 (0.830–0.910) | 0.213 (0.111–0.333) |      0.756 |   0.424 |   0.443 | case (XML)                         |
| DDTI_original | TI-RADS 2–3 vs 4–5 (primary)            | Swin-Tiny            |      349 |     298 |          61 |         288 | 0.513 (0.431–0.598) | 0.837 (0.775–0.892) |            0.825 |               0.4198 | 0.024 (0.007–0.043) | 1.000 (1.000–1.000) |      0.195 |   0.384 |   0.489 | case (XML)                         |
| DDTI_original | TI-RADS 2–3 vs 4–5 (primary)            | ResNet-50            |      349 |     298 |          61 |         288 | 0.572 (0.486–0.658) | 0.862 (0.809–0.911) |            0.825 |               0.144  | 0.108 (0.070–0.150) | 0.918 (0.846–0.980) |      0.249 |   0.694 |   0.742 | case (XML)                         |
| DDTI_original | TI-RADS 2–3 vs 4–5 (primary)            | DenseNet-121         |      349 |     298 |          61 |         288 | 0.522 (0.435–0.614) | 0.842 (0.778–0.899) |            0.825 |               0.3966 | 0.726 (0.671–0.776) | 0.344 (0.216–0.491) |      0.659 |   0.294 |   0.324 | case (XML)                         |
| DDTI_original | TI-RADS 2–3 vs 4–5 (primary)            | Ensemble (mean of 5) |      349 |     298 |          61 |         288 | 0.518 (0.436–0.605) | 0.846 (0.786–0.900) |            0.825 |               0.3507 | 0.566 (0.505–0.622) | 0.459 (0.333–0.594) |      0.547 |   0.357 |   0.45  | case (XML)                         |
| DDTI_original | TI-RADS 2–4a vs 4b–5                    | ConvNeXt-Small       |      349 |     298 |         157 |         192 | 0.506 (0.440–0.575) | 0.556 (0.478–0.647) |            0.55  |               0.4721 | 0.016 (0.000–0.036) | 1.000 (1.000–1.000) |      0.458 |   0.254 |   0.078 | case (XML)                         |
| DDTI_original | TI-RADS 2–4a vs 4b–5                    | EfficientNet-B3      |      349 |     298 |         157 |         192 | 0.546 (0.482–0.610) | 0.614 (0.532–0.693) |            0.55  |               0.0062 | 0.901 (0.856–0.943) | 0.197 (0.137–0.261) |      0.585 |   0.392 |   0.367 | case (XML)                         |
| DDTI_original | TI-RADS 2–4a vs 4b–5                    | Swin-Tiny            |      349 |     298 |         157 |         192 | 0.548 (0.482–0.616) | 0.603 (0.525–0.693) |            0.55  |               0.4198 | 0.026 (0.005–0.051) | 0.987 (0.967–1.000) |      0.458 |   0.291 |   0.216 | case (XML)                         |
| DDTI_original | TI-RADS 2–4a vs 4b–5                    | ResNet-50            |      349 |     298 |         157 |         192 | 0.590 (0.528–0.653) | 0.623 (0.545–0.709) |            0.55  |               0.144  | 0.130 (0.080–0.185) | 0.930 (0.889–0.967) |      0.49  |   0.461 |   0.467 | case (XML)                         |
| DDTI_original | TI-RADS 2–4a vs 4b–5                    | DenseNet-121         |      349 |     298 |         157 |         192 | 0.596 (0.532–0.663) | 0.635 (0.546–0.733) |            0.55  |               0.3966 | 0.766 (0.702–0.826) | 0.350 (0.274–0.433) |      0.579 |   0.267 |   0.137 | case (XML)                         |
| DDTI_original | TI-RADS 2–4a vs 4b–5                    | Ensemble (mean of 5) |      349 |     298 |         157 |         192 | 0.566 (0.504–0.632) | 0.638 (0.552–0.727) |            0.55  |               0.3507 | 0.589 (0.511–0.661) | 0.471 (0.393–0.551) |      0.536 |   0.277 |   0.175 | case (XML)                         |
| DDTI_original | TI-RADS 2 vs 4–5                        | ConvNeXt-Small       |      330 |     284 |          42 |         288 | 0.516 (0.419–0.606) | 0.886 (0.832–0.931) |            0.873 |               0.4721 | 0.010 (0.000–0.024) | 1.000 (1.000–1.000) |      0.136 |   0.272 |   0.401 | case (XML)                         |
| DDTI_original | TI-RADS 2 vs 4–5                        | EfficientNet-B3      |      330 |     284 |          42 |         288 | 0.564 (0.467–0.664) | 0.903 (0.859–0.943) |            0.873 |               0.0062 | 0.872 (0.830–0.909) | 0.262 (0.129–0.400) |      0.794 |   0.419 |   0.45  | case (XML)                         |
| DDTI_original | TI-RADS 2 vs 4–5                        | Swin-Tiny            |      330 |     284 |          42 |         288 | 0.533 (0.433–0.633) | 0.890 (0.840–0.935) |            0.873 |               0.4198 | 0.024 (0.007–0.043) | 1.000 (1.000–1.000) |      0.148 |   0.399 |   0.536 | case (XML)                         |
| DDTI_original | TI-RADS 2 vs 4–5                        | ResNet-50            |      330 |     284 |          42 |         288 | 0.559 (0.458–0.660) | 0.902 (0.856–0.942) |            0.873 |               0.144  | 0.108 (0.071–0.148) | 0.952 (0.880–1.000) |      0.215 |   0.733 |   0.789 | case (XML)                         |
| DDTI_original | TI-RADS 2 vs 4–5                        | DenseNet-121         |      330 |     284 |          42 |         288 | 0.553 (0.451–0.664) | 0.893 (0.841–0.939) |            0.873 |               0.3966 | 0.726 (0.671–0.776) | 0.429 (0.273–0.605) |      0.688 |   0.291 |   0.367 | case (XML)                         |
| DDTI_original | TI-RADS 2 vs 4–5                        | Ensemble (mean of 5) |      330 |     284 |          42 |         288 | 0.559 (0.460–0.661) | 0.899 (0.850–0.943) |            0.873 |               0.3507 | 0.566 (0.507–0.624) | 0.524 (0.375–0.694) |      0.561 |   0.368 |   0.499 | case (XML)                         |


## I1_mmd: Maximum mean discrepancy between cohorts (EfficientNet-B3 features, PCA-50, RBF kernel, 500 permutations)

| comparison                          |   mmd2 |   permutation_p |
|:------------------------------------|-------:|----------------:|
| Pang train vs Pang test (reference) | 0.0159 |          0.1637 |


## I2_image_statistics: Acquisition-level image statistics by cohort

| cohort          |   images |   median_width |   median_height |   mean_intensity |   mean_contrast_sd |   share_near_black |
|:----------------|---------:|---------------:|----------------:|-----------------:|-------------------:|-------------------:|
| Pang (internal) |      364 |           1346 |             759 |             33.1 |               37.7 |              0.474 |

- Figures written: ['Fig1', 'Fig2', 'Fig3', 'Fig4', 'Fig5', 'Fig6'] (+ Grad-CAM, t-SNE and supplementary sheets from stages A, G, I).

- Release folder ready: D:\Thyroid-BHI-26\revision_round2\release — push it to GitHub, tag a release, and archive it on Zenodo for a DOI.
