import csv
import sys
from typing import List, Dict, Optional

def export_to_csv(data: List[Dict], filename: Optional[str] = None) -> None:
    fieldnames = ["PubmedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"]
    rows = []
    for paper in data:
        non_acads = [a for a in paper["authors"] if a.get("non_academic")]
        if not non_acads:
            continue
        rows.append({
            "PubmedID": paper["pmid"],
            "Title": paper["title"],
            "Publication Date": paper["pub_date"],
            "Non-academic Author(s)": "; ".join(a["name"] for a in non_acads),
            "Company Affiliation(s)": "; ".join(a["affiliation"] for a in non_acads),
            "Corresponding Author Email": paper["authors"][0].get("email", "")
        })
    if filename:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    else:
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)