from __future__ import annotations
import numpy as np


def _matrix(x):
    x = np.asarray(x, float)
    if x.ndim != 2 or len(x) < 2 or not np.isfinite(x).all(): raise ValueError("embeddings must be a finite 2D matrix")
    return x


def distances(a, b):
    a, b = _matrix(a), _matrix(b)
    return np.maximum((a * a).sum(1)[:, None] + (b * b).sum(1)[None, :] - 2 * a @ b.T, 0)


def balanced_accuracy(true, predicted):
    labels = sorted(set(true)); scores = []
    for label in labels:
        idx = [i for i, value in enumerate(true) if value == label]
        scores.append(sum(predicted[i] == label for i in idx) / len(idx))
    return float(np.mean(scores))


def cross_species_knn(embedding, species, labels, reference):
    embedding = _matrix(embedding)
    ref = np.array([s == reference for s in species]); query = ~ref
    if not ref.any() or not query.any(): raise ValueError("reference and query species are required")
    d = distances(embedding[query], embedding[ref])
    reference_labels = np.asarray(labels)[ref]
    predicted = reference_labels[d.argmin(1)].tolist()
    truth = np.asarray(labels)[query].tolist()
    confidence = (-np.sqrt(d.min(1))).tolist()
    return truth, predicted, confidence


def species_entropy(embedding, species, labels, k=15):
    embedding = _matrix(embedding); species = np.asarray(species); labels = np.asarray(labels)
    d = distances(embedding, embedding); np.fill_diagonal(d, np.inf)
    values = []
    for i in range(len(embedding)):
        candidates = np.where(labels == labels[i])[0]; candidates = candidates[candidates != i]
        if not len(candidates): continue
        near = candidates[np.argsort(d[i, candidates])[: min(k, len(candidates))]]
        counts = np.array([(species[near] == value).sum() for value in np.unique(species)], float)
        p = counts[counts > 0] / counts.sum()
        values.append(float(-(p * np.log(p)).sum() / np.log(len(np.unique(species)))))
    return float(np.mean(values)) if values else float("nan")


def rankdata(values):
    order = np.argsort(values, kind="mergesort"); ranks = np.empty(len(values), float)
    start = 0
    while start < len(values):
        end = start + 1
        while end < len(values) and values[order[end]] == values[order[start]]: end += 1
        ranks[order[start:end]] = (start + end - 1) / 2
        start = end
    return ranks


def spearman(a, b):
    a, b = rankdata(np.asarray(a, float)), rankdata(np.asarray(b, float))
    if a.std() == 0 or b.std() == 0: return float("nan")
    return float(np.corrcoef(a, b)[0, 1])


def stage_ordering(embedding, stages, labels):
    embedding = _matrix(embedding); stages = np.asarray(stages, float); labels = np.asarray(labels)
    scores = []
    for label in sorted(set(labels)):
        idx = np.where(labels == label)[0]
        if len(idx) < 3 or len(set(stages[idx])) < 2: continue
        centered = embedding[idx] - embedding[idx].mean(0)
        _, _, vt = np.linalg.svd(centered, full_matrices=False)
        scores.append(abs(spearman(centered @ vt[0], stages[idx])))
    return float(np.nanmean(scores)) if scores else float("nan")


def auroc(labels, scores):
    labels = np.asarray(labels, bool); scores = np.asarray(scores, float)
    pos, neg = scores[labels], scores[~labels]
    if not len(pos) or not len(neg): return float("nan")
    return float(np.mean([(x > y) + 0.5 * (x == y) for x in pos for y in neg]))
