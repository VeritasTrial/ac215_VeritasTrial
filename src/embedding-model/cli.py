"""The CLI entrypoint."""

import click

from embed import main as cli_embed
from store import main as cli_store
from upload import main as cli_upload
from query import main as cli_query
from eval import main as cli_eval



@click.group(help="Embedding model CLI for VeritasTrial.")
def cli():
    pass


@cli.command(help="Create vector embeddings.")
def embed():
    cli_embed()


@cli.command(help="Upload embeddings to GCS.")
def upload():
    cli_upload()


@cli.command(help="Store embeddings in ChromaDB.")
def store():
    cli_store()

@cli.command(help="Retrieve trials from ChromaDB based on query.")
@click.argument('query_text')
@click.option('--top_k', default=10, help='Number of top results to retrieve.')
def query(query_text, top_k):
    """Retrieve trials from ChromaDB based on the query text."""
    cli_query(query_text, top_k)

@cli.command(help="Evaluate the embedding quality")
def eval():
    cli_eval()


if __name__ == "__main__":
    cli()
