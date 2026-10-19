
import unittest
from unittest.mock import patch

from inputs.manual import (
    read_integer,
    read_alpha,
    read_comparison_mode,
    read_manual_experiment,
)


class TestManualInput(unittest.TestCase):

    @patch("builtins.input", side_effect=["100"])
    def test_valid_integer(self, mock_input):
        result = read_integer("Number: ", minimum=1)

        self.assertEqual(result, 100)

    @patch("builtins.input", side_effect=["abc", "-5", "10"])
    def test_invalid_integer_then_valid(self, mock_input):
        result = read_integer("Number: ", minimum=1)

        self.assertEqual(result, 10)
        self.assertEqual(mock_input.call_count, 3)

    @patch("builtins.input", side_effect=["15", "5"])
    def test_integer_above_maximum(self, mock_input):
        result = read_integer(
            "Number: ",
            minimum=1,
            maximum=10,
        )

        self.assertEqual(result, 5)
        self.assertEqual(mock_input.call_count, 2)

    @patch("builtins.input", side_effect=[""])
    def test_default_alpha(self, mock_input):
        self.assertEqual(read_alpha(), 0.05)

    @patch("builtins.input", side_effect=["0", "1", "abc", "0.10"])
    def test_invalid_alpha_then_valid(self, mock_input):
        result = read_alpha()

        self.assertAlmostEqual(result, 0.10)
        self.assertEqual(mock_input.call_count, 4)

    @patch("builtins.input", side_effect=[""])
    def test_default_comparison_mode(self, mock_input):
        self.assertEqual(read_comparison_mode(), "control")

    @patch("builtins.input", side_effect=["wrong", "ALL_PAIRS"])
    def test_invalid_comparison_mode_then_valid(self, mock_input):
        result = read_comparison_mode()

        self.assertEqual(result, "all_pairs")
        self.assertEqual(mock_input.call_count, 2)

    @patch(
        "builtins.input",
        side_effect=[
            "3",
            "1000", "120",
            "1000", "150",
            "1000", "180",
            "control",
            "0.05",
        ],
    )
    def test_complete_manual_experiment(self, mock_input):
        result = read_manual_experiment()

        variants = result["variants"]

        self.assertEqual(len(variants), 3)
        self.assertEqual(
            [variant.name for variant in variants],
            ["A", "B", "C"],
        )
        self.assertEqual(variants[0].sample_size, 1000)
        self.assertEqual(variants[0].success_count, 120)
        self.assertEqual(variants[1].success_count, 150)
        self.assertEqual(variants[2].success_count, 180)

        self.assertEqual(result["comparison_mode"], "control")
        self.assertAlmostEqual(result["alpha"], 0.05)
        self.assertEqual(mock_input.call_count, 9)


if __name__ == "__main__":
    unittest.main()
