import requests

from shared import default_progress

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


def main():
    page_token = None
    studies = []

    with default_progress() as progress:
        task = progress.add_task(f"Fetched {len(studies):5d} data", total=None)

        while True:
            data = query(page_token=page_token)
            studies += data["studies"]
            progress.update(task, description=f"Fetched {len(studies):5d} data")

            if "nextPageToken" not in data:
                break  # This means there are no more pages to fetch
            page_token = data["nextPageToken"]
            break  # TODO: Remove this line

    # TODO: Process the fetched data
    # TODO: Upload to GCP bucket
