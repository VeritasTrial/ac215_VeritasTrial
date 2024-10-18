"""The CLI entrypoint."""

import click

from train import main as cli_train


@click.group(help="Model finetuning CLI for VeritasTrial.")
def cli():
    pass


@cli.command(help="Finetune the model.")
@click.option("--epochs", type=int, default=1, help="Number of SFT epochs.")
@click.option("--learning-rate", type=float, default=1.0, help="SFT learning rate.")
def train(epochs, learning_rate):
    cli_train(epochs, learning_rate)


if __name__ == "__main__":
    cli()
