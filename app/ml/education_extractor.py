import re


DEGREE_PATTERNS = [
    r"\bbachelor\b",
    r"\bb\.?tech\b",
    r"\bb\.?sc\b",
    r"\bbca\b",
    r"\bmaster\b",
    r"\bm\.?tech\b",
    r"\bm\.?sc\b",
    r"\bmba\b",
    r"\bphd\b"
]

INSTITUTION_KEYWORDS = [
    "university",
    "college",
    "institute",
    "school",
    "academy"
]

YEAR_RANGE_PATTERN = r"(20\d{2})\s*[-–]\s*(20\d{2})"
YEAR_PATTERN = r"(20\d{2}|19\d{2})"


def clean_line(text: str):
    """
    Remove bullets and weird symbols
    """
    return re.sub(r"[•|:]", "", text).strip()


def extract_education(text: str):

    lines = text.split("\n")

    degree = None
    institution = None
    graduation_year = None

    for line in lines:

        line_clean = clean_line(line)
        line_lower = line_clean.lower()

        # ---- DEGREE DETECTION ----
        if degree is None:
            for pattern in DEGREE_PATTERNS:
                if re.search(pattern, line_lower):

                    if "bca" in line_lower:
                        degree = "Bachelor of Computer Applications (BCA)"
                    elif "btech" in line_lower or "b.tech" in line_lower:
                        degree = "Bachelor of Technology"
                    elif "bsc" in line_lower or "b.sc" in line_lower:
                        degree = "Bachelor of Science"
                    elif "mba" in line_lower:
                        degree = "Master of Business Administration"
                    elif "msc" in line_lower:
                        degree = "Master of Science"
                    else:
                        degree = line_clean

                    break

        # ---- INSTITUTION DETECTION ----
        if institution is None:
            for keyword in INSTITUTION_KEYWORDS:
                if keyword in line_lower:
                    institution = line_clean
                    break

        # ---- YEAR RANGE (Preferred) ----
        if graduation_year is None:
            range_match = re.search(YEAR_RANGE_PATTERN, line)

            if range_match:
                graduation_year = int(range_match.group(2))
            else:
                year_match = re.search(YEAR_PATTERN, line)

                if year_match:
                    graduation_year = int(year_match.group(1))

        # stop early if everything found
        if degree and institution and graduation_year:
            break

    return {
        "degree": degree,
        "institution": institution,
        "graduation_year": graduation_year
    }