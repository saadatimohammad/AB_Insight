
import csv
import tempfile
import unittest
from pathlib import Path

from openpyxl import Workbook

from inputs.file_reader import (
    parse_integer,
    parse_rows,
    read_experiment_file,
)


class TestFileReader(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.directory = Path(self.temp_dir.name)

        self.valid_rows = [
            {
                "variant": "A",
                "sample_size": 1000,
                "success_count": 120,
            },
            {
                "variant": "B",
                "sample_size": 1000,
                "success_count": 150,
            },
            {
                "variant": "C",
                "sample_size": 1000,
                "success_count": 180,
            },
        ]

    def tearDown(self):
        self.temp_dir.cleanup()

    def create_csv(self, filename, rows, headers=None):
        path = self.directory / filename

        if headers is None:
            headers = [
                "variant",
                "sample_size",
                "success_count",
            ]

        with path.open(
            "w",
            encoding="utf-8",
            newline="",
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=headers,
            )
            writer.writeheader()
            writer.writerows(rows)

        return path

    def create_excel(self, filename, rows):
        path = self.directory / filename

        workbook = Workbook()
        worksheet = workbook.active

        worksheet.append([
            "variant",
            "sample_size",
            "success_count",
        ])

        for row in rows:
            worksheet.append([
                row["variant"],
                row["sample_size"],
                row["success_count"],
            ])

        workbook.save(path)
        workbook.close()

        return path

    def test_parse_valid_integer(self):
        self.assertEqual(
            parse_integer("1000", "sample_size"),
            1000,
        )
        self.assertEqual(
            parse_integer(1000.0, "sample_size"),
            1000,
        )

    def test_reject_invalid_integer(self):
        for value in ["abc", 10.5, True, None]:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    parse_integer(value, "sample_size")

    def test_parse_valid_rows(self):
        variants = parse_rows(self.valid_rows)

        self.assertEqual(len(variants), 3)
        self.assertEqual(
            [variant.name for variant in variants],
            ["A", "B", "C"],
        )
        self.assertEqual(variants[0].success_count, 120)

    def test_empty_rows(self):
        with self.assertRaises(ValueError):
            parse_rows([])

    def test_missing_required_column(self):
        rows = [
            {
                "variant": "A",
                "sample_size": 1000,
            }
        ]

        with self.assertRaises(ValueError):
            parse_rows(rows)

    def test_invalid_success_count(self):
        rows = [
            {
                "variant": "A",
                "sample_size": 100,
                "success_count": 120,
            },
            {
                "variant": "B",
                "sample_size": 100,
                "success_count": 20,
            },
        ]

        with self.assertRaises(ValueError):
            parse_rows(rows)

    def test_read_csv(self):
        path = self.create_csv(
            "experiment.csv",
            self.valid_rows,
        )

        variants = read_experiment_file(str(path))

        self.assertEqual(len(variants), 3)
        self.assertEqual(variants[1].name, "B")
        self.assertEqual(variants[1].success_count, 150)

    def test_read_excel(self):
        path = self.create_excel(
            "experiment.xlsx",
            self.valid_rows,
        )

        variants = read_experiment_file(str(path))

        self.assertEqual(len(variants), 3)
        self.assertEqual(variants[2].name, "C")
        self.assertEqual(variants[2].success_count, 180)

    def test_file_not_found(self):
        path = self.directory / "missing.csv"

        with self.assertRaises(FileNotFoundError):
            read_experiment_file(str(path))

    def test_unsupported_format(self):
        path = self.directory / "experiment.txt"
        path.write_text("test", encoding="utf-8")

        with self.assertRaises(ValueError):
            read_experiment_file(str(path))

    def test_invalid_variant_order(self):
        rows = [
            {
                "variant": "B",
                "sample_size": 100,
                "success_count": 20,
            },
            {
                "variant": "A",
                "sample_size": 100,
                "success_count": 10,
            },
        ]

        with self.assertRaises(ValueError):
            parse_rows(rows)


if __name__ == "__main__":
    unittest.main()
