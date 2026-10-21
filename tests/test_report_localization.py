
import tempfile
import unittest
from pathlib import Path
from string import Formatter
from unittest.mock import patch

from openpyxl import load_workbook

from core.engine import run_experiment
from core.interpreter import interpret_experiment
from core.models import BinaryVariant
from reports.console import generate_console_report
from reports.excel import generate_excel_report
from reports.locales import en, fa


class TestReportLocalization(unittest.TestCase):

    def setUp(self):
        variants = [
            BinaryVariant("A", 1000, 100),
            BinaryVariant("B", 1000, 200),
        ]

        result = run_experiment(
            variants=variants,
            comparison_mode="control",
            alpha=0.05,
        )

        self.result = interpret_experiment(result)

    def generate_workbook(self, language):
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)

        output_path = (
            Path(temporary_directory.name)
            / f"report_{language}.xlsx"
        )

        generate_excel_report(
            self.result,
            output_path,
            language=language,
        )

        workbook = load_workbook(output_path)
        self.addCleanup(workbook.close)

        return workbook

    def test_translation_sections_exist(self):
        sections = [
            "CONSOLE",
            "INTERPRETATIONS",
            "EXCEL",
            "GUIDE",
            "SUMMARY_INTERPRETATIONS",
        ]

        for locale in (en, fa):
            for section in sections:
                with self.subTest(
                    language=locale.LANGUAGE_CODE,
                    section=section,
                ):
                    translations = getattr(locale, section)

                    self.assertIsInstance(
                        translations,
                        dict,
                    )

                    self.assertTrue(translations)

    def test_translation_values_are_strings(self):
        sections = [
            "CONSOLE",
            "INTERPRETATIONS",
            "EXCEL",
            "GUIDE",
            "SUMMARY_INTERPRETATIONS",
        ]

        for locale in (en, fa):
            for section in sections:
                translations = getattr(locale, section)

                for key, value in translations.items():
                    with self.subTest(
                        language=locale.LANGUAGE_CODE,
                        section=section,
                        key=key,
                    ):
                        self.assertIsInstance(key, str)
                        self.assertIsInstance(value, str)
                        self.assertTrue(value.strip())

    def test_summary_translation_placeholders(self):
        required_placeholders = {
            "best_improvement": {
                "variant_a",
                "variant_b",
                "rate_a",
                "rate_b",
                "difference",
                "relative_text",
            },
            "relative_improvement": {
                "value",
            },
            "other_not_significant": {
                "comparisons",
            },
        }

        formatter = Formatter()

        for locale in (en, fa):
            for key, expected in required_placeholders.items():
                template = locale.SUMMARY_INTERPRETATIONS[key]

                actual = {
                    field_name
                    for _, field_name, _, _ in formatter.parse(
                        template
                    )
                    if field_name is not None
                }

                with self.subTest(
                    language=locale.LANGUAGE_CODE,
                    key=key,
                ):
                    self.assertEqual(actual, expected)

    def test_console_uses_translated_labels(self):
        with patch.dict(
            en.CONSOLE,
            {"comparison_mode": "TEST MODE LABEL"},
        ):
            report = generate_console_report(
                self.result,
                language="en",
            )

        self.assertIn(
            "TEST MODE LABEL:",
            report,
        )

    def test_console_uses_translated_interpretation(self):
        with patch.dict(
            en.INTERPRETATIONS,
            {
                "significant_increase": (
                    "TEST SIGNIFICANT INCREASE"
                ),
            },
        ):
            report = generate_console_report(
                self.result,
                language="en",
            )

        self.assertIn(
            "TEST SIGNIFICANT INCREASE",
            report,
        )

    def test_excel_uses_translated_content(self):
        with tempfile.TemporaryDirectory() as directory:
            output_path = (
                Path(directory) / "localized_report.xlsx"
            )

            with patch.dict(
                en.EXCEL,
                {
                    "summary_sheet": "Test Summary",
                    "result_overview": "TEST OVERVIEW",
                },
            ):
                with patch.dict(
                    en.GUIDE,
                    {
                        "success_rate": (
                            "TEST SUCCESS RATE DESCRIPTION"
                        ),
                    },
                ):
                    generate_excel_report(
                        self.result,
                        output_path,
                        language="en",
                    )

            workbook = load_workbook(output_path)

            try:
                self.assertIn(
                    "Test Summary",
                    workbook.sheetnames,
                )

                summary = workbook["Test Summary"]

                self.assertEqual(
                    summary["A1"].value,
                    "TEST OVERVIEW",
                )

                guide = workbook["Guide"]

                self.assertEqual(
                    guide["B2"].value,
                    "TEST SUCCESS RATE DESCRIPTION",
                )
            finally:
                workbook.close()

    def test_excel_uses_translated_interpretation(self):
        with tempfile.TemporaryDirectory() as directory:
            output_path = (
                Path(directory) / "interpretation.xlsx"
            )

            with patch.dict(
                en.SUMMARY_INTERPRETATIONS,
                {
                    "best_improvement": (
                        "TEST BEST IMPROVEMENT "
                        "{variant_a} {variant_b} "
                        "{rate_a} {rate_b} "
                        "{difference} {relative_text}"
                    ),
                },
            ):
                generate_excel_report(
                    self.result,
                    output_path,
                    language="en",
                )

            workbook = load_workbook(output_path)

            try:
                summary = workbook["Summary"]

                interpretation = summary["B11"].value

                self.assertIn(
                    "TEST BEST IMPROVEMENT",
                    interpretation,
                )
            finally:
                workbook.close()

    def test_reports_reject_unsupported_language(self):
        with self.assertRaises(ValueError):
            generate_console_report(
                self.result,
                language="de",
            )

        with tempfile.TemporaryDirectory() as directory:
            output_path = (
                Path(directory) / "invalid_language.xlsx"
            )

            with self.assertRaises(ValueError):
                generate_excel_report(
                    self.result,
                    output_path,
                    language="de",
                )

            self.assertFalse(output_path.exists())

    def test_persian_sheet_names(self):
        workbook = self.generate_workbook("fa")

        self.assertEqual(
            workbook.sheetnames,
            [
                fa.EXCEL["summary_sheet"],
                fa.EXCEL["comparison_details_sheet"],
                fa.EXCEL["guide_sheet"],
            ],
        )

    def test_english_sheet_names(self):
        workbook = self.generate_workbook("en")

        self.assertEqual(
            workbook.sheetnames,
            [
                en.EXCEL["summary_sheet"],
                en.EXCEL["comparison_details_sheet"],
                en.EXCEL["guide_sheet"],
            ],
        )

    def test_persian_sheets_are_right_to_left(self):
        workbook = self.generate_workbook("fa")

        for worksheet in workbook.worksheets:
            with self.subTest(sheet=worksheet.title):
                self.assertTrue(
                    worksheet.sheet_view.rightToLeft
                )

    def test_english_sheets_are_left_to_right(self):
        workbook = self.generate_workbook("en")

        for worksheet in workbook.worksheets:
            with self.subTest(sheet=worksheet.title):
                self.assertFalse(
                    worksheet.sheet_view.rightToLeft
                )

    def test_persian_cells_use_b_nazanin(self):
        workbook = self.generate_workbook("fa")

        for worksheet in workbook.worksheets:
            for row in worksheet.iter_rows():
                for cell in row:
                    if cell.value is None:
                        continue

                    with self.subTest(
                        sheet=worksheet.title,
                        cell=cell.coordinate,
                    ):
                        self.assertEqual(
                            cell.font.name,
                            "B Nazanin",
                        )

    def test_english_cells_use_calibri(self):
        workbook = self.generate_workbook("en")

        for worksheet in workbook.worksheets:
            for row in worksheet.iter_rows():
                for cell in row:
                    if cell.value is None:
                        continue

                    with self.subTest(
                        sheet=worksheet.title,
                        cell=cell.coordinate,
                    ):
                        self.assertEqual(
                            cell.font.name,
                            "Calibri",
                        )

    def test_persian_summary_comparison_format(self):
        workbook = self.generate_workbook("fa")
        worksheet = workbook[fa.EXCEL["summary_sheet"]]

        self.assertEqual(
            worksheet["B4"].value,
            "(A vs B)",
        )

    def test_english_summary_comparison_format(self):
        workbook = self.generate_workbook("en")
        worksheet = workbook[en.EXCEL["summary_sheet"]]

        self.assertEqual(
            worksheet["B4"].value,
            "(A vs B)",
        )

    def test_persian_header_keeps_bold_format(self):
        workbook = self.generate_workbook("fa")

        for worksheet in workbook.worksheets:
            with self.subTest(sheet=worksheet.title):
                self.assertTrue(
                    worksheet["A1"].font.bold
                )

                self.assertEqual(
                    worksheet["A1"].font.name,
                    "B Nazanin",
                )

    def test_english_header_keeps_bold_format(self):
        workbook = self.generate_workbook("en")

        for worksheet in workbook.worksheets:
            with self.subTest(sheet=worksheet.title):
                self.assertTrue(
                    worksheet["A1"].font.bold
                )

                self.assertEqual(
                    worksheet["A1"].font.name,
                    "Calibri",
                )


if __name__ == "__main__":
    unittest.main()
