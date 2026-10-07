import unittest
import numpy as np
from vec_xspecies.metrics import auroc, balanced_accuracy, cross_species_knn, spearman, species_entropy


class MetricTests(unittest.TestCase):
    def test_balanced_accuracy(self): self.assertEqual(balanced_accuracy(["a", "a", "b"], ["a", "a", "a"]), 0.5)
    def test_auroc(self): self.assertEqual(auroc([False, False, True, True], [0, 1, 2, 3]), 1.0)
    def test_spearman(self): self.assertAlmostEqual(spearman([1, 2, 3], [4, 8, 9]), 1.0)
    def test_cross_species_retrieval(self):
        z = np.array([[0, 0], [5, 0], [.1, 0], [5.1, 0]])
        truth, pred, _ = cross_species_knn(z, ["m", "m", "r", "r"], ["a", "b", "a", "b"], "m")
        self.assertEqual(truth, pred)
        # With exactly one same-label neighbor, local entropy is necessarily zero.
        self.assertEqual(species_entropy(z, ["m", "m", "r", "r"], ["a", "b", "a", "b"], 1), 0.0)


if __name__ == "__main__": unittest.main()
