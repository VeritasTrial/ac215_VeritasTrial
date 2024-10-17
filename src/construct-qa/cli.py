"""The CLI entrypoint."""

import click

from generate import main as cli_generate
from prepare import main as cli_prepare
from upload import main as cli_upload


@click.group(help="Constructing qa-pairs for VeritasTrial.")
def cli():
    pass


@cli.command(help="Gnenerate qa-pairs.")
def generate():
    cli_generate()


@cli.command(help="Prepare datasets as needed in Gemini.")
def prepare():
    cli_prepare()


@cli.command(help="Upload qa-pairs in the required format.")
def upload():
    cli_upload()


if __name__ == "__main__":
    cli()
