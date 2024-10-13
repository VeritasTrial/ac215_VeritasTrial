"""The CLI entrypoint."""

import click

from clean import main as cli_clean
from fetch import main as cli_fetch
from upload import main as cli_upload


@click.group(help="Data pipeline CLI for VeritasTrial.")
def cli():
    pass


@cli.command(help="Fetch data from API.")
def fetch():
    cli_fetch()


@cli.command(help="Clean fetched data.")
def clean():
    cli_clean()


@cli.command(help="Upload cleaned data.")
def upload():
    cli_upload()


if __name__ == "__main__":
    cli()
