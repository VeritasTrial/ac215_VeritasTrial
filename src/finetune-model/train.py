"""The train subcommand."""

import rich
import vertexai
from vertexai.tuning import sft

from shared import (
    BUCKET_FINETUNE_DATA_DIR,
    BUCKET_NAME,
    GCP_PROJECT_ID,
    GCP_PROJECT_LOCATION,
)

BASE_MODEL = "gemini-1.5-flash-002"


def main(train_dataset, test_dataset, epochs, learning_rate):
    vertexai.init(project=GCP_PROJECT_ID, location=GCP_PROJECT_LOCATION)

    # Initialize a new supervised fine-tuning job
    # https://cloud.google.com/vertex-ai/generative-ai/docs/reference/python/latest/vertexai.preview.tuning.sft#vertexai_preview_tuning_sft_train
    sft_job = sft.train(
        source_model=BASE_MODEL,
        train_dataset=f"gs://{BUCKET_NAME}/{BUCKET_FINETUNE_DATA_DIR}/{train_dataset}.jsonl",
        validation_dataset=f"gs://{BUCKET_NAME}/{BUCKET_FINETUNE_DATA_DIR}/{test_dataset}.jsonl",
        epochs=epochs,
        learning_rate_multiplier=learning_rate,
        adapter_size=4,
        tuned_model_display_name=f"veritas-trial",
    )

    rich.print(f"[bold green]->[/] SFT job created")
    rich.print(f"   Name:       [dim]{sft_job.tuned_model_name}[/]")
    rich.print(f"   Endpoint:   [dim]{sft_job.tuned_model_endpoint_name}[/]")
    rich.print(f"   Experiment: [dim]{sft_job.experiment}[/]")
