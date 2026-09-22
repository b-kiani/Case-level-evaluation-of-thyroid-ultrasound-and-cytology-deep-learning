# Publishing this release (GitHub + Zenodo)

1. Fill the repository on the analysis machine (after the final Stage I rerun):
   `python tools/collect_from_local.py --root "D:\Thyroid-BHI-26" --zip-checkpoints`
2. Link Zenodo to GitHub BEFORE creating the release: https://zenodo.org -> log in with GitHub -> Account -> GitHub -> switch ON this repository.
3. Replace the old repository contents and push (Git Bash / PowerShell, in an empty working folder):
   git clone https://github.com/b-kiani/Thyroid-Cancer-Classification-2026.git
   cd Thyroid-Cancer-Classification-2026
   git rm -r -q .
   (copy every file and folder of this release into the folder, including .gitignore)
   git add -A
   git commit -m "Analysis release for BMC Medical Imaging revision 1"
   git push origin main
4. GitHub -> Releases -> Draft a new release -> tag v1.0.0 -> title "BMC Medical Imaging revision 1" -> Publish.
   Zenodo archives the release automatically and issues a DOI (Zenodo -> Upload -> the new record).
5. Upload `revision_round2\zenodo_frozen_split_checkpoints.zip` as a separate Zenodo upload (New upload), then put its DOI into `checkpoints/CHECKPOINTS.md`.
6. Put the repository URL and release DOI into the manuscript (Data availability, Code availability), the response letter, and `CITATION.cff`; commit that change as v1.0.1 if you want the DOI inside the archived copy.
