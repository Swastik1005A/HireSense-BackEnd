import re
from typing import Dict, List


# Matches:
# 3 years
# 3+ years
# 2-4 years
# 5 yrs experience
YEAR_PATTERN = re.compile(
    r'(\d+)\s*(\+|\-)?\s*(\d+)?\s*(years|year|yrs|yr)',
    re.IGNORECASE
)

# Matches:
# 6 months
# 10 month internship
MONTH_PATTERN = re.compile(
    r'(\d+)\s*(months|month)',
    re.IGNORECASE
)

# Matches date ranges:
# 2019 - 2022
# 2020 to 2023
DATE_RANGE_PATTERN = re.compile(
    r'(20\d{2})\s*(\-|to)\s*(20\d{2})',
    re.IGNORECASE
)


def _parse_year_match(match) -> float:
    """
    Handles:
    3 years
    3+ years
    2-4 years
    """

    first_number = int(match.group(1))
    range_symbol = match.group(2)
    second_number = match.group(3)

    if range_symbol == "-" and second_number:
        return (first_number + int(second_number)) / 2

    return float(first_number)


def extract_experience_years(text: str) -> Dict:

    text = text.lower()

    years_found: List[float] = []
    raw_matches: List[str] = []

    # -------- Year phrases --------
    for match in YEAR_PATTERN.finditer(text):
        raw_matches.append(match.group(0))
        years_found.append(_parse_year_match(match))

    # -------- Month phrases --------
    for match in MONTH_PATTERN.finditer(text):
        raw_matches.append(match.group(0))
        months = int(match.group(1))
        years_found.append(months / 12)

    # -------- Date ranges --------
    for match in DATE_RANGE_PATTERN.finditer(text):

        start_year = int(match.group(1))
        end_year = int(match.group(3))

        duration = end_year - start_year

        if duration > 0:
            raw_matches.append(match.group(0))
            years_found.append(duration)

    if not years_found:
        return {
            "total_years": 0.0,
            "raw_matches": [],
            "confidence": 0.0
        }

    # Use the highest detected experience
    total_years = max(years_found)

    confidence = min(len(raw_matches) / 4, 1.0)

    return {
        "total_years": round(total_years, 2),
        "raw_matches": raw_matches,
        "confidence": round(confidence, 2)
    }