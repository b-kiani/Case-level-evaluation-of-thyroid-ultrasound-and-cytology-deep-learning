"""Verify that the frozen case-level manifest is byte-identical to the one used for every reported analysis."""
import hashlib
from pathlib import Path

EXPECTED = "83e656eff33e272020d85f8faf4004285a67768d3ef79e040c59ee13ea1575f5"
path = Path(__file__).resolve().parents[1] / "manifests" / "04_frozen_manifest.csv"
h = hashlib.sha256(path.read_bytes()).hexdigest()
print(f"{path.name}: {h}")
print("OK: matches the manuscript" if h == EXPECTED else "MISMATCH: this is not the manifest used in the manuscript")
