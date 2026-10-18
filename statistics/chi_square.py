
from scipy.stats import chi2_contingency

from core.models import BinaryVariant
from core.validator import validate_variant


def calculate_chi_square(
    variant_a: BinaryVariant,
    variant_b: BinaryVariant
) -> dict:

    validate_variant(variant_a)
    validate_variant(variant_b)

    contingency_table = [
        [variant_a.success_count, variant_a.failure_count],
        [variant_b.success_count, variant_b.failure_count],
    ]

    total_successes = (
        variant_a.success_count + variant_b.success_count
    )

    total_failures = (
        variant_a.failure_count + variant_b.failure_count
    )

    if total_successes == 0 or total_failures == 0:
        raise ValueError(
            "Chi-square test cannot be performed when "
            "all observations have the same outcome."
        )

    chi2, p_value, degrees_of_freedom, expected = (
        chi2_contingency(
            contingency_table,
            correction=False
        )
    )

    if (expected < 5).any():
        raise ValueError(
            "Chi-square assumptions are not satisfied: "
            "expected frequencies must be at least 5."
        )

    return {
        "chi2": float(chi2),
        "p_value": float(p_value),
        "degrees_of_freedom": int(degrees_of_freedom),
        "expected_frequencies": expected.tolist(),
    }
