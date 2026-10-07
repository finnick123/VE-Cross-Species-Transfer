import argparse, csv, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
from vec_xspecies.metrics import auroc, balanced_accuracy, cross_species_knn, species_entropy, stage_ordering


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input"); parser.add_argument("--reference", required=True); parser.add_argument("--output", required=True)
    args = parser.parse_args()
    with open(args.input, newline="", encoding="utf-8") as handle: rows = list(csv.DictReader(handle))
    zcols = sorted([c for c in rows[0] if c.startswith("z")], key=lambda x: int(x[1:]))
    z = np.array([[float(r[c]) for c in zcols] for r in rows])
    species = [r["species"] for r in rows]; labels = [r["cell_type"] for r in rows]; stages = [float(r["stage"]) for r in rows]
    truth, predicted, confidence = cross_species_knn(z, species, labels, args.reference)
    query_rows = [r for r in rows if r["species"] != args.reference]
    known = [r["known_in_reference"].lower() == "yes" for r in query_rows]
    report = {
        "reference_species": args.reference,
        "cells": len(rows),
        "dimensions": len(zcols),
        "known_type_balanced_accuracy": balanced_accuracy([t for t, k in zip(truth, known) if k], [p for p, k in zip(predicted, known) if k]),
        "unknown_rejection_auroc": auroc([not k for k in known], [-x for x in confidence]),
        "species_entropy_within_type": species_entropy(z, species, labels),
        "stage_ordering_abs_spearman": stage_ordering(z, stages, labels),
    }
    Path(args.output).write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__": main()
