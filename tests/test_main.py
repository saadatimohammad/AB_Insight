
import unittest
from unittest.mock import patch

from core.models import BinaryVariant
from main import (
    main,
    read_file_path,
    read_comparison_mode,
    read_alpha,
)


class TestMain(unittest.TestCase):

    @patch("builtins.input", side_effect=["", "data/test.csv"])
    def test_read_file_path_rejects_empty_input(self, mock_input):
        self.assertEqual(read_file_path(), "data/test.csv")

    @patch("builtins.input", return_value='"data/test.csv"')
    def test_read_file_path_removes_quotes(self, mock_input):
        self.assertEqual(read_file_path(), "data/test.csv")

    @patch("builtins.input", return_value="")
    def test_default_comparison_mode(self, mock_input):
        self.assertEqual(read_comparison_mode(), "control")

    @patch("builtins.input", return_value="2")
    def test_all_pairs_comparison_mode(self, mock_input):
        self.assertEqual(read_comparison_mode(), "all_pairs")

    @patch("builtins.input", side_effect=["3", "1"])
    def test_invalid_comparison_mode(self, mock_input):
        self.assertEqual(read_comparison_mode(), "control")

    @patch("builtins.input", return_value="")
    def test_default_alpha(self, mock_input):
        self.assertEqual(read_alpha(), 0.05)

    @patch("builtins.input", return_value="0.01")
    def test_custom_alpha(self, mock_input):
        self.assertEqual(read_alpha(), 0.01)

    @patch(
        "builtins.input",
        side_effect=["abc", "0", "1", "0.05"],
    )
    def test_invalid_alpha(self, mock_input):
        self.assertEqual(read_alpha(), 0.05)

    @patch(
        "builtins.input",
        side_effect=["nan", "inf", "0.05"],
    )
    def test_non_finite_alpha(self, mock_input):
        self.assertEqual(read_alpha(), 0.05)

    @patch("main.print_console_report")
    @patch("main.read_alpha", return_value=0.05)
    @patch("main.read_comparison_mode", return_value="control")
    @patch("main.read_experiment_file")
    @patch("main.read_file_path", return_value="test.csv")
    def test_main_successful_execution(
        self,
        mock_path,
        mock_file,
        mock_mode,
        mock_alpha,
        mock_report,
    ):
        mock_file.return_value = [
            BinaryVariant("A", 1000, 120),
            BinaryVariant("B", 1000, 150),
        ]

        main()

        mock_file.assert_called_once_with("test.csv")
        mock_report.assert_called_once()

        report_data = mock_report.call_args.args[0]

        self.assertEqual(
            report_data["number_of_comparisons"],
            1,
        )
        self.assertEqual(
            report_data["comparisons"][0]["variant_a"],
            "A",
        )
        self.assertEqual(
            report_data["comparisons"][0]["variant_b"],
            "B",
        )

    @patch("main.print_console_report")
    @patch(
        "main.read_experiment_file",
        side_effect=FileNotFoundError("File not found"),
    )
    @patch("main.read_file_path", return_value="missing.csv")
    def test_main_handles_missing_file(
        self,
        mock_path,
        mock_file,
        mock_report,
    ):
        with patch("builtins.print") as mock_print:
            main()

        mock_report.assert_not_called()
        mock_print.assert_any_call(
            "\nError: File not found"
        )


if __name__ == "__main__":
    unittest.main()
