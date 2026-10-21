
# English translations for A/B Insight reports.

LANGUAGE_CODE = "en"
LANGUAGE_NAME = "English"

CONSOLE = {
    "comparison_mode": "Comparison mode",
    "significance_level": "Significance level",
    "adjusted_alpha": "Bonferroni adjusted alpha",
    "number_of_comparisons": "Number of comparisons",
    "comparison": "Comparison",
    "success_rate": "Success rate",
    "difference": "Difference",
    "relative_lift": "Relative lift",
    "chi_square": "Chi-square statistic",
    "p_value": "P-value",
    "adjusted_p_value": "Adjusted p-value",
    "statistically_significant": "Statistically significant",
    "interpretation": "Interpretation",
    "yes": "Yes",
    "no": "No",
    "not_available": "N/A",
}

INTERPRETATIONS = {
    "significant_increase": (
        "Statistically significant increase in success rate."
    ),
    "significant_decrease": (
        "Statistically significant decrease in success rate."
    ),
    "significant_no_change": (
        "Statistically significant difference "
        "with no observed change in success rate."
    ),
    "not_significant": (
        "No statistically significant difference detected."
    ),
}

EXCEL = {
    "summary_sheet": "Summary",
    "comparison_details_sheet": "Comparison Details",
    "guide_sheet": "Guide",
    "result_overview": "Result overview",
    "value": "Value",
    "best_improvement": (
        "Best statistically supported improvement"
    ),
    "none_identified": "None identified",
    "control_variant": "Control variant",
    "comparisons": "Comparisons",
    "comparison_mode": "Comparison mode",
    "significant_comparisons": "Significant comparisons",
    "control_success_rate": "Control success rate",
    "variant_success_rate": "Variant {variant} success rate",
    "improved_variant_success_rate": (
        "Improved variant success rate"
    ),
    "success_rate_difference": "Success rate difference",
    "relative_improvement": "Relative improvement",
    "interpretation": "Interpretation",
    "control_vs_alternatives": "Control vs alternatives",
    "all_pairwise_comparisons": "All pairwise comparisons",
    "variant": "Variant",
    "role": "Role",
    "sample_size": "Sample size",
    "success_count": "Success count",
    "success_rate": "Success rate",
    "improvement_vs_control": "Improvement vs A",
    "adjusted_p_value": "Adjusted p-value",
    "statistical_conclusion": "Statistical conclusion",
    "statistical_significance": "Statistical significance",
    "control": "Control",
    "alternative": "Alternative",
    "reference": "Reference",
    "not_available": "Not available",
    "not_significant": "Not significant",
    "significant_increase": "Significant increase",
    "significant_decrease": "Significant decrease",
    "no_difference": "No difference",
    "additional_pairwise_comparisons": (
        "Additional pairwise comparisons"
    ),
    "comparison": "Comparison",
    "success_rate_a": "Success rate A",
    "success_rate_b": "Success rate B",
    "difference": "Difference",
    "metric": "Metric",
    "meaning": "Meaning",
}

GUIDE = {
    "success_rate": (
        "Success count divided by sample size."
    ),
    "improvement_vs_control": (
        "Relative change in success rate "
        "compared with control A."
    ),
    "success_rate_difference": (
        "Difference between two success rates; "
        "shown as a percentage, equivalent to "
        "percentage-point change."
    ),
    "relative_improvement": (
        "How much higher the success rate is "
        "relative to the baseline rate."
    ),
    "adjusted_p_value": (
        "Statistical evidence after accounting "
        "for multiple comparisons. Smaller values "
        "indicate stronger evidence against "
        "equal success rates."
    ),
    "statistical_significance": (
        "Whether the observed difference passes "
        "the configured statistical threshold."
    ),
    "reference": (
        "The control variant used as the baseline."
    ),
}

SUMMARY_INTERPRETATIONS = {
    "no_significant_difference": (
        "No statistically significant difference "
        "was identified among the tested comparisons. "
        "Observed success rate differences are not "
        "sufficient to establish an improvement."
    ),
    "no_significant_improvement": (
        "No statistically significant improvement "
        "was identified. Some comparisons showed "
        "a statistically significant decrease."
    ),
    "relative_undefined": (
        "Relative improvement is undefined "
        "because the baseline success rate is zero"
    ),
    "relative_improvement": (
        "equivalent to a {value} relative improvement"
    ),
    "best_improvement": (
        "Variant {variant_b} achieved a {rate_b} "
        "success rate compared with {rate_a} "
        "for Variant {variant_a}. "
        "The difference is {difference} "
        "percentage points, {relative_text}, "
        "and is statistically significant."
    ),
    "other_not_significant": (
        "The following comparisons were "
        "not statistically significant: {comparisons}."
    ),
}
