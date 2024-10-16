"""The CLI entrypoint."""

import click

from embed import main as cli_embed
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


if __name__ == "__main__":
    cli()
