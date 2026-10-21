
import unittest
from pathlib import Path
from unittest.mock import patch

from core.models import BinaryVariant
from main import main


class TestMain(unittest.TestCase):

    def setUp(self):
        self.variants = [
            BinaryVariant("A", 1000, 120),
            BinaryVariant("B", 1000, 150),
            BinaryVariant("C", 1000, 180),
        ]

        self.settings = {
            "file_path": Path("data/sample_experiment.csv"),
            "comparison_mode": "control",
            "alpha": 0.05,
            "console": True,
        }

    @patch("main.print_console_report")
    @patch("main.read_experiment_file")
    @patch("main.read_config")
    def test_successful_execution(
        self,
        mock_config,
        mock_file,
        mock_report,
    ):
        mock_config.return_value = self.settings
        mock_file.return_value = self.variants

        main()

        mock_config.assert_called_once_with()
        mock_file.assert_called_once_with(
            str(self.settings["file_path"])
        )
        mock_report.assert_called_once()

        result = mock_report.call_args.args[0]

        self.assertEqual(
            result["number_of_comparisons"],
            2,
        )
        self.assertEqual(
            result["comparison_mode"],
            "control",
        )

    @patch("main.print_console_report")
    @patch("main.read_experiment_file")
    @patch("main.read_config")
    def test_all_pairs_execution(
        self,
        mock_config,
        mock_file,
        mock_report,
    ):
        mock_config.return_value = {
            **self.settings,
            "comparison_mode": "all_pairs",
        }
        mock_file.return_value = self.variants

        main()

        result = mock_report.call_args.args[0]

        self.assertEqual(
            result["number_of_comparisons"],
            3,
        )

    @patch("main.print_console_report")
    @patch("main.read_experiment_file")
    @patch("main.read_config")
    def test_console_disabled(
        self,
        mock_config,
        mock_file,
        mock_report,
    ):
        mock_config.return_value = {
            **self.settings,
            "console": False,
        }
        mock_file.return_value = self.variants

        main()

        mock_report.assert_not_called()

    @patch(
        "main.read_config",
        side_effect=FileNotFoundError(
            "Configuration file not found"
        ),
    )
    def test_missing_configuration_file(self, mock_config):
        with patch("builtins.print") as mock_print:
            main()

        mock_print.assert_any_call(
            "\nError: Configuration file not found"
        )

    @patch("main.print_console_report")
    @patch(
        "main.read_experiment_file",
        side_effect=FileNotFoundError(
            "Input file not found"
        ),
    )
    @patch("main.read_config")
    def test_missing_input_file(
        self,
        mock_config,
        mock_file,
        mock_report,
    ):
        mock_config.return_value = self.settings

        with patch("builtins.print") as mock_print:
            main()

        mock_report.assert_not_called()
        mock_print.assert_any_call(
            "\nError: Input file not found"
        )

    @patch("main.print_console_report")
    @patch("main.read_experiment_file")
    @patch("main.read_config")
    def test_invalid_experiment_data(
        self,
        mock_config,
        mock_file,
        mock_report,
    ):
        mock_config.return_value = self.settings
        mock_file.return_value = [
            BinaryVariant("A", 100, 120),
            BinaryVariant("B", 100, 20),
        ]

        with patch("builtins.print") as mock_print:
            main()

        mock_report.assert_not_called()

        self.assertTrue(
            any(
                "Error:" in str(call)
                for call in mock_print.call_args_list
            )
        )


if __name__ == "__main__":
    unittest.main()
