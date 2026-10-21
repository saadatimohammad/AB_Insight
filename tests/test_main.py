
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
            "file_path": Path(
                "data/datasets/sample_experiment.csv"
            ),
            "comparison_mode": "control",
            "alpha": 0.05,
            "language": "en",
            "console": True,
            "excel": True,
            "output_path": Path("data/output/results.xlsx"),
        }

    @patch("main.generate_excel_report")
    @patch("main.print_console_report")
    @patch("main.read_experiment_file")
    @patch("main.read_config")
    def test_successful_execution(
        self,
        mock_config,
        mock_file,
        mock_report,
        mock_excel,
    ):
        mock_config.return_value = self.settings
        mock_file.return_value = self.variants
        mock_excel.return_value = self.settings["output_path"]

        main()

        mock_config.assert_called_once_with()
        mock_file.assert_called_once_with(
            str(self.settings["file_path"])
        )

        mock_report.assert_called_once()
        mock_excel.assert_called_once()

        result = mock_report.call_args.args[0]

        self.assertEqual(
            result["number_of_comparisons"],
            2,
        )
        self.assertEqual(
            result["comparison_mode"],
            "control",
        )

        self.assertEqual(
            mock_report.call_args.kwargs,
            {"language": "en"},
        )

        excel_result = mock_excel.call_args.args[0]

        self.assertEqual(result, excel_result)
        self.assertEqual(
            mock_excel.call_args.args[1],
            self.settings["output_path"],
        )

        self.assertEqual(
            mock_excel.call_args.kwargs,
            {"language": "en"},
        )

    @patch("main.generate_excel_report")
    @patch("main.print_console_report")
    @patch("main.read_experiment_file")
    @patch("main.read_config")
    def test_all_pairs_execution(
        self,
        mock_config,
        mock_file,
        mock_report,
        mock_excel,
    ):
        mock_config.return_value = {
            **self.settings,
            "comparison_mode": "all_pairs",
        }
        mock_file.return_value = self.variants
        mock_excel.return_value = self.settings["output_path"]

        main()

        result = mock_report.call_args.args[0]

        self.assertEqual(
            result["number_of_comparisons"],
            3,
        )
        mock_excel.assert_called_once()

    @patch("main.generate_excel_report")
    @patch("main.print_console_report")
    @patch("main.read_experiment_file")
    @patch("main.read_config")
    def test_console_disabled(
        self,
        mock_config,
        mock_file,
        mock_report,
        mock_excel,
    ):
        mock_config.return_value = {
            **self.settings,
            "console": False,
        }
        mock_file.return_value = self.variants
        mock_excel.return_value = self.settings["output_path"]

        main()

        mock_report.assert_not_called()
        mock_excel.assert_called_once()

    @patch("main.generate_excel_report")
    @patch("main.print_console_report")
    @patch("main.read_experiment_file")
    @patch("main.read_config")
    def test_excel_disabled(
        self,
        mock_config,
        mock_file,
        mock_report,
        mock_excel,
    ):
        mock_config.return_value = {
            **self.settings,
            "excel": False,
        }
        mock_file.return_value = self.variants

        main()

        mock_report.assert_called_once()
        mock_excel.assert_not_called()

    @patch("main.generate_excel_report")
    @patch("main.print_console_report")
    @patch("main.read_experiment_file")
    @patch("main.read_config")
    def test_excel_output_path(
        self,
        mock_config,
        mock_file,
        mock_report,
        mock_excel,
    ):
        mock_config.return_value = self.settings
        mock_file.return_value = self.variants
        mock_excel.return_value = self.settings["output_path"]

        main()

        mock_excel.assert_called_once()

        args = mock_excel.call_args.args

        self.assertEqual(
            args[1],
            self.settings["output_path"],
        )

    @patch(
        "main.generate_excel_report",
        side_effect=PermissionError(
            "Cannot save Excel report"
        ),
    )
    @patch("main.print_console_report")
    @patch("main.read_experiment_file")
    @patch("main.read_config")
    def test_excel_save_error(
        self,
        mock_config,
        mock_file,
        mock_report,
        mock_excel,
    ):
        mock_config.return_value = self.settings
        mock_file.return_value = self.variants

        with patch("builtins.print") as mock_print:
            main()

        mock_print.assert_any_call(
            "\nError: Cannot save Excel report"
        )

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

    @patch("main.generate_excel_report")
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
        mock_excel,
    ):
        mock_config.return_value = self.settings

        with patch("builtins.print") as mock_print:
            main()

        mock_report.assert_not_called()
        mock_excel.assert_not_called()
        mock_print.assert_any_call(
            "\nError: Input file not found"
        )

    @patch("main.generate_excel_report")
    @patch("main.print_console_report")
    @patch("main.read_experiment_file")
    @patch("main.read_config")
    def test_invalid_experiment_data(
        self,
        mock_config,
        mock_file,
        mock_report,
        mock_excel,
    ):
        mock_config.return_value = self.settings
        mock_file.return_value = [
            BinaryVariant("A", 100, 120),
            BinaryVariant("B", 100, 20),
        ]

        with patch("builtins.print") as mock_print:
            main()

        mock_report.assert_not_called()
        mock_excel.assert_not_called()

        self.assertTrue(
            any(
                "Error:" in str(call)
                for call in mock_print.call_args_list
            )
        )

    @patch("main.generate_excel_report")
    @patch("main.print_console_report")
    @patch("main.read_experiment_file")
    @patch("main.read_config")
    def test_language_passed_to_reports(
        self,
        mock_config,
        mock_file,
        mock_report,
        mock_excel,
    ):
        mock_config.return_value = {
            **self.settings,
            "language": "en",
        }
        mock_file.return_value = self.variants
        mock_excel.return_value = self.settings["output_path"]

        main()

        self.assertEqual(
            mock_report.call_args.kwargs["language"],
            "en",
        )

        self.assertEqual(
            mock_excel.call_args.kwargs["language"],
            "en",
        )


if __name__ == "__main__":
    unittest.main()
