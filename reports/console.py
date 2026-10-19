
from config import PROJECT_NAME


def format_percentage(value: float) -> str:
    return f"{value * 100:.2f}%"


def format_signed_percentage(value: float) -> str:
    return f"{value:+.2f}%"


def format_percentage_points(value: float) -> str:
    return f"{value:+.2f} pp"


def format_relative_lift(value: float | None) -> str:
    if value is None:
        return "N/A"

    return format_signed_percentage(value)


def format_p_value(value: float) -> str:
    return f"{value:.6f}"


def generate_console_report(experiment_result: dict) -> str:
    lines = [
        "=" * 50,
        PROJECT_NAME.center(50),
        "=" * 50,
        f"Comparison mode: {experiment_result['comparison_mode']}",
        f"Significance level: {experiment_result['alpha']:.4f}",
        (
            "Bonferroni adjusted alpha: "
            f"{experiment_result['adjusted_alpha']:.4f}"
        ),
        (
            "Number of comparisons: "
            f"{experiment_result['number_of_comparisons']}"
        ),
    ]

    for comparison in experiment_result["comparisons"]:
        variant_a = comparison["variant_a"]
        variant_b = comparison["variant_b"]

        significant = (
            "Yes" if comparison["is_significant"] else "No"
        )

        lines.extend([
            "",
            "-" * 50,
            f"Comparison: {variant_a} vs {variant_b}",
            "-" * 50,
            (
                f"Success rate {variant_a}: "
                f"{format_percentage(comparison['success_rate_a'])}"
            ),
            (
                f"Success rate {variant_b}: "
                f"{format_percentage(comparison['success_rate_b'])}"
            ),
            (
                "Difference: "
                f"{format_percentage_points(comparison['percentage_point_difference'])}"
            ),
            (
                "Relative lift: "
                f"{format_relative_lift(comparison['relative_lift'])}"
            ),
            (
                "Chi-square statistic: "
                f"{comparison['chi2']:.4f}"
            ),
            (
                "P-value: "
                f"{format_p_value(comparison['p_value'])}"
            ),
            (
                "Adjusted p-value: "
                f"{format_p_value(comparison['adjusted_p_value'])}"
            ),
            f"Statistically significant: {significant}",
            f"Interpretation: {comparison['interpretation']}",
        ])

    return "\n".join(lines)


def print_console_report(experiment_result: dict) -> None:
    report = generate_console_report(experiment_result)
    print(report)
