"""The CLI entrypoint."""

import click

from embed import main as cli_embed
from upload import main as cli_upload


@click.group(help="Embedding model CLI for VeritasTrial.")
def cli():
    pass


@cli.command(help="Construct vector embeddings.")
def embed():
    cli_embed()


@cli.command(help="Upload vector database.")
def upload():
    cli_upload()


if __name__ == "__main__":
    cli()
