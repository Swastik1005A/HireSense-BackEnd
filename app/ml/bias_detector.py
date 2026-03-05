import re
from typing import Dict, List


GENDER_TERMS = [
    "he", "she", "him", "her",
    "mr", "mrs", "miss", "ms"
]

AGE_PATTERNS = [
    r"\b\d{2}\s*years old\b",
    r"date of birth",
    r"\bage\b"
]

NATIONALITY_TERMS = [
    "nationality",
    "citizenship",
    "indian",
    "american"
]

PRESTIGE_UNIVERSITIES = [
    "iit",
    "mit",
    "stanford",
    "harvard",
    "cambridge",
    "oxford"
]


def detect_bias(text: str) -> Dict:

    text_lower = text.lower()

    detected = {
        "gender": [],
        "age": [],
        "nationality": [],
        "prestige_education": []
    }

    # Gender
    for term in GENDER_TERMS:
        if term in text_lower:
            detected["gender"].append(term)

    # Age
    for pattern in AGE_PATTERNS:
        matches = re.findall(pattern, text_lower)
        detected["age"].extend(matches)

    # Nationality
    for term in NATIONALITY_TERMS:
        if term in text_lower:
            detected["nationality"].append(term)

    # Prestige University Bias
    for uni in PRESTIGE_UNIVERSITIES:
        if uni in text_lower:
            detected["prestige_education"].append(uni)

    bias_score = sum(len(v) for v in detected.values())

    if bias_score == 0:
        bias_flag = "None"
    elif bias_score < 3:
        bias_flag = "Low"
    else:
        bias_flag = "High"

    return {
        "bias_flag": bias_flag,
        "bias_score": bias_score,
        "signals": detected
    }