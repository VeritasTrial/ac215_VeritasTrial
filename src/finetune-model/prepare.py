import time

import jsonlines
import numpy as np
import rich
from google.cloud import storage
from sklearn.model_selection import train_test_split

from shared import (
    BUCKET_FINETUNE_DATA_DIR,
    BUCKET_NAME,
    DATASET_MAPPING,
    TEMP_TEST_JSONL_PATH,
    TEMP_TRAIN_JSONL_PATH,
    default_progress,
)


def parse_config(config):
    """Parse a dataset configuration string.

    This returns a tuple of dataset path, data size, and test size if successful,
    otherwise returns None.
    """
    try:
        name, data_size, test_size = config.split(",")
    except:
        rich.print(f"[bold red]Error:[/] Invalid format in {config!r}")
        return

    # Check if dataset name is valid
    remote_path = DATASET_MAPPING.get(name)
    if remote_path is None:
        rich.print(f"[bold red]Error:[/] Invalid dataset name in {config!r}")
        return

    # Parse data size into int or float
    try:
        data_size = int(data_size)
    except:
        try:
            data_size = float(data_size)
        except:
            rich.print(f"[bold red]Error:[/] Invalid data size in {config!r}")
            return

    # Parse test size into int or float
    try:
        test_size = int(test_size)
    except:
        try:
            test_size = float(test_size)
        except:
            rich.print(f"[bold red]Error:[/] Invalid test size in {config!r}")
            return

    return remote_path, data_size, test_size


def reuse_or_fetch(remote_path, data_size, test_size, seed):
    """Reuse local dataset or fetch from GCS and return data.

    This function returns a tuple of train and test data.
    """
    local_path = TEMP_TRAIN_JSONL_PATH.parent / remote_path
    if not local_path.exists():
        # Download the dataset from GCS if it does not exist locally
        local_path.parent.mkdir(parents=True, exist_ok=True)
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(remote_path)
        blob.download_to_filename(local_path)

    # Load the full dataset
    with jsonlines.open(local_path) as f:
        data = [line for line in f]

    # Randomly sample data; if `data_size` is float then sample fraction of data,
    # otherwise sample `data_size` number of data
    data_size = data_size if isinstance(data_size, int) else int(len(data) * data_size)
    rng = np.random.default_rng(seed)
    data = rng.choice(data, data_size, replace=False)

    # Split the data into train and test sets
    train_data, test_data = train_test_split(
        data, test_size=test_size, random_state=seed
    )
    return train_data, test_data


def main(configs, seed):
    configs = [parse_config(config) for config in configs]
    if None in configs:
        return

    # Prepare the dataset writers
    train_writer = jsonlines.open(TEMP_TRAIN_JSONL_PATH, "w")
    test_writer = jsonlines.open(TEMP_TEST_JSONL_PATH, "w")
    n_train, n_test = 0, 0

    with default_progress() as progress:
        task = progress.add_task("Preparing dataset...", total=len(configs))
        for remote_path, data_size, test_size in configs:
            rich.print(f"[bold green]->[/] Processing {remote_path!r}")
            train_data, test_data = reuse_or_fetch(
                remote_path, data_size, test_size, seed
            )

            # Write the train and test data to JSONL files
            train_writer.write_all(train_data)
            test_writer.write_all(test_data)
            n_train += len(train_data)
            n_test += len(test_data)
            rich.print(f"   [bold green]->[/] Appended {len(train_data)} train data")
            rich.print(f"   [bold green]->[/] Appended {len(test_data)} test data")
            progress.update(task, advance=1)

        train_writer.close()
        test_writer.close()

        # Upload the constructed datasets to GCS
        task = progress.add_task("Uploading dataset...", total=2)
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        # Use timestamp to avoid overwriting existing data, and include data size in the
        # filename for easy identification
        timestamp = int(time.time())
        train_loc = f"{BUCKET_FINETUNE_DATA_DIR}/{timestamp}_train_{n_train}.jsonl"
        test_loc = f"{BUCKET_FINETUNE_DATA_DIR}/{timestamp}_test_{n_test}.jsonl"
        blob = bucket.blob(train_loc)
        blob.upload_from_filename(TEMP_TRAIN_JSONL_PATH)
        progress.update(task, advance=1)
        blob = bucket.blob(test_loc)
        blob.upload_from_filename(TEMP_TEST_JSONL_PATH)
        progress.update(task, advance=1)

    rich.print(
        f"[bold green]->[/] {n_train} train data uploaded to {train_loc!r} in bucket "
        f"{BUCKET_NAME!r}"
    )
    rich.print(
        f"[bold green]->[/] {n_test} test data uploaded to {test_loc!r} in bucket "
        f"{BUCKET_NAME!r}"
    )
