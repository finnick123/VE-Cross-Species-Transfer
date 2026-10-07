# VEC Cross-Species Transfer Lab

A compact benchmark for deciding whether a cross-species embryonic representation is useful for Virtual Embryo modeling.

External atlases can add developmental states that are absent from released mouse training stages, but a visually mixed embedding does not establish useful transfer. This repository evaluates five separate properties:

1. retained gene coverage after orthology/model-vocabulary mapping;
2. cross-species cell-type retrieval;
3. species mixing within matched biological groups;
4. preservation of developmental ordering;
5. rejection of cell types deliberately absent from the reference species.

It compares representations rather than prescribing one integration package. PCA, scVI/scArches, SAMap, SATURN, Geneformer, scGPT or a custom embedding can all be evaluated by exporting one row per cell.

## Input

CSV columns:

```text
cell_id,species,cell_type,stage,known_in_reference,z0,z1,...
```

`stage` must be a numeric, study-specific ordering variable. Do not convert human, rabbit, pig or primate development to mouse embryonic days with a fixed arithmetic offset. `known_in_reference` is `yes` or `no` for open-set evaluation.

## Run

```bash
python3 examples/make_synthetic.py
python3 scripts/benchmark.py examples/synthetic_embeddings.csv --reference mouse --output examples/report.json
python3 scripts/audit_repository.py
python3 -m unittest discover -s tests -v
```

The report contains cross-species 1-nearest-neighbor balanced accuracy, unknown rejection AUROC, normalized neighbor species entropy and Spearman stage correlation within cell types. Use `scripts/gene_coverage.py` to report input attrition separately.

See [benchmark design](docs/design.md), [dataset protocol](docs/datasets.md), [literature](references/reading.md), and the [submission draft](SUBMISSION_TEXT.md).

MIT licensed. No external atlas or challenge expression matrices are redistributed.
