
def apply_bonferroni(
    p_values: list[float],
    alpha: float = 0.05
) -> dict:

    if not p_values:
        raise ValueError("At least one p-value is required.")

    if not 0 < alpha < 1:
        raise ValueError("Alpha must be between 0 and 1.")

    for p_value in p_values:
        if not 0 <= p_value <= 1:
            raise ValueError("P-values must be between 0 and 1.")

    number_of_tests = len(p_values)

    adjusted_alpha = alpha / number_of_tests

    adjusted_p_values = [
        min(p_value * number_of_tests, 1.0)
        for p_value in p_values
    ]

    significant_results = [
        p_value < adjusted_alpha
        for p_value in p_values
    ]

    return {
        "number_of_tests": number_of_tests,
        "adjusted_alpha": adjusted_alpha,
        "adjusted_p_values": adjusted_p_values,
        "significant_results": significant_results,
    }
