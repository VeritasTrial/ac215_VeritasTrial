"""The CLI entrypoint."""

import click

from generate import main as cli_generate
from prepare import main as cli_prepare
from upload import main as cli_upload


@click.group(help="QA construction CLI for VeritasTrial.")
def cli():
    pass


@cli.command(help="Generate QA with VertexAI.")
@click.option("-s", "--start", type=int, help="Starting index of studies to process.")
@click.option("-e", "--end", type=int, help="Ending index of studies to process.")
@click.option("--overwrite", is_flag=True, help="Overwrite QA for existing studies.")
def generate(start, end, overwrite):
    cli_generate(start, end, overwrite)


@cli.command(help="Prepare instruction dataset from generated QA.")
@click.option("-s", "--seed", default=42, help="Random seed for dataset splitting.")
def prepare(seed):
    print(seed)
    cli_prepare(seed)


@cli.command(help="Upload instruction dataset.")
def upload():
    cli_upload()


if __name__ == "__main__":
    cli()
