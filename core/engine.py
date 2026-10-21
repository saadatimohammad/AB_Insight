
from itertools import combinations

from core.models import BinaryVariant
from core.validator import validate_experiment
from statistical_tests.chi_square import calculate_chi_square
from statistical_tests.bonferroni import apply_bonferroni
from config import DEFAULT_ALPHA


def run_experiment(
    variants: list[BinaryVariant],
    comparison_mode: str = "control",
    alpha: float = DEFAULT_ALPHA
) -> dict:

    validate_experiment(variants)

    if comparison_mode not in ("control", "all_pairs"):
        raise ValueError(
            "Comparison mode must be 'control' or 'all_pairs'."
        )

    if comparison_mode == "control":
        control = variants[0]

        comparison_pairs = [
            (control, variant)
            for variant in variants[1:]
        ]

    else:
        comparison_pairs = list(combinations(variants, 2))

    comparisons = []
    p_values = []

    for variant_a, variant_b in comparison_pairs:

        result = calculate_chi_square(
            variant_a,
            variant_b
        )

        comparisons.append({
            "variant_a": variant_a.name,
            "variant_b": variant_b.name,
            "success_rate_a": variant_a.success_rate,
            "success_rate_b": variant_b.success_rate,
            "chi2": result["chi2"],
            "p_value": result["p_value"],
            "degrees_of_freedom": result["degrees_of_freedom"],
            "expected_frequencies": result["expected_frequencies"],
        })

        p_values.append(result["p_value"])

    correction = apply_bonferroni(
        p_values,
        alpha=alpha
    )

    for index, comparison in enumerate(comparisons):
        comparison["adjusted_p_value"] = (
            correction["adjusted_p_values"][index]
        )

        comparison["is_significant"] = (
            correction["significant_results"][index]
        )

    variant_details = [
        {
            "name": variant.name,
            "sample_size": variant.sample_size,
            "success_count": variant.success_count,
            "success_rate": variant.success_rate,
        }
        for variant in variants
    ]

    return {
        "comparison_mode": comparison_mode,
        "alpha": alpha,
        "adjusted_alpha": correction["adjusted_alpha"],
        "number_of_comparisons": correction["number_of_tests"],
        "variants": variant_details,
        "comparisons": comparisons,
    }
