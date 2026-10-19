
from config import (
    DEFAULT_ALPHA,
    MIN_VARIANTS,
    MAX_VARIANTS,
    ALLOWED_VARIANTS,
)
from core.models import BinaryVariant
from core.validator import validate_experiment


def read_integer(prompt: str, minimum: int, maximum: int | None = None) -> int:
    while True:
        value = input(prompt).strip()

        try:
            number = int(value)
        except ValueError:
            print("Please enter a valid integer.")
            continue

        if number < minimum:
            print(f"Value must be at least {minimum}.")
            continue

        if maximum is not None and number > maximum:
            print(f"Value must not exceed {maximum}.")
            continue

        return number


def read_alpha() -> float:
    while True:
        value = input(
            f"Significance level [{DEFAULT_ALPHA}]: "
        ).strip()

        if not value:
            return DEFAULT_ALPHA

        try:
            alpha = float(value)
        except ValueError:
            print("Please enter a valid number.")
            continue

        if not 0 < alpha < 1:
            print("Significance level must be between 0 and 1.")
            continue

        return alpha


def read_comparison_mode() -> str:
    while True:
        mode = input(
            "Comparison mode (control/all_pairs) [control]: "
        ).strip().lower()

        if not mode:
            return "control"

        if mode in ("control", "all_pairs"):
            return mode

        print("Please enter 'control' or 'all_pairs'.")


def read_manual_experiment() -> dict:
    print("\n=== A/B Insight: Manual Data Entry ===\n")

    number_of_variants = read_integer(
        f"Number of variants ({MIN_VARIANTS}-{MAX_VARIANTS}): ",
        minimum=MIN_VARIANTS,
        maximum=MAX_VARIANTS,
    )

    variants = []

    for name in ALLOWED_VARIANTS[:number_of_variants]:
        print(f"\nVariant {name}")

        sample_size = read_integer(
            "Sample size: ",
            minimum=1,
        )

        success_count = read_integer(
            "Success count: ",
            minimum=0,
            maximum=sample_size,
        )

        variants.append(
            BinaryVariant(
                name=name,
                sample_size=sample_size,
                success_count=success_count,
            )
        )

    validate_experiment(variants)

    print()
    comparison_mode = read_comparison_mode()
    alpha = read_alpha()

    return {
        "variants": variants,
        "comparison_mode": comparison_mode,
        "alpha": alpha,
    }


if __name__ == "__main__":
    experiment = read_manual_experiment()
    print("\nCollected experiment data:")
    print(experiment)
