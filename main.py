
from math import isfinite

from config import PROJECT_NAME, VERSION, DEFAULT_ALPHA
from core.engine import run_experiment
from core.interpreter import interpret_experiment
from inputs.file_reader import read_experiment_file
from reports.console import print_console_report


def read_file_path() -> str:
    while True:
        file_path = input(
            "\nEnter CSV or Excel file path: "
        ).strip().strip('"').strip("'")

        if file_path:
            return file_path

        print("File path cannot be empty.")


def read_comparison_mode() -> str:
    while True:
        print("\nSelect comparison mode:")
        print("1. Compare each variant with control (A)")
        print("2. Compare all variant pairs")

        choice = input(
            "\nEnter your choice (1/2) [1]: "
        ).strip()

        if choice in ("", "1"):
            return "control"

        if choice == "2":
            return "all_pairs"

        print("Invalid choice. Please enter 1 or 2.")


def read_alpha() -> float:
    while True:
        value = input(
            f"\nSignificance level [{DEFAULT_ALPHA}]: "
        ).strip()

        if not value:
            return DEFAULT_ALPHA

        try:
            alpha = float(value)
        except ValueError:
            print("Please enter a valid number.")
            continue

        if not isfinite(alpha) or not 0 < alpha < 1:
            print(
                "Significance level must be "
                "a finite number between 0 and 1."
            )
            continue

        return alpha


def main() -> None:
    print(f"\n{PROJECT_NAME} v{VERSION}")
    print("=" * 50)

    try:
        file_path = read_file_path()

        variants = read_experiment_file(file_path)

        print(
            f"\nSuccessfully loaded {len(variants)} variants."
        )

        comparison_mode = read_comparison_mode()
        alpha = read_alpha()

        result = run_experiment(
            variants=variants,
            comparison_mode=comparison_mode,
            alpha=alpha,
        )

        interpreted_result = interpret_experiment(result)

        print()
        print_console_report(interpreted_result)

    except (ValueError, TypeError, FileNotFoundError) as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()
