import typer
import pandas as pd
from pubmed_fetcher.fetcher import PubMedFetcher

app = typer.Typer()

@app.command()
def get_papers_list(
    query: str,
    debug: bool = typer.Option(False, "--debug", "-d"),
    file: str = typer.Option(None, "--file", "-f")
) -> None:
    """
    Fetch papers matching the query and output CSV.
    """
    fetcher = PubMedFetcher(debug)
    ids = fetcher.fetch_paper_ids(query)
    xml_data = fetcher.fetch_paper_details(ids)
    papers = fetcher.parse_and_filter(xml_data)

    df = pd.DataFrame(papers)
    if file:
        df.to_csv(file, index=False)
        typer.echo(f"Results saved to {file}")
    else:
        typer.echo(df.to_csv(index=False))

if __name__ == "__main__":
    app()

