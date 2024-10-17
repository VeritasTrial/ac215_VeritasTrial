"""The embed subcommand."""

import numpy as np
import rich

from shared import (
    EMBEDDINGS_NPY_PATH,
    default_progress,
    get_cleaned_data,
    get_model,
)


def main():
    with default_progress() as progress:
        task = progress.add_task("Fetching cleaned data...", total=1)
        studies_df = get_cleaned_data()
        progress.update(task, advance=1)

    # Load the model and encode the summaries, then save the embeddings as binary
    # TODO: strangely use_fp16=True in the container still gives float32 embeddings
    model = get_model()
    rich.print("[bold green]->[/] Creating vector embeddings...")
    embeddings = model.encode(studies_df["summary"].to_list())
    np.save(EMBEDDINGS_NPY_PATH, embeddings)

    rich.print(f"[bold green]->[/] Embeddings saved to {EMBEDDINGS_NPY_PATH}")
