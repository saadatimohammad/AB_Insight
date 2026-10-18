
import unittest

from core.models import BinaryVariant
from statistics.chi_square import calculate_chi_square


class TestChiSquare(unittest.TestCase):

    def test_valid_chi_square(self):
        variant_a = BinaryVariant("A", 1000, 120)
        variant_b = BinaryVariant("B", 1000, 150)

        result = calculate_chi_square(variant_a, variant_b)

        self.assertAlmostEqual(
            result["chi2"],
            3.8535645472061657
        )

        self.assertAlmostEqual(
            result["p_value"],
            0.049640386865368834
        )

        self.assertEqual(result["degrees_of_freedom"], 1)

    def test_expected_frequencies(self):
        variant_a = BinaryVariant("A", 1000, 120)
        variant_b = BinaryVariant("B", 1000, 150)

        result = calculate_chi_square(variant_a, variant_b)

        self.assertEqual(
            result["expected_frequencies"],
            [[135.0, 865.0], [135.0, 865.0]]
        )

    def test_low_expected_frequencies(self):
        variant_a = BinaryVariant("A", 20, 1)
        variant_b = BinaryVariant("B", 20, 2)

        with self.assertRaises(ValueError):
            calculate_chi_square(variant_a, variant_b)

    def test_all_successes(self):
        variant_a = BinaryVariant("A", 100, 100)
        variant_b = BinaryVariant("B", 100, 100)

        with self.assertRaises(ValueError):
            calculate_chi_square(variant_a, variant_b)

    def test_all_failures(self):
        variant_a = BinaryVariant("A", 100, 0)
        variant_b = BinaryVariant("B", 100, 0)

        with self.assertRaises(ValueError):
            calculate_chi_square(variant_a, variant_b)

    def test_invalid_variant(self):
        variant_a = BinaryVariant("A", 100, 150)
        variant_b = BinaryVariant("B", 100, 50)

        with self.assertRaises(ValueError):
            calculate_chi_square(variant_a, variant_b)


if __name__ == "__main__":
    unittest.main()
