"""The fetch subcommand."""

import json

import jsonlines
import requests
import rich

from shared import METADATA_PATH, RAW_JSONL_PATH, default_progress

API_ENDPOINT = "https://clinicaltrials.gov/api/v2/studies"
AGG_FILTERS = "docs:sap,results:with,status:com"
PAGE_SIZE = 1000


def query(page_token=None):
    """Query the ClinicalTrials.gov API for studies."""
    url = f"{API_ENDPOINT}?aggFilters={AGG_FILTERS}&pageSize={PAGE_SIZE}"
    if page_token is not None:
        url += f"&pageToken={page_token}"

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    raise Exception(f"Failed to fetch data (status: {response.status_code})")


def dump_metadata(n_studies):
    """Dump metadata to a JSON file."""
    with METADATA_PATH.open("w", encoding="utf-8") as f:
        json.dump({"n_studies": n_studies}, f, indent=2)


def main():
    page_token = None
    n_studies = 0

    with default_progress() as progress:
        task = progress.add_task(f"Fetching data...", total=None)
        dump_metadata(n_studies)

        with jsonlines.open(RAW_JSONL_PATH, "w") as f:
            while True:
                # Fetch a certain number of data from the API endpoint and write to the file
                data = query(page_token=page_token)
                f.write_all(data["studies"])
                advance = len(data["studies"])
                n_studies += advance
                dump_metadata(n_studies)
                progress.update(task, advance=advance)

                # Break if there are no more pages, otherwise update the page token which
                # tells the API which page to fetch next
                if "nextPageToken" not in data:
                    break
                page_token = data["nextPageToken"]

    rich.print(f"[bold green]->[/] {n_studies} studies saved to {RAW_JSONL_PATH}")
    rich.print(f"[bold green]->[/] Metadata saved to {METADATA_PATH}")
