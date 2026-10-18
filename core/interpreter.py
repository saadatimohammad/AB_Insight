
def interpret_comparison(comparison: dict) -> dict:

    rate_a = comparison["success_rate_a"]
    rate_b = comparison["success_rate_b"]

    absolute_difference = rate_b - rate_a

    percentage_point_difference = absolute_difference * 100

    if rate_a == 0:
        relative_lift = None
    else:
        relative_lift = (absolute_difference / rate_a) * 100

    if rate_b > rate_a:
        direction = "increase"
    elif rate_b < rate_a:
        direction = "decrease"
    else:
        direction = "no_change"

    is_significant = comparison["is_significant"]

    if is_significant:
        if direction == "increase":
            interpretation = (
                "Statistically significant increase "
                "in success rate."
            )
        elif direction == "decrease":
            interpretation = (
                "Statistically significant decrease "
                "in success rate."
            )
        else:
            interpretation = (
                "Statistically significant difference "
                "with no observed change in success rate."
            )
    else:
        interpretation = (
            "No statistically significant difference detected."
        )

    return {
        **comparison,
        "absolute_difference": absolute_difference,
        "percentage_point_difference": percentage_point_difference,
        "relative_lift": relative_lift,
        "direction": direction,
        "interpretation": interpretation,
    }


def interpret_experiment(experiment_result: dict) -> dict:

    interpreted_comparisons = [
        interpret_comparison(comparison)
        for comparison in experiment_result["comparisons"]
    ]

    return {
        **experiment_result,
        "comparisons": interpreted_comparisons,
    }
