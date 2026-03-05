import re


DEGREE_PATTERNS = [
    r"bachelor",
    r"b\.?tech",
    r"b\.?sc",
    r"bca",
    r"master",
    r"m\.?tech",
    r"m\.?sc",
    r"mba",
    r"phd"
]

INSTITUTION_KEYWORDS = [
    "university",
    "college",
    "institute",
    "school",
    "academy"
]

YEAR_PATTERN = r"(20\d{2}|19\d{2})"


def extract_education(text: str):

    lines = text.split("\n")

    degree = None
    institution = None
    graduation_year = None

    for line in lines:

        line_clean = line.strip()
        line_lower = line_clean.lower()

        # ---- Detect Degree ----
        if degree is None:
            for pattern in DEGREE_PATTERNS:
                if re.search(pattern, line_lower):
                    degree = line_clean
                    break

        # ---- Detect Institution ----
        if institution is None:
            for keyword in INSTITUTION_KEYWORDS:
                if keyword in line_lower:
                    institution = line_clean
                    break

        # ---- Detect Graduation Year ----
        if graduation_year is None:
            year_match = re.search(YEAR_PATTERN, line)
            if year_match:
                graduation_year = int(year_match.group(0))

        # Stop early if everything found
        if degree and institution and graduation_year:
            break

    return {
        "degree": degree,
        "institution": institution,
        "graduation_year": graduation_year
    }