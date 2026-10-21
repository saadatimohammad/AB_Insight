
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

from reports.locales.manager import get_translations


NAVY = "17365D"
WHITE = "FFFFFF"
PALE_BLUE = "EAF1F7"
PALE_GREEN = "E2F0D9"
TEXT_COLOR = "243247"

PERCENT_FORMAT = "0.00%"
P_VALUE_FORMAT = "0.000000"


def style_header(worksheet, row_number=1):
    for cell in worksheet[row_number]:
        if cell.value is None:
            continue

        cell.fill = PatternFill(
            fill_type="solid",
            fgColor=NAVY,
        )
        cell.font = Font(
            name="Calibri",
            size=11,
            bold=True,
            color=WHITE,
        )
        cell.alignment = Alignment(
            horizontal="center",
            vertical="center",
            wrap_text=True,
        )

    worksheet.row_dimensions[row_number].height = 32


def style_body(worksheet, first_row=2):
    for row in worksheet.iter_rows(min_row=first_row):
        for cell in row:
            cell.font = Font(
                name="Calibri",
                size=11,
                color=TEXT_COLOR,
            )
            cell.alignment = Alignment(
                vertical="center",
                wrap_text=True,
            )

            if cell.row % 2 == 0:
                cell.fill = PatternFill(
                    fill_type="solid",
                    fgColor=PALE_BLUE,
                )

        if worksheet.row_dimensions[row[0].row].height is None:
            worksheet.row_dimensions[row[0].row].height = 25


def set_column_widths(worksheet, widths):
    for column, width in widths.items():
        worksheet.column_dimensions[column].width = width


def format_percentage(value):
    if value is None:
        return "N/A"

    return f"{value:.2%}"


def get_variant_details(result):
    variants = result.get("variants")

    if not isinstance(variants, list) or not variants:
        raise ValueError(
            "Experiment result must contain variant details."
        )

    return variants


def get_control_comparisons(result):
    return {
        comparison["variant_b"]: comparison
        for comparison in result["comparisons"]
        if comparison["variant_a"] == "A"
    }


def get_best_improvement(result):
    candidates = []

    for comparison in result["comparisons"]:
        difference = (
            comparison["success_rate_b"]
            - comparison["success_rate_a"]
        )

        if comparison["is_significant"] and difference > 0:
            candidates.append(comparison)

    if not candidates:
        return None

    return max(
        candidates,
        key=lambda comparison: (
            comparison["success_rate_b"]
            - comparison["success_rate_a"]
        ),
    )


def get_comparison_label(comparison):
    return (
        f'{comparison["variant_a"]} vs '
        f'{comparison["variant_b"]}'
    )


def get_improvement_label(comparison):
    return (
        f'{comparison["variant_b"]} vs '
        f'{comparison["variant_a"]}'
    )


def get_statistical_conclusion(comparison, translations):
    if not comparison["is_significant"]:
        return translations["not_significant"]

    difference = (
        comparison["success_rate_b"]
        - comparison["success_rate_a"]
    )

    if difference > 0:
        return translations["significant_increase"]

    if difference < 0:
        return translations["significant_decrease"]

    return translations["no_difference"]


def build_interpretation(result, best, translations):
    comparisons = result["comparisons"]

    if best is None:
        significant_count = sum(
            comparison["is_significant"]
            for comparison in comparisons
        )

        if significant_count:
            return translations["no_significant_improvement"]

        return translations["no_significant_difference"]

    variant_a = best["variant_a"]
    variant_b = best["variant_b"]

    rate_a = best["success_rate_a"]
    rate_b = best["success_rate_b"]

    difference = (rate_b - rate_a) * 100

    if rate_a == 0:
        relative_text = translations["relative_undefined"]
    else:
        relative_improvement = (
            (rate_b - rate_a) / rate_a
        )

        relative_text = translations[
            "relative_improvement"
        ].format(
            value=format_percentage(relative_improvement)
        )

    interpretation = translations["best_improvement"].format(
        variant_a=variant_a,
        variant_b=variant_b,
        rate_a=format_percentage(rate_a),
        rate_b=format_percentage(rate_b),
        difference=f"{difference:.2f}",
        relative_text=relative_text,
    )

    other_comparisons = [
        comparison
        for comparison in comparisons
        if comparison is not best
    ]

    not_significant = [
        comparison
        for comparison in other_comparisons
        if not comparison["is_significant"]
    ]

    if not_significant:
        labels = ", ".join(
            get_comparison_label(comparison)
            for comparison in not_significant
        )

        interpretation += (
            " "
            + translations["other_not_significant"].format(
                comparisons=labels
            )
        )

    return interpretation


def create_summary_sheet(
    workbook,
    result,
    translations,
    interpretation_translations,
):
    worksheet = workbook.active
    worksheet.title = translations["summary_sheet"]

    variants = get_variant_details(result)
    best = get_best_improvement(result)

    control = next(
        variant
        for variant in variants
        if variant["name"] == "A"
    )

    comparison_labels = ", ".join(
        get_comparison_label(comparison)
        for comparison in result["comparisons"]
    )

    comparison_mode = (
        translations["control_vs_alternatives"]
        if result["comparison_mode"] == "control"
        else translations["all_pairwise_comparisons"]
    )

    significant_count = sum(
        comparison["is_significant"]
        for comparison in result["comparisons"]
    )

    rows = [
        (
            translations["result_overview"],
            translations["value"],
        ),
        (
            translations["best_improvement"],
            (
                get_improvement_label(best)
                if best is not None
                else translations["none_identified"]
            ),
        ),
        (
            translations["control_variant"],
            "A",
        ),
        (
            translations["comparisons"],
            comparison_labels,
        ),
        (
            translations["comparison_mode"],
            comparison_mode,
        ),
        (
            translations["significant_comparisons"],
            significant_count,
        ),
        (
            translations["control_success_rate"],
            control["success_rate"],
        ),
    ]

    if best is not None:
        rows.extend([
            (
                translations["variant_success_rate"].format(
                    variant=best["variant_b"]
                ),
                best["success_rate_b"],
            ),
            (
                translations["success_rate_difference"],
                (
                    best["success_rate_b"]
                    - best["success_rate_a"]
                ),
            ),
            (
                translations["relative_improvement"],
                (
                    (
                        best["success_rate_b"]
                        - best["success_rate_a"]
                    ) / best["success_rate_a"]
                    if best["success_rate_a"] != 0
                    else None
                ),
            ),
        ])
    else:
        rows.extend([
            (
                translations["improved_variant_success_rate"],
                None,
            ),
            (
                translations["success_rate_difference"],
                None,
            ),
            (
                translations["relative_improvement"],
                None,
            ),
        ])

    rows.append((
        translations["interpretation"],
        build_interpretation(
            result,
            best,
            interpretation_translations,
        ),
    ))

    for row in rows:
        worksheet.append(row)

    style_body(worksheet)
    style_header(worksheet)

    set_column_widths(
        worksheet,
        {
            "A": 43,
            "B": 65,
        },
    )

    for row_number in (7, 8, 9, 10):
        worksheet.cell(
            row=row_number,
            column=2,
        ).number_format = PERCENT_FORMAT

    for cell in worksheet[2]:
        cell.fill = PatternFill(
            fill_type="solid",
            fgColor=PALE_GREEN,
        )
        cell.font = Font(
            name="Calibri",
            size=11,
            bold=True,
            color=TEXT_COLOR,
        )

    interpretation_row = len(rows)

    label_cell = worksheet.cell(
        row=interpretation_row,
        column=1,
    )
    text_cell = worksheet.cell(
        row=interpretation_row,
        column=2,
    )

    label_cell.font = Font(
        name="Calibri",
        size=11,
        bold=True,
        color=TEXT_COLOR,
    )

    text_cell.font = Font(
        name="Calibri",
        size=11,
        color=TEXT_COLOR,
    )

    text_cell.alignment = Alignment(
        vertical="top",
        wrap_text=True,
    )

    label_cell.alignment = Alignment(
        vertical="top",
    )

    worksheet.row_dimensions[
        interpretation_row
    ].height = max(
        75,
        16 * (
            len(str(text_cell.value)) // 65 + 2
        ),
    )

    worksheet.freeze_panes = None
    worksheet.sheet_view.showGridLines = False


def create_comparisons_sheet(
    workbook,
    result,
    translations,
):
    worksheet = workbook.create_sheet(
        translations["comparison_details_sheet"]
    )

    headers = [
        translations["variant"],
        translations["role"],
        translations["sample_size"],
        translations["success_count"],
        translations["success_rate"],
        translations["improvement_vs_control"],
        translations["adjusted_p_value"],
        translations["statistical_conclusion"],
    ]

    worksheet.append(headers)

    variants = get_variant_details(result)
    control_comparisons = get_control_comparisons(result)

    control = next(
        variant
        for variant in variants
        if variant["name"] == "A"
    )

    control_rate = control["success_rate"]

    for variant in variants:
        name = variant["name"]

        if name == "A":
            worksheet.append([
                name,
                translations["control"],
                variant["sample_size"],
                variant["success_count"],
                variant["success_rate"],
                None,
                None,
                translations["reference"],
            ])
            continue

        comparison = control_comparisons.get(name)

        if control_rate == 0:
            improvement = None
        else:
            improvement = (
                variant["success_rate"] - control_rate
            ) / control_rate

        worksheet.append([
            name,
            translations["alternative"],
            variant["sample_size"],
            variant["success_count"],
            variant["success_rate"],
            improvement,
            (
                comparison["adjusted_p_value"]
                if comparison is not None
                else None
            ),
            (
                get_statistical_conclusion(
                    comparison,
                    translations,
                )
                if comparison is not None
                else translations["not_available"]
            ),
        ])

    style_body(worksheet)
    style_header(worksheet)

    for row_number in range(2, len(variants) + 2):
        for column in (5, 6):
            worksheet.cell(
                row=row_number,
                column=column,
            ).number_format = PERCENT_FORMAT

        worksheet.cell(
            row=row_number,
            column=7,
        ).number_format = P_VALUE_FORMAT

    set_column_widths(
        worksheet,
        {
            "A": 15,
            "B": 18,
            "C": 18,
            "D": 19,
            "E": 19,
            "F": 23,
            "G": 22,
            "H": 27,
        },
    )

    if result["comparison_mode"] == "all_pairs":
        extra_comparisons = [
            comparison
            for comparison in result["comparisons"]
            if comparison["variant_a"] != "A"
        ]

        if extra_comparisons:
            start_row = len(variants) + 4

            worksheet.cell(
                row=start_row,
                column=1,
                value=translations[
                    "additional_pairwise_comparisons"
                ],
            )

            worksheet.cell(
                row=start_row,
                column=1,
            ).font = Font(
                name="Calibri",
                bold=True,
                size=12,
                color=NAVY,
            )

            header_row = start_row + 1

            extra_headers = [
                translations["comparison"],
                translations["success_rate_a"],
                translations["success_rate_b"],
                translations["difference"],
                translations["adjusted_p_value"],
                translations["statistical_conclusion"],
            ]

            for column, header in enumerate(
                extra_headers,
                start=1,
            ):
                worksheet.cell(
                    row=header_row,
                    column=column,
                    value=header,
                )

            for comparison in extra_comparisons:
                worksheet.append([
                    get_comparison_label(comparison),
                    comparison["success_rate_a"],
                    comparison["success_rate_b"],
                    (
                        comparison["success_rate_b"]
                        - comparison["success_rate_a"]
                    ),
                    comparison["adjusted_p_value"],
                    get_statistical_conclusion(
                        comparison,
                        translations,
                    ),
                ])

            for row in worksheet.iter_rows(
                min_row=header_row + 1,
                max_row=worksheet.max_row,
                max_col=6,
            ):
                for cell in row:
                    cell.font = Font(
                        name="Calibri",
                        size=11,
                        color=TEXT_COLOR,
                    )
                    cell.alignment = Alignment(
                        vertical="center",
                    )

                for index in (1, 2, 3):
                    row[index].number_format = (
                        PERCENT_FORMAT
                    )

                row[4].number_format = P_VALUE_FORMAT

            style_header(worksheet, header_row)

    worksheet.freeze_panes = None
    worksheet.auto_filter.ref = (
        f"A1:H{len(variants) + 1}"
    )
    worksheet.sheet_view.showGridLines = False


def create_guide_sheet(
    workbook,
    translations,
    guide_translations,
):
    worksheet = workbook.create_sheet(
        translations["guide_sheet"]
    )

    rows = [
        (
            translations["metric"],
            translations["meaning"],
        ),
        (
            translations["success_rate"],
            guide_translations["success_rate"],
        ),
        (
            translations["improvement_vs_control"],
            guide_translations["improvement_vs_control"],
        ),
        (
            translations["success_rate_difference"],
            guide_translations["success_rate_difference"],
        ),
        (
            translations["relative_improvement"],
            guide_translations["relative_improvement"],
        ),
        (
            translations["adjusted_p_value"],
            guide_translations["adjusted_p_value"],
        ),
        (
            translations["statistical_significance"],
            guide_translations["statistical_significance"],
        ),
        (
            translations["reference"],
            guide_translations["reference"],
        ),
    ]

    for row in rows:
        worksheet.append(row)

    style_body(worksheet)
    style_header(worksheet)

    set_column_widths(
        worksheet,
        {
            "A": 30,
            "B": 85,
        },
    )

    for row_number in range(2, len(rows) + 1):
        worksheet.row_dimensions[row_number].height = 34

    worksheet.freeze_panes = None
    worksheet.sheet_view.showGridLines = False


def generate_excel_report(
    experiment_result: dict,
    output_path: str | Path,
    language: str = "en",
) -> Path:
    translations = get_translations(
        "EXCEL",
        language,
    )

    guide_translations = get_translations(
        "GUIDE",
        language,
    )

    interpretation_translations = get_translations(
        "SUMMARY_INTERPRETATIONS",
        language,
    )

    path = Path(output_path)

    if path.suffix.lower() != ".xlsx":
        raise ValueError(
            "Excel report path must end with .xlsx."
        )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    workbook = Workbook()

    try:
        create_summary_sheet(
            workbook,
            experiment_result,
            translations,
            interpretation_translations,
        )

        create_comparisons_sheet(
            workbook,
            experiment_result,
            translations,
        )

        create_guide_sheet(
            workbook,
            translations,
            guide_translations,
        )

        workbook.save(path)
    finally:
        workbook.close()

    return path
