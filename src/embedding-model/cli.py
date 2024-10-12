"""The CLI entrypoint."""

import click

from embed import main as cli_embed


@click.group(help="Embedding model CLI for VeritasTrial.")
def cli():
    pass


@cli.command(help="Construct vector embeddings.")
def embed():
    cli_embed()


if __name__ == "__main__":
    cli()
