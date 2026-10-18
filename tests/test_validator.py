
import unittest

from core.models import BinaryVariant
from core.validator import validate_variant, validate_experiment


class TestVariantValidation(unittest.TestCase):

    def test_valid_variant(self):
        variant = BinaryVariant("A", 100, 60)
        validate_variant(variant)

    def test_success_count_exceeds_sample_size(self):
        variant = BinaryVariant("A", 100, 150)

        with self.assertRaises(ValueError):
            validate_variant(variant)

    def test_negative_success_count(self):
        variant = BinaryVariant("A", 100, -5)

        with self.assertRaises(ValueError):
            validate_variant(variant)

    def test_zero_sample_size(self):
        variant = BinaryVariant("A", 0, 0)

        with self.assertRaises(ValueError):
            validate_variant(variant)

    def test_non_integer_sample_size(self):
        variant = BinaryVariant("A", 100.5, 60)

        with self.assertRaises(TypeError):
            validate_variant(variant)


class TestExperimentValidation(unittest.TestCase):

    def test_valid_experiment(self):
        variants = [
            BinaryVariant("A", 100, 60),
            BinaryVariant("B", 120, 84),
        ]

        validate_experiment(variants)

    def test_single_variant(self):
        variants = [
            BinaryVariant("A", 100, 60),
        ]

        with self.assertRaises(ValueError):
            validate_experiment(variants)

    def test_missing_variant_b(self):
        variants = [
            BinaryVariant("A", 100, 60),
            BinaryVariant("C", 120, 84),
        ]

        with self.assertRaises(ValueError):
            validate_experiment(variants)

    def test_duplicate_variant_names(self):
        variants = [
            BinaryVariant("A", 100, 60),
            BinaryVariant("A", 120, 84),
        ]

        with self.assertRaises(ValueError):
            validate_experiment(variants)

    def test_more_than_five_variants(self):
        variants = [
            BinaryVariant(name, 100, 50)
            for name in ["A", "B", "C", "D", "E", "F"]
        ]

        with self.assertRaises(ValueError):
            validate_experiment(variants)


if __name__ == "__main__":
    unittest.main()
