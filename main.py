
import tomllib

from config import PROJECT_NAME, VERSION
from core.engine import run_experiment
from core.interpreter import interpret_experiment
from inputs.config_reader import read_config
from inputs.file_reader import read_experiment_file
from reports.console import print_console_report
from reports.excel import generate_excel_report


def main() -> None:
    print(f"\n{PROJECT_NAME} v{VERSION}")
    print("=" * 50)

    try:
        settings = read_config()

        variants = read_experiment_file(
            str(settings["file_path"])
        )

        print(
            f"\nSuccessfully loaded {len(variants)} variants."
        )

        result = run_experiment(
            variants=variants,
            comparison_mode=settings["comparison_mode"],
            alpha=settings["alpha"],
        )

        interpreted_result = interpret_experiment(result)

        if settings["console"]:
            print()
            print_console_report(interpreted_result)

        if settings["excel"]:
            report_path = generate_excel_report(
                interpreted_result,
                settings["output_path"],
            )

            print(f"\nExcel report saved to: {report_path}")

    except (
        ValueError,
        TypeError,
        FileNotFoundError,
        PermissionError,
        OSError,
        tomllib.TOMLDecodeError,
    ) as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()
