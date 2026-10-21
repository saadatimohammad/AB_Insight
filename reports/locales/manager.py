
from reports.locales import en


DEFAULT_LANGUAGE = "en"

SUPPORTED_LANGUAGES = {
    "en": en,
}


def get_locale(language: str = DEFAULT_LANGUAGE):
    if not isinstance(language, str):
        raise ValueError(
            "Report language must be a string."
        )

    language = language.strip().lower()

    if language not in SUPPORTED_LANGUAGES:
        supported = ", ".join(SUPPORTED_LANGUAGES)

        raise ValueError(
            f"Unsupported report language: {language}. "
            f"Supported languages: {supported}."
        )

    return SUPPORTED_LANGUAGES[language]


def get_translations(
    section: str,
    language: str = DEFAULT_LANGUAGE,
) -> dict:
    locale = get_locale(language)

    if not hasattr(locale, section):
        raise ValueError(
            f"Translation section '{section}' "
            f"is not available for language '{language}'."
        )

    return getattr(locale, section)