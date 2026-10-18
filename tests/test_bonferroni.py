
import unittest

from statistics.bonferroni import apply_bonferroni


class TestBonferroni(unittest.TestCase):

    def test_multiple_comparisons(self):
        result = apply_bonferroni([0.01, 0.03, 0.04])

        self.assertEqual(result["number_of_tests"], 3)
        self.assertAlmostEqual(
            result["adjusted_alpha"], 0.05 / 3
        )
        self.assertEqual(
            result["adjusted_p_values"],
            [0.03, 0.09, 0.12]
        )
        self.assertEqual(
            result["significant_results"],
            [True, False, False]
        )

    def test_single_comparison(self):
        result = apply_bonferroni([0.03])

        self.assertEqual(result["number_of_tests"], 1)
        self.assertAlmostEqual(result["adjusted_alpha"], 0.05)
        self.assertEqual(result["significant_results"], [True])

    def test_adjusted_p_value_cannot_exceed_one(self):
        result = apply_bonferroni([0.4, 0.6, 0.8])

        self.assertEqual(
            result["adjusted_p_values"],
            [1.0, 1.0, 1.0]
        )

    def test_custom_alpha(self):
        result = apply_bonferroni([0.01, 0.03], alpha=0.10)

        self.assertAlmostEqual(result["adjusted_alpha"], 0.05)
        self.assertEqual(
            result["significant_results"],
            [True, True]
        )

    def test_empty_p_values(self):
        with self.assertRaises(ValueError):
            apply_bonferroni([])

    def test_invalid_alpha(self):
        for alpha in [0, 1, -0.05, 1.5]:
            with self.subTest(alpha=alpha):
                with self.assertRaises(ValueError):
                    apply_bonferroni([0.01], alpha=alpha)

    def test_invalid_p_values(self):
        for p_value in [-0.1, 1.2]:
            with self.subTest(p_value=p_value):
                with self.assertRaises(ValueError):
                    apply_bonferroni([p_value])

    def test_p_value_equal_to_threshold(self):
        result = apply_bonferroni([0.025, 0.04])

        self.assertEqual(
            result["significant_results"],
            [False, False]
        )


if __name__ == "__main__":
    unittest.main()
