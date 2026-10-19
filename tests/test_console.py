
import unittest
from unittest.mock import patch

from core.models import BinaryVariant
from core.engine import run_experiment
from core.interpreter import interpret_experiment

from reports.console import (
    format_percentage,
    format_signed_percentage,
    format_percentage_points,
    format_relative_lift,
    format_p_value,
    generate_console_report,
    print_console_report,
)


class TestConsoleReport(unittest.TestCase):

    def setUp(self):
        variants = [
            BinaryVariant("A", 1000, 120),
            BinaryVariant("B", 1000, 150),
            BinaryVariant("C", 1000, 180),
        ]

        experiment = run_experiment(
            variants,
            comparison_mode="control",
            alpha=0.05,
        )

        self.result = interpret_experiment(experiment)

    def test_format_percentage(self):
        self.assertEqual(
            format_percentage(0.12),
            "12.00%",
        )

    def test_format_signed_percentage(self):
        self.assertEqual(
            format_signed_percentage(25.0),
            "+25.00%",
        )
        self.assertEqual(
            format_signed_percentage(-10.0),
            "-10.00%",
        )

    def test_format_percentage_points(self):
        self.assertEqual(
            format_percentage_points(3.0),
            "+3.00 pp",
        )
        self.assertEqual(
            format_percentage_points(-5.0),
            "-5.00 pp",
        )

    def test_format_relative_lift(self):
        self.assertEqual(
            format_relative_lift(25.0),
            "+25.00%",
        )
        self.assertEqual(
            format_relative_lift(None),
            "N/A",
        )

    def test_format_p_value(self):
        self.assertEqual(
            format_p_value(0.049640386),
            "0.049640",
        )

    def test_report_header(self):
        report = generate_console_report(self.result)

        self.assertIn("A/B Insight", report)
        self.assertIn("Comparison mode: control", report)
        self.assertIn("Significance level: 0.0500", report)
        self.assertIn(
            "Bonferroni adjusted alpha: 0.0250",
            report,
        )
        self.assertIn("Number of comparisons: 2", report)

    def test_report_contains_comparisons(self):
        report = generate_console_report(self.result)

        self.assertIn("Comparison: A vs B", report)
        self.assertIn("Comparison: A vs C", report)

    def test_report_contains_statistical_results(self):
        report = generate_console_report(self.result)

        self.assertIn("Chi-square statistic: 3.8536", report)
        self.assertIn("Adjusted p-value: 0.099281", report)
        self.assertIn("Adjusted p-value: 0.000343", report)

    def test_report_contains_interpretations(self):
        report = generate_console_report(self.result)

        self.assertIn(
            "No statistically significant difference detected.",
            report,
        )
        self.assertIn(
            "Statistically significant increase in success rate.",
            report,
        )

    def test_report_contains_relative_lift(self):
        report = generate_console_report(self.result)

        self.assertIn("Relative lift: +25.00%", report)
        self.assertIn("Relative lift: +50.00%", report)

    @patch("builtins.print")
    def test_print_console_report(self, mock_print):
        expected_report = generate_console_report(self.result)

        print_console_report(self.result)

        mock_print.assert_called_once_with(expected_report)


if __name__ == "__main__":
    unittest.main()
