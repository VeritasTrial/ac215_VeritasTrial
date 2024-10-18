"""The upload subcommand."""

import os
import argparse
import pandas as pd
import json
import glob
from google.cloud import storage
from io import StringIO
from shared import (
    BUCKET_NAME,
    default_progress,
)

# Setup environment variables
OUTPUT_FOLDER = "data" 

def main():
    print("Uploading generated files to GCP bucket...")

    # Initialize GCP storage client
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    timeout = 300 

    # Define the file paths for JSONL and CSV files
    data_files = glob.glob(os.path.join(OUTPUT_FOLDER, "*.jsonl")) + glob.glob(os.path.join(OUTPUT_FOLDER, "*.csv"))
    data_files.sort()

    # Ensure files are found before proceeding
    if not data_files:
        print(f"No files found in {OUTPUT_FOLDER} to upload.")
        return

    # Start the upload with a progress bar
    with default_progress() as progress:
        task = progress.add_task("Uploading files...", total=len(data_files))

        for data_file in data_files:
            filename = os.path.basename(data_file)
            destination_blob_name = os.path.join("construct-qa", filename)
            blob = bucket.blob(destination_blob_name)

            try:
                print(f"Uploading {data_file} to {destination_blob_name}...")
                blob.upload_from_filename(data_file, timeout=timeout)
                progress.update(task, advance=1)
            except Exception as e:
                print(f"Error uploading {data_file}: {e}")

    rich.print(f"[bold green]Data uploaded to 'construct-qa/' in bucket {BUCKET_NAME}![/]")