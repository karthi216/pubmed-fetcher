import requests
import xml.etree.ElementTree as ET
from typing import List, Dict

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

def fetch_pubmed_ids(query: str, retmax: int = 100) -> List[str]:
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": retmax
    }
    response = requests.get(BASE_URL + "esearch.fcgi", params=params)
    response.raise_for_status()
    return response.json()["esearchresult"]["idlist"]

def fetch_details(pubmed_ids: List[str]) -> List[Dict]:
    ids = ",".join(pubmed_ids)
    params = {
        "db": "pubmed",
        "id": ids,
        "retmode": "xml"
    }
    response = requests.get(BASE_URL + "efetch.fcgi", params=params)
    response.raise_for_status()
    root = ET.fromstring(response.content)
    return [parse_article(article) for article in root.findall(".//PubmedArticle")]

def parse_article(article: ET.Element) -> Dict:
    pmid = article.findtext(".//PMID")
    title = article.findtext(".//ArticleTitle")
    pub_date = article.findtext(".//PubDate/Year") or "Unknown"
    authors = []
    for author in article.findall(".//Author"):
        name = " ".join(filter(None, [author.findtext("ForeName"), author.findtext("LastName")]))
        affil = author.findtext(".//AffiliationInfo/Affiliation")
        email = extract_email(affil or "")
        authors.append({"name": name, "affiliation": affil, "email": email})
    return {"pmid": pmid, "title": title, "pub_date": pub_date, "authors": authors}

def extract_email(text: str) -> str:
    import re
    match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return match.group(0) if match else ""