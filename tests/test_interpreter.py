
import unittest

from core.engine import run_experiment
from core.interpreter import (
    interpret_comparison,
    interpret_experiment,
)
from core.models import BinaryVariant


class TestInterpreter(unittest.TestCase):

    def create_comparison(
        self,
        rate_a,
        rate_b,
        is_significant=False
    ):
        return {
            "variant_a": "A",
            "variant_b": "B",
            "success_rate_a": rate_a,
            "success_rate_b": rate_b,
            "is_significant": is_significant,
        }

    def test_positive_relative_lift(self):
        comparison = self.create_comparison(0.12, 0.15)

        result = interpret_comparison(comparison)

        self.assertAlmostEqual(
            result["percentage_point_difference"], 3.0
        )
        self.assertAlmostEqual(result["relative_lift"], 25.0)
        self.assertEqual(result["direction"], "increase")

    def test_negative_relative_lift(self):
        comparison = self.create_comparison(0.20, 0.15)

        result = interpret_comparison(comparison)

        self.assertAlmostEqual(
            result["percentage_point_difference"], -5.0
        )
        self.assertAlmostEqual(result["relative_lift"], -25.0)
        self.assertEqual(result["direction"], "decrease")

    def test_no_change(self):
        comparison = self.create_comparison(0.15, 0.15)

        result = interpret_comparison(comparison)

        self.assertEqual(result["absolute_difference"], 0)
        self.assertEqual(result["relative_lift"], 0)
        self.assertEqual(result["direction"], "no_change")

    def test_zero_baseline(self):
        comparison = self.create_comparison(0.0, 0.10)

        result = interpret_comparison(comparison)

        self.assertIsNone(result["relative_lift"])
        self.assertEqual(result["direction"], "increase")

    def test_significant_increase(self):
        comparison = self.create_comparison(
            0.12, 0.18, is_significant=True
        )

        result = interpret_comparison(comparison)

        self.assertEqual(
            result["interpretation"],
            "Statistically significant increase in success rate."
        )

    def test_significant_decrease(self):
        comparison = self.create_comparison(
            0.18, 0.12, is_significant=True
        )

        result = interpret_comparison(comparison)

        self.assertEqual(
            result["interpretation"],
            "Statistically significant decrease in success rate."
        )

    def test_not_significant(self):
        comparison = self.create_comparison(0.12, 0.15)

        result = interpret_comparison(comparison)

        self.assertEqual(
            result["interpretation"],
            "No statistically significant difference detected."
        )

    def test_interpret_experiment(self):
        variants = [
            BinaryVariant("A", 1000, 120),
            BinaryVariant("B", 1000, 150),
            BinaryVariant("C", 1000, 180),
        ]

        experiment = run_experiment(variants)
        result = interpret_experiment(experiment)

        self.assertEqual(len(result["comparisons"]), 2)
        self.assertEqual(result["comparison_mode"], "control")

        first = result["comparisons"][0]
        second = result["comparisons"][1]

        self.assertFalse(first["is_significant"])
        self.assertTrue(second["is_significant"])

        self.assertAlmostEqual(first["relative_lift"], 25.0)
        self.assertAlmostEqual(second["relative_lift"], 50.0)


if __name__ == "__main__":
    unittest.main()
