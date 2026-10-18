
from core.models import BinaryVariant
from config import MIN_VARIANTS, MAX_VARIANTS, ALLOWED_VARIANTS


def validate_variant(variant: BinaryVariant) -> None:
    if not isinstance(variant.name, str) or not variant.name.strip():
        raise ValueError("Variant name must be a non-empty string.")

    if type(variant.sample_size) is not int:
        raise TypeError("Sample size must be an integer.")

    if type(variant.success_count) is not int:
        raise TypeError("Success count must be an integer.")

    if variant.sample_size <= 0:
        raise ValueError("Sample size must be greater than zero.")

    if variant.success_count < 0:
        raise ValueError("Success count cannot be negative.")

    if variant.success_count > variant.sample_size:
        raise ValueError("Success count cannot exceed sample size.")


def validate_experiment(variants: list[BinaryVariant]) -> None:
    if not isinstance(variants, list):
        raise TypeError("Variants must be provided as a list.")

    if not MIN_VARIANTS <= len(variants) <= MAX_VARIANTS:
        raise ValueError(
            f"Experiment must contain between "
            f"{MIN_VARIANTS} and {MAX_VARIANTS} variants."
        )

    expected_names = list(ALLOWED_VARIANTS[:len(variants)])
    actual_names = []

    for variant in variants:
        if not isinstance(variant, BinaryVariant):
            raise TypeError("Each variant must be a BinaryVariant.")

        validate_variant(variant)
        actual_names.append(variant.name)

    if actual_names != expected_names:
        raise ValueError(
            f"Variant names must be {expected_names} in order."
        )
