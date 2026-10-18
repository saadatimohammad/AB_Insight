
import unittest

from core.engine import run_experiment
from core.models import BinaryVariant


class TestEngine(unittest.TestCase):

    def setUp(self):
        self.variants = [
            BinaryVariant("A", 1000, 120),
            BinaryVariant("B", 1000, 150),
            BinaryVariant("C", 1000, 180),
        ]

    def test_control_comparisons(self):
        result = run_experiment(
            self.variants,
            comparison_mode="control"
        )

        self.assertEqual(result["comparison_mode"], "control")
        self.assertEqual(result["number_of_comparisons"], 2)
        self.assertAlmostEqual(result["adjusted_alpha"], 0.025)

        pairs = [
            (item["variant_a"], item["variant_b"])
            for item in result["comparisons"]
        ]

        self.assertEqual(pairs, [("A", "B"), ("A", "C")])

    def test_all_pairs_comparisons(self):
        result = run_experiment(
            self.variants,
            comparison_mode="all_pairs"
        )

        self.assertEqual(result["number_of_comparisons"], 3)

        pairs = [
            (item["variant_a"], item["variant_b"])
            for item in result["comparisons"]
        ]

        self.assertEqual(
            pairs,
            [("A", "B"), ("A", "C"), ("B", "C")]
        )

    def test_significance_after_bonferroni(self):
        result = run_experiment(self.variants)

        comparisons = result["comparisons"]

        self.assertFalse(comparisons[0]["is_significant"])
        self.assertTrue(comparisons[1]["is_significant"])

        self.assertAlmostEqual(
            comparisons[0]["adjusted_p_value"],
            comparisons[0]["p_value"] * 2
        )

    def test_single_comparison(self):
        result = run_experiment(self.variants[:2])

        self.assertEqual(result["number_of_comparisons"], 1)
        self.assertAlmostEqual(result["adjusted_alpha"], 0.05)

        comparison = result["comparisons"][0]

        self.assertAlmostEqual(
            comparison["adjusted_p_value"],
            comparison["p_value"]
        )

    def test_custom_alpha(self):
        result = run_experiment(
            self.variants,
            alpha=0.10
        )

        self.assertAlmostEqual(result["alpha"], 0.10)
        self.assertAlmostEqual(result["adjusted_alpha"], 0.05)

    def test_invalid_comparison_mode(self):
        with self.assertRaises(ValueError):
            run_experiment(
                self.variants,
                comparison_mode="invalid"
            )

    def test_invalid_experiment(self):
        with self.assertRaises(ValueError):
            run_experiment(self.variants[:1])

    def test_chi_square_assumption_failure(self):
        variants = [
            BinaryVariant("A", 100, 1),
            BinaryVariant("B", 100, 2),
        ]

        with self.assertRaises(ValueError):
            run_experiment(variants)


if __name__ == "__main__":
    unittest.main()
