
from config import PROJECT_NAME
from reports.locales.manager import get_translations


def format_percentage(value: float) -> str:
    return f"{value * 100:.2f}%"


def format_signed_percentage(value: float) -> str:
    return f"{value:+.2f}%"


def format_percentage_points(value: float) -> str:
    return f"{value:+.2f} pp"


def format_relative_lift(
    value: float | None,
    language: str = "en",
) -> str:
    if value is None:
        translations = get_translations(
            "CONSOLE",
            language,
        )
        return translations["not_available"]

    return format_signed_percentage(value)


def format_p_value(value: float) -> str:
    return f"{value:.6f}"


def generate_console_report(
    experiment_result: dict,
    language: str = "en",
) -> str:
    translations = get_translations(
        "CONSOLE",
        language,
    )

    interpretations = get_translations(
        "INTERPRETATIONS",
        language,
    )

    lines = [
        "=" * 50,
        PROJECT_NAME.center(50),
        "=" * 50,
        (
            f"{translations['comparison_mode']}: "
            f"{experiment_result['comparison_mode']}"
        ),
        (
            f"{translations['significance_level']}: "
            f"{experiment_result['alpha']:.4f}"
        ),
        (
            f"{translations['adjusted_alpha']}: "
            f"{experiment_result['adjusted_alpha']:.4f}"
        ),
        (
            f"{translations['number_of_comparisons']}: "
            f"{experiment_result['number_of_comparisons']}"
        ),
    ]

    for comparison in experiment_result["comparisons"]:
        variant_a = comparison["variant_a"]
        variant_b = comparison["variant_b"]

        significant = (
            translations["yes"]
            if comparison["is_significant"]
            else translations["no"]
        )

        interpretation_key = comparison.get(
            "interpretation_key"
        )

        if interpretation_key is not None:
            interpretation = interpretations[
                interpretation_key
            ]
        else:
            interpretation = comparison["interpretation"]

        lines.extend([
            "",
            "-" * 50,
            (
                f"{translations['comparison']}: "
                f"{variant_a} vs {variant_b}"
            ),
            "-" * 50,
            (
                f"{translations['success_rate']} {variant_a}: "
                f"{format_percentage(comparison['success_rate_a'])}"
            ),
            (
                f"{translations['success_rate']} {variant_b}: "
                f"{format_percentage(comparison['success_rate_b'])}"
            ),
            (
                f"{translations['difference']}: "
                f"{format_percentage_points(comparison['percentage_point_difference'])}"
            ),
            (
                f"{translations['relative_lift']}: "
                f"{format_relative_lift(comparison['relative_lift'], language)}"
            ),
            (
                f"{translations['chi_square']}: "
                f"{comparison['chi2']:.4f}"
            ),
            (
                f"{translations['p_value']}: "
                f"{format_p_value(comparison['p_value'])}"
            ),
            (
                f"{translations['adjusted_p_value']}: "
                f"{format_p_value(comparison['adjusted_p_value'])}"
            ),
            (
                f"{translations['statistically_significant']}: "
                f"{significant}"
            ),
            (
                f"{translations['interpretation']}: "
                f"{interpretation}"
            ),
        ])

    return "\n".join(lines)


def print_console_report(
    experiment_result: dict,
    language: str = "en",
) -> None:
    report = generate_console_report(
        experiment_result,
        language=language,
    )
    print(report)
