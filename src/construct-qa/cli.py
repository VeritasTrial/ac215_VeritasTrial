"""The CLI entrypoint."""

import click

from fetch import main as cli_fetch
from generate import main as cli_generate
from prepare import main as cli_prepare
from upload import main as cli_upload


@click.group(help="QA construction CLI for VeritasTrial.")
def cli():
    pass


@cli.command(help="Fetch QA from GCS.")
def fetch():
    cli_fetch()


@cli.command(help="Generate QA with VertexAI.")
@click.option("-s", "--start", type=int, help="Starting index of studies to process.")
@click.option("-e", "--end", type=int, help="Ending index of studies to process.")
@click.option("-n", "--n-pairs", default=3, help="Number of QA to generate per study.")
@click.option("--overwrite", is_flag=True, help="Overwrite QA for existing studies.")
def generate(start, end, n_pairs, overwrite):
    cli_generate(start, end, n_pairs, overwrite)


@cli.command(help="Prepare instruction dataset from generated QA.")
@click.option("-s", "--seed", default=42, help="Random seed for dataset splitting.")
def prepare(seed):
    cli_prepare(seed)


@cli.command(help="Upload QA and instruction datasets.")
def upload():
    cli_upload()


if __name__ == "__main__":
    cli()
