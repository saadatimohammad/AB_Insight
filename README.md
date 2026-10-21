# A/B Insight

**A/B Insight** is a Python-based tool for analyzing A/B tests and multivariant experiments with binary outcomes, such as conversions, sign-ups, or other success events.

It compares success rates, evaluates statistical significance using chi-square tests, applies the Bonferroni correction for multiple comparisons, and produces English or Persian reports in the console and Excel.

## Features

- Analyze experiments with 2 to 5 ordered variants (`A` through `E`).
- Read experiment results from CSV (`.csv`) and Excel (`.xlsx`) files.
- Compare each alternative with control `A`, or compare all pairs of variants.
- Run chi-square tests for binary success outcomes.
- Account for multiple comparisons with the Bonferroni correction.
- Report success rates, absolute differences, relative lift, and adjusted p-values.
- Identify statistically significant improvements over control in `control` mode.
- Identify a conclusive winner in `all_pairs` mode only if it significantly outperforms every other variant.
- Generate console reports and formatted Excel workbooks.
- Support English (`en`) and Persian (`fa`) report languages, including right-to-left Excel worksheets for Persian.

## Requirements

- Python 3.11 or later (the project uses Python's built-in `tomllib` module).
- Dependencies from `requirements.txt`.

The project has been developed and tested with Python 3.14; compatibility with every Python version from 3.11 onward has not been independently verified.

## Installation

**1. Clone the repository**

```bash
git clone <repository-url>
cd AB_Insight
```

Replace `<repository-url>` with the actual GitHub repository URL.

**2. Create a virtual environment**

```bash
python -m venv .venv
```

**3. Activate the virtual environment**

Windows (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
source .venv/bin/activate
```

**4. Install dependencies**

```bash
python -m pip install -r requirements.txt
```

## Input Data

A/B Insight accepts `.csv` and `.xlsx` files with the following required column names:

| Column | Description | Expected value |
|---|---|---|
| `variant` | Experiment variant identifier | Text (`A`, `B`, etc.) |
| `sample_size` | Number of observations in the variant | Positive whole number |
| `success_count` | Number of successful outcomes | Whole number from 0 to `sample_size` |

### Example Dataset

| variant | sample_size | success_count |
|---|---:|---:|
| A | 1000 | 120 |
| B | 1000 | 150 |
| C | 1000 | 180 |

The equivalent CSV file is:

```csv
variant,sample_size,success_count
A,1000,120
B,1000,150
C,1000,180
```

**Success rate** is calculated as `success_count / sample_size`. For example, 150 successes among 1,000 observations represent a 15% success rate.

### Input Requirements

- Column names must match exactly: `variant`, `sample_size`, and `success_count` (case-sensitive).
- Numeric fields must represent whole numbers. Integer-valued numbers and strings containing decimal digits are accepted by the input parser.
- The `variant` field must contain text.
- CSV files are read as UTF-8, including UTF-8 with BOM.
- For Excel files, the application reads the active worksheet.
- Completely empty Excel rows are skipped.
- The dataset is validated before statistical analysis.

### Experiment Validation Rules

- An experiment must contain **2 to 5 variants**.
- Variant names must be consecutive and in order, starting from `A`: `A, B`; `A, B, C`; and so on up to `A, B, C, D, E`.
- Sample sizes must be positive integers.
- Success counts must be non-negative integers and cannot exceed sample sizes.
- Variant names must be non-empty text.

Invalid input is rejected with an error message. For example, `A, C` is invalid because `B` is missing, and `B, A` is invalid because the order is incorrect.

## Configuration

Edit `config.toml` in the project root to select the input dataset, comparison method, significance level, report language, and output options.

```toml
[input]
file_path = "data/datasets/sample_experiment.csv"

[experiment]
comparison_mode = "control"
alpha = 0.05

[output]
language = "en"
console = true
excel = true
output_path = "data/output/results.xlsx"
```

| Setting | Description |
|---|---|
| `file_path` | Path to the experiment CSV or XLSX file |
| `comparison_mode` | `"control"` or `"all_pairs"` |
| `alpha` | Statistical significance level, greater than 0 and less than 1 |
| `language` | `"en"` for English or `"fa"` for Persian |
| `console` | Enable or disable console reporting |
| `excel` | Enable or disable Excel report generation |
| `output_path` | Destination of the Excel workbook (`.xlsx`) |

### Comparison Modes

**Control mode (`control`)** compares every alternative with control `A`.

For variants `A`, `B`, and `C`, the comparisons are:

- `A vs B`
- `A vs C`

The summary identifies the largest statistically significant increase in success rate relative to `A`, if one is found. This is an improvement over the control, not necessarily proof that the selected alternative outperforms every other alternative.

**All-pairs mode (`all_pairs`)** evaluates every possible pair of variants.

For variants `A`, `B`, and `C`, the comparisons are:

- `A vs B`
- `A vs C`
- `B vs C`

The summary identifies a **conclusive winner** only if one variant has a higher observed success rate than every other variant **and** every corresponding pairwise difference is statistically significant after the multiple-comparison adjustment. The control `A` can also be the winner.

If no variant meets this condition, the summary states that no conclusive winner was identified. This does not mean that every pairwise comparison was non-significant.

## Running the Application

From the project root, run:

```bash
python main.py
```

The application will:

1. Load `config.toml`.
2. Read and validate the experiment dataset.
3. Run the configured statistical comparisons.
4. Interpret the experiment results.
5. Display a console report and/or save an Excel report, depending on the output settings.

With the sample configuration above, the Excel report is saved to `data/output/results.xlsx`.

## Excel Report

The generated workbook includes three worksheets:

| Worksheet | Contents |
|---|---|
| **Summary** | Comparison mode, significant-comparison count, success rates, improvement or winner information, and an interpretation |
| **Comparison Details** | Variant metrics, adjusted p-values, statistical conclusions, and additional pairwise results in `all_pairs` mode |
| **Guide** | Definitions and explanations of the reported metrics |

When `language = "fa"`, worksheet titles and report text are in Persian, and worksheets use right-to-left formatting.

## Statistical Methodology

A/B Insight applies chi-square tests to compare success proportions between variants. For multiple comparisons, the Bonferroni correction is used to account for the increased chance of false positives.

A statistically significant result indicates evidence of a difference under the configured statistical test and significance level. It does **not** automatically establish practical or business value. Consider effect size, sample size, experimental design, and business goals before making a decision.

## Running Tests

Run the automated test suite from the project root:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

At the time of preparing this README, the project had **142 passing automated tests**, covering validation, statistical calculations, experiment execution, reporting, localization, and winner selection.

## Technology Stack

- Python
- SciPy
- pandas
- openpyxl
- TOML (`tomllib`)
- `unittest`

## License

No license has been specified for this repository yet.
