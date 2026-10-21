# Persian translations for A/B Insight reports.

LANGUAGE_CODE = "fa"
LANGUAGE_NAME = "فارسی"

CONSOLE = {
    "comparison_mode": "حالت مقایسه",
    "significance_level": "سطح معناداری",
    "adjusted_alpha": "سطح معناداری تعدیل‌شده بونفرونی",
    "number_of_comparisons": "تعداد مقایسه‌ها",
    "comparison": "مقایسه",
    "success_rate": "نرخ موفقیت",
    "difference": "اختلاف",
    "relative_lift": "بهبود نسبی",
    "chi_square": "آماره کای‌دو",
    "p_value": "مقدار پی",
    "adjusted_p_value": "مقدار پی تعدیل‌شده",
    "statistically_significant": "معناداری آماری",
    "interpretation": "تفسیر",
    "yes": "بله",
    "no": "خیر",
    "not_available": "ناموجود",
}

INTERPRETATIONS = {
    "significant_increase": "افزایش نرخ موفقیت از نظر آماری معنادار است.",
    "significant_decrease": "کاهش نرخ موفقیت از نظر آماری معنادار است.",
    "significant_no_change": (
        "اختلاف از نظر آماری معنادار است، "
        "اما تغییری در نرخ موفقیت مشاهده نشده است."
    ),
    "not_significant": "اختلاف معناداری از نظر آماری شناسایی نشد.",
}

EXCEL = {
    "summary_sheet": "خلاصه نتایج",
    "comparison_details_sheet": "جزئیات مقایسه‌ها",
    "guide_sheet": "راهنما",
    "result_overview": "خلاصه نتایج",
    "value": "مقدار",
    "best_improvement": "بهترین بهبود تأییدشده از نظر آماری",
    "confirmed_winner": "برنده قطعی از نظر آماری",
    "none_identified": "موردی شناسایی نشد",
    "control_variant": "نسخه کنترل",
    "comparisons": "مقایسه‌ها",
    "comparison_mode": "حالت مقایسه",
    "significant_comparisons": "تعداد مقایسه‌های معنادار",
    "control_success_rate": "نرخ موفقیت نسخه کنترل",
    "variant_success_rate": "نرخ موفقیت نسخه {variant}",
    "improved_variant_success_rate": "نرخ موفقیت نسخه بهبودیافته",
    "winner_success_rate": "نرخ موفقیت نسخه برنده",
    "success_rate_difference": "اختلاف نرخ موفقیت",
    "winner_rate_difference": "اختلاف با نزدیک‌ترین رقیب",
    "relative_improvement": "بهبود نسبی",
    "winner_relative_improvement": "بهبود نسبی در برابر نزدیک‌ترین رقیب",
    "interpretation": "تفسیر نتایج",
    "control_vs_alternatives": "کنترل در برابر نسخه‌های جایگزین",
    "all_pairwise_comparisons": "تمام مقایسه‌های دوتایی",
    "variant": "نسخه",
    "role": "نقش",
    "sample_size": "حجم نمونه",
    "success_count": "تعداد موفقیت‌ها",
    "success_rate": "نرخ موفقیت",
    "improvement_vs_control": "بهبود نسبت به نسخه A",
    "adjusted_p_value": "مقدار پی تعدیل‌شده",
    "statistical_conclusion": "نتیجه آماری",
    "statistical_significance": "معناداری آماری",
    "control": "کنترل",
    "alternative": "جایگزین",
    "reference": "مبنای مقایسه",
    "not_available": "ناموجود",
    "not_significant": "معنادار نیست",
    "significant_increase": "افزایش معنادار",
    "significant_decrease": "کاهش معنادار",
    "no_difference": "بدون اختلاف",
    "additional_pairwise_comparisons": "مقایسه‌های دوتایی تکمیلی",
    "comparison": "مقایسه",
    "success_rate_a": "نرخ موفقیت نسخه اول",
    "success_rate_b": "نرخ موفقیت نسخه دوم",
    "difference": "اختلاف",
    "metric": "شاخص",
    "meaning": "توضیحات",
}

GUIDE = {
    "success_rate": "نسبت تعداد موفقیت‌ها به حجم نمونه.",
    "improvement_vs_control": (
        "درصد تغییر نسبی نرخ موفقیت در مقایسه با نسخه کنترل A."
    ),
    "success_rate_difference": (
        "اختلاف بین دو نرخ موفقیت که بر حسب واحد درصد نمایش داده می‌شود."
    ),
    "relative_improvement": (
        "میزان افزایش نرخ موفقیت نسبت به نرخ موفقیت نسخه مبنا."
    ),
    "adjusted_p_value": (
        "مقدار پی پس از تعدیل برای مقایسه‌های متعدد. "
        "مقادیر کوچک‌تر نشان‌دهنده شواهد آماری قوی‌تر علیه "
        "برابری نرخ‌های موفقیت هستند."
    ),
    "statistical_significance": (
        "نشان می‌دهد آیا اختلاف مشاهده‌شده از آستانه آماری تعیین‌شده عبور کرده است."
    ),
    "reference": "نسخه کنترل که به‌عنوان مبنای مقایسه استفاده می‌شود.",
}

SUMMARY_INTERPRETATIONS = {
    "no_significant_difference": (
        "در مقایسه‌های انجام‌شده هیچ اختلاف معناداری از نظر آماری شناسایی نشد. "
        "اختلاف‌های مشاهده‌شده در نرخ موفقیت برای اثبات بهبود کافی نیستند."
    ),
    "no_significant_improvement": (
        "هیچ بهبود معناداری از نظر آماری شناسایی نشد. "
        "برخی مقایسه‌ها کاهش معنادار نرخ موفقیت را نشان داده‌اند."
    ),
    "no_clear_winner": (
        "هیچ نسخه‌ای شناسایی نشد که پس از تعدیل برای مقایسه‌های متعدد، "
        "برتری نرخ موفقیت آن نسبت به تمام نسخه‌های دیگر از نظر آماری معنادار باشد. "
        "ممکن است برخی مقایسه‌های دوتایی به‌تنهایی معنادار باشند."
    ),
    "relative_undefined": (
        "بهبود نسبی قابل محاسبه نیست، زیرا نرخ موفقیت نسخه مبنا صفر است"
    ),
    "relative_improvement": "معادل {value} بهبود نسبی",
    "best_improvement": (
        "نسخه {variant_b} به نرخ موفقیت {rate_b} دست یافته است، "
        "درحالی‌که نرخ موفقیت نسخه {variant_a} برابر با {rate_a} بوده است. "
        "اختلاف برابر با {difference} واحد درصد است که {relative_text} محسوب "
        "می‌شود. این اختلاف از نظر آماری معنادار است."
    ),
    "all_pairs_winner": (
        "نسخه {variant_b} با نرخ موفقیت {rate_b} پس از تعدیل برای مقایسه‌های "
        "متعدد، از تمام نسخه‌های دیگر برتری معنادار آماری دارد. "
        "نزدیک‌ترین رقیب آن نسخه {variant_a} با نرخ موفقیت {rate_a} است. "
        "اختلاف این دو {difference} واحد درصد است که {relative_text} محسوب می‌شود."
    ),
    "other_not_significant": (
        "مقایسه‌های زیر از نظر آماری معنادار نبودند: {comparisons}."
    ),
}
