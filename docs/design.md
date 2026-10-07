# Benchmark design

Evaluate representations under leave-one-species-out and leave-one-cell-type-out protocols. Hyperparameters may use labels within training species but must not use query-species labels. Report every method's measured, orthology-mapped and model-usable gene counts before embedding quality.

Cross-species retrieval measures whether query cells find the correct reference type. Species entropy is calculated within annotated cell types so biological separation is not rewarded as poor mixing. Stage ordering asks whether developmental progression remains recoverable within a type. Unknown rejection treats types absent from the reference as positives and uses distance to the closest reference cell.

No single metric is sufficient. Perfect mixing can erase species-specific biology; perfect label transfer can result from label leakage; stage correlation can be driven by technical depth. Include a species-native PCA baseline, one-to-one ortholog PCA, shuffled labels and shuffled stages.
