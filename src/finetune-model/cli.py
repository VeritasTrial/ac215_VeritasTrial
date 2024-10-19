"""The CLI entrypoint."""

import click

from chat import main as cli_chat
from prepare import main as cli_prepare
from shared import DATASET_MAPPING
from train import main as cli_train


@click.group(help="Model finetuning CLI for VeritasTrial.")
def cli():
    pass


@cli.command(help="Prepare finetuning dataset on GCS.")
@click.option(
    "-d",
    "--dataset",
    type=str,
    required=True,
    multiple=True,
    help=(
        "Datasets to combine, each specified as '<name>,<data_size>,<test_size>'. "
        f"Available datasets: {', '.join(DATASET_MAPPING)}. Data size is the number of "
        "samples to randomly sample from the dataset (including train and test), and "
        "test size is the number of test samples to further sample from the sampled "
        "dataset. Both sizes can be an integer that represents an abolute number of "
        "samples, or a float in (0, 1) that represents a fraction."
    ),
)
@click.option("-s", "--seed", default=42, help="Random seed.")
def prepare(dataset, seed):
    cli_prepare(dataset, seed)


@cli.command(help="Chat with a finetuned model.")
@click.argument("endpoint")
def chat(endpoint):
    cli_chat(endpoint)


@cli.command(help="Finetune the model.")
@click.argument("train_dataset")
@click.argument("test_dataset")
@click.option("--epochs", type=int, default=1, help="Number of SFT epochs.")
@click.option("--learning-rate", type=float, default=1.0, help="SFT learning rate.")
def train(train_dataset, test_dataset, epochs, learning_rate):
    cli_train(train_dataset, test_dataset, epochs, learning_rate)


if __name__ == "__main__":
    cli()
