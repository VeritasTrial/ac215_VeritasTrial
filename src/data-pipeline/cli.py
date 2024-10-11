"""
This files wraps the subcommands into a single CLI entry point.
"""

import click

from clean import main as cli_clean
from fetch import main as cli_fetch
from upload import main as cli_upload


@click.group()
def cli():
    pass


@cli.command()
def fetch():
    cli_fetch()


@cli.command()
def clean():
    cli_clean()


@cli.command()
def upload():
    cli_upload()


if __name__ == "__main__":
    cli()
