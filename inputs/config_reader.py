
import math
import tomllib
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config.toml"


def read_config(
    config_path: str | Path = DEFAULT_CONFIG_PATH,
) -> dict:

    path = Path(config_path)

    if not path.is_file():
        raise FileNotFoundError(
            f"Configuration file not found: {path}"
        )

    with path.open("rb") as file:
        config = tomllib.load(file)

    input_settings = config.get("input")
    experiment_settings = config.get("experiment")
    output_settings = config.get("output")

    if not isinstance(input_settings, dict):
        raise ValueError(
            "Missing or invalid [input] section."
        )

    if not isinstance(experiment_settings, dict):
        raise ValueError(
            "Missing or invalid [experiment] section."
        )

    if not isinstance(output_settings, dict):
        raise ValueError(
            "Missing or invalid [output] section."
        )

    file_path = input_settings.get("file_path")

    if not isinstance(file_path, str) or not file_path.strip():
        raise ValueError(
            "Input file_path must be a non-empty string."
        )

    comparison_mode = experiment_settings.get(
        "comparison_mode"
    )

    if comparison_mode not in ("control", "all_pairs"):
        raise ValueError(
            "Comparison mode must be 'control' or 'all_pairs'."
        )

    alpha = experiment_settings.get("alpha")

    if (
        type(alpha) not in (int, float)
        or not math.isfinite(alpha)
        or not 0 < alpha < 1
    ):
        raise ValueError(
            "Alpha must be a finite number between 0 and 1."
        )

    console = output_settings.get("console")
    excel = output_settings.get("excel")
    output_path = output_settings.get("output_path")

    if type(console) is not bool:
        raise ValueError(
            "Output console must be true or false."
        )

    if type(excel) is not bool:
        raise ValueError(
            "Output excel must be true or false."
        )

    if not console and not excel:
        raise ValueError(
            "At least one output format must be enabled."
        )

    if not isinstance(output_path, str) or not output_path.strip():
        raise ValueError(
            "Output path must be a non-empty string."
        )

    data_path = Path(file_path.strip())
    report_path = Path(output_path.strip())

    if not data_path.is_absolute():
        data_path = PROJECT_ROOT / data_path

    if not report_path.is_absolute():
        report_path = PROJECT_ROOT / report_path

    if report_path.suffix.lower() != ".xlsx":
        raise ValueError(
            "Output path must end with .xlsx."
        )

    return {
        "file_path": data_path,
        "comparison_mode": comparison_mode,
        "alpha": float(alpha),
        "console": console,
        "excel": excel,
        "output_path": report_path,
    }
