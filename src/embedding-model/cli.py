"""The CLI entrypoint."""

import click

# from embed import main as cli_embed
from store import main as cli_store
from upload import main as cli_upload


@click.group(help="Embedding model CLI for VeritasTrial.")
def cli():
    pass


@cli.command(help="Create vector embeddings and upload to GCP bucket")
def embed():
    cli_embed()

@cli.command(help="Fetch embeddings from GCP bucket")
def store():
    cli_store()

@cli.command(help="Upload embeddings into GCP bucket")
def upload():
    cli_upload()


if __name__ == "__main__":
    cli()
