"""The CLI entrypoint."""

import click

from embed import main as cli_embed
from eval import main as cli_eval
from query import main as cli_query
from store import main as cli_store
from upload import main as cli_upload


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


@cli.command(help="Query ChromaDB for top matches.")
@click.argument("query")
@click.option("-k", "--top-k", default=10, help="Number of top matches to retrieve.")
def query(query, top_k):
    cli_query(query, top_k)


@cli.command(help="Evaluate embeddings quality.")
@click.option("-s", "--seed", default=42, help="Random seed.")
def eval(seed):
    cli_eval(seed)


if __name__ == "__main__":
    cli()
