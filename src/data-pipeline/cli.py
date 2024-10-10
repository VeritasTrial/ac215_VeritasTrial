"""
This files wraps the subcommands into a single CLI entry point.
"""

import click

from fetch_studies import main as cli_fetch_studies


@click.group()
def cli():
    pass


@cli.command()
def fetch():
    cli_fetch_studies()


if __name__ == "__main__":
    cli()
