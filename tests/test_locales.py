
import unittest

from reports.locales import en
from reports.locales.manager import (
    DEFAULT_LANGUAGE,
    SUPPORTED_LANGUAGES,
    get_locale,
    get_translations,
)


class TestLocales(unittest.TestCase):

    def test_default_language(self):
        self.assertEqual(DEFAULT_LANGUAGE, "en")

    def test_english_is_supported(self):
        self.assertIn("en", SUPPORTED_LANGUAGES)

    def test_get_default_locale(self):
        self.assertIs(get_locale(), en)

    def test_get_english_locale(self):
        self.assertIs(get_locale("en"), en)

    def test_language_is_case_insensitive(self):
        self.assertIs(get_locale("EN"), en)

    def test_language_whitespace_is_removed(self):
        self.assertIs(get_locale("  en  "), en)

    def test_unsupported_language(self):
        with self.assertRaisesRegex(
            ValueError,
            "Unsupported report language",
        ):
            get_locale("de")

    def test_invalid_language_type(self):
        with self.assertRaisesRegex(
            ValueError,
            "Report language must be a string",
        ):
            get_locale(None)

    def test_get_console_translations(self):
        translations = get_translations("CONSOLE", "en")

        self.assertEqual(
            translations["comparison_mode"],
            "Comparison mode",
        )

    def test_get_excel_translations(self):
        translations = get_translations("EXCEL", "en")

        self.assertEqual(
            translations["summary_sheet"],
            "Summary",
        )

    def test_get_guide_translations(self):
        translations = get_translations("GUIDE", "en")

        self.assertIn(
            "success_rate",
            translations,
        )

    def test_get_interpretation_translations(self):
        translations = get_translations(
            "INTERPRETATIONS",
            "en",
        )

        self.assertIn(
            "significant_increase",
            translations,
        )

    def test_get_summary_interpretations(self):
        translations = get_translations(
            "SUMMARY_INTERPRETATIONS",
            "en",
        )

        self.assertIn(
            "best_improvement",
            translations,
        )

    def test_missing_translation_section(self):
        with self.assertRaisesRegex(
            ValueError,
            "Translation section",
        ):
            get_translations("UNKNOWN", "en")


if __name__ == "__main__":
    unittest.main()
