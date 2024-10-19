import time

import rich
import vertexai
from rich.progress import Progress, SpinnerColumn, TextColumn
from vertexai.generative_models import GenerativeModel

from shared import GCP_PROJECT_ID, GCP_PROJECT_LOCATION

GENERATION_CONFIG = {
    "max_output_tokens": 2048,
    "temperature": 0.75,
    "top_p": 0.95,
}


def main(endpoint):
    vertexai.init(project=GCP_PROJECT_ID, location=GCP_PROJECT_LOCATION)

    model = GenerativeModel(
        f"projects/{GCP_PROJECT_ID}/locations/{GCP_PROJECT_LOCATION}/endpoints/{endpoint}",
        generation_config=GENERATION_CONFIG,
    )

    while True:
        rich.get_console().rule(style="dim")
        rich.print("[bold green]-> You:[/]", end=" ")
        user_input = input().strip()
        if user_input.lower() in ["exit", "quit"]:
            break

        start = time.perf_counter()
        with Progress(
            TextColumn("{task.description}"),
            SpinnerColumn(style="blue"),
            transient=True,
        ) as progress:
            progress.add_task("[bold blue]-> Bot:[/]", total=None)
            response = model.generate_content(user_input, stream=False)
        end = time.perf_counter()
        rich.get_console().print(
            f"[bold blue]-> Bot:[/] {response.text.strip()} [dim][Answered in "
            f"{end - start:.3f} seconds][/dim]",
            highlight=False,
        )
