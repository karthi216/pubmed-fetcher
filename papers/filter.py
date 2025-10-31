from typing import List, Dict

NON_ACADEMIC_KEYWORDS = ["pharma", "biotech", "inc", "ltd", "corp", "gmbh", "co."]
ACADEMIC_KEYWORDS = ["university", "college", "institute", "school", "hospital"]

def is_non_academic(affiliation: str) -> bool:
    affil = affiliation.lower()
    return any(word in affil for word in NON_ACADEMIC_KEYWORDS) and not any(word in affil for word in ACADEMIC_KEYWORDS)

def filter_non_academic_authors(authors: List[Dict]) -> List[Dict]:
    return [a for a in authors if a["affiliation"] and is_non_academic(a["affiliation"])]