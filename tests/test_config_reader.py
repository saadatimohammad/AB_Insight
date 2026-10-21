
import math
import tempfile
import unittest
from pathlib import Path

from inputs.config_reader import read_config


class TestConfigReader(unittest.TestCase):

    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_directory.cleanup)

        self.config_path = (
            Path(self.temp_directory.name) / "config.toml"
        )

    def write_config(
        self,
        file_path="data/sample_experiment.csv",
        comparison_mode="control",
        alpha="0.05",
        console="true",
    ):
        content = f"""
[input]
file_path = "{file_path}"

[experiment]
comparison_mode = "{comparison_mode}"
alpha = {alpha}

[output]
console = {console}
"""
        self.config_path.write_text(
            content,
            encoding="utf-8",
        )

    def test_valid_configuration(self):
        self.write_config()

        settings = read_config(self.config_path)

        self.assertEqual(
            settings["comparison_mode"],
            "control",
        )
        self.assertEqual(settings["alpha"], 0.05)
        self.assertTrue(settings["console"])
        self.assertTrue(settings["file_path"].is_absolute())

    def test_all_pairs_mode(self):
        self.write_config(comparison_mode="all_pairs")

        settings = read_config(self.config_path)

        self.assertEqual(
            settings["comparison_mode"],
            "all_pairs",
        )

    def test_console_disabled(self):
        self.write_config(console="false")

        settings = read_config(self.config_path)

        self.assertFalse(settings["console"])

    def test_missing_configuration_file(self):
        missing_path = (
            Path(self.temp_directory.name) / "missing.toml"
        )

        with self.assertRaises(FileNotFoundError):
            read_config(missing_path)

    def test_missing_input_section(self):
        self.config_path.write_text(
            "[experiment]\nalpha = 0.05\n",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(
            ValueError,
            r"\[input\]",
        ):
            read_config(self.config_path)

    def test_empty_file_path(self):
        self.write_config(file_path="")

        with self.assertRaises(ValueError):
            read_config(self.config_path)

    def test_invalid_comparison_mode(self):
        self.write_config(comparison_mode="invalid")

        with self.assertRaises(ValueError):
            read_config(self.config_path)

    def test_alpha_out_of_range(self):
        for alpha in ("0", "1", "-0.1", "2"):
            with self.subTest(alpha=alpha):
                self.write_config(alpha=alpha)

                with self.assertRaises(ValueError):
                    read_config(self.config_path)

    def test_alpha_wrong_type(self):
        for alpha in ('"0.05"', "true"):
            with self.subTest(alpha=alpha):
                self.write_config(alpha=alpha)

                with self.assertRaises(ValueError):
                    read_config(self.config_path)

    def test_invalid_console_setting(self):
        self.write_config(console='"true"')

        with self.assertRaises(ValueError):
            read_config(self.config_path)

    def test_absolute_input_path(self):
        data_path = (
            Path(self.temp_directory.name) / "experiment.csv"
        )

        self.write_config(
            file_path=data_path.as_posix()
        )

        settings = read_config(self.config_path)

        self.assertEqual(
            settings["file_path"],
            data_path,
        )

    def test_invalid_toml_syntax(self):
        self.config_path.write_text(
            "[input\nfile_path = 'test.csv'",
            encoding="utf-8",
        )

        with self.assertRaises(ValueError):
            read_config(self.config_path)


if __name__ == "__main__":
    unittest.main()
