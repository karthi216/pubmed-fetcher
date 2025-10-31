import typer
from papers.fetch import fetch_pubmed_ids, fetch_details
from papers.filter import filter_non_academic_authors, is_non_academic
from papers.exporter import export_to_csv

app = typer.Typer()

@app.command()
def main(
    query: str = typer.Argument(..., help="PubMed search query"),
    file: str = typer.Option(None, "-f", "--file", help="Output CSV filename"),
    debug: bool = typer.Option(False, "-d", "--debug", help="Enable debug output")
):
    if debug:
        typer.echo(f"Searching PubMed for: {query}")
    ids = fetch_pubmed_ids(query)
    if debug:
        typer.echo(f"Found {len(ids)} papers")
    papers = fetch_details(ids)
    for paper in papers:
        for author in paper["authors"]:
            affil = author.get("affiliation") or ""
            author["non_academic"] = bool(affil) and is_non_academic(affil)
    export_to_csv(papers, filename=file)
    if not file:
        typer.echo("Results printed to console.")

if __name__ == "__main__":
    app()