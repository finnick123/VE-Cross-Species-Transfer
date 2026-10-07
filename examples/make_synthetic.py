import csv
from pathlib import Path
import numpy as np

rng = np.random.default_rng(9); rows = []
for species, shift in [("mouse", 0.0), ("rabbit", 0.15)]:
    for cell_type, center in [("cardiac", np.array([0., 0.])), ("endothelial", np.array([4., 0.]))]:
        for i in range(30):
            stage = i / 10
            z = center + np.array([0.2 * stage, stage]) + shift + rng.normal(0, 0.12, 2)
            rows.append([f"{species}_{cell_type}_{i}", species, cell_type, stage, "yes", *z])
for i in range(20):
    z = np.array([8., i / 10]) + rng.normal(0, 0.12, 2)
    rows.append([f"rabbit_neural_{i}", "rabbit", "neural", i / 10, "no", *z])
path = Path(__file__).with_name("synthetic_embeddings.csv")
with path.open("w", newline="") as handle:
    writer = csv.writer(handle); writer.writerow(["cell_id", "species", "cell_type", "stage", "known_in_reference", "z0", "z1"]); writer.writerows(rows)
print(path)
