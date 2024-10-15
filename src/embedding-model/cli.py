"""The CLI entrypoint."""

import click

from embed import main as cli_embed
from store import main as cli_store


@click.group(help="Embedding model CLI for VeritasTrial.")
def cli():
    pass


@cli.command(help="Create vector embeddings and upload to GCP bucket")
def embed():
    cli_embed()

@cli.command(help="Fetch embeddings from GCP bucket")
def store():
    cli_store()


if __name__ == "__main__":
    cli()
