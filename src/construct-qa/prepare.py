"""The prepare subcommand."""

import json

import jsonlines
import rich
from sklearn.model_selection import train_test_split

from shared import (
    INSTRUCTION_TEST_JSONL_PATH,
    INSTRUCTION_TRAIN_JSONL_PATH,
    QA_JSON_PATH,
    default_progress,
)


def main(seed):
    if not QA_JSON_PATH.exists():
        rich.print(
            f"[bold red]Error:[/] Generated QA missing at: {QA_JSON_PATH}; run the "
            "generate subcommand first"
        )
        return

    # Load the generated QA JSON file
    with QA_JSON_PATH.open("r", encoding="utf-8") as f:
        qa_data = json.load(f)

    # Convert into instruction dataset format
    # {
    #   "contents": [
    #     {"role": "user", "parts": [{"text": "QUESTION?"}]},
    #     {"role": "model", "parts": [{"text": "ANSWER."}]}
    #   ]
    # }
    # https://cloud.google.com/vertex-ai/generative-ai/docs/models/gemini-supervised-tuning-prepare#dataset_example_for_gemini-15-pro_and_gemini-15-flash
    with default_progress() as progress:
        task = progress.add_task("Construction dataset...", total=len(qa_data))
        dataset = []
        for _, qa_pairs in qa_data.items():
            for qa_pair in qa_pairs:
                dataset.append(
                    {
                        "contents": [
                            {"role": "user", "parts": [{"text": qa_pair["question"]}]},
                            {"role": "model", "parts": [{"text": qa_pair["answer"]}]},
                        ],
                    }
                )
            progress.update(task, advance=1)

    # Split into training and testing sets
    trainset, testset = train_test_split(dataset, test_size=0.1, random_state=seed)
    with jsonlines.open(INSTRUCTION_TRAIN_JSONL_PATH, "w") as f:
        f.write_all(trainset)
    with jsonlines.open(INSTRUCTION_TEST_JSONL_PATH, "w") as f:
        f.write_all(testset)

    rich.print(
        f"[bold green]->[/] {len(trainset)} training data saved to "
        f"{INSTRUCTION_TRAIN_JSONL_PATH}"
    )
    rich.print(
        f"[bold green]->[/] {len(testset)} testing data saved to "
        f"{INSTRUCTION_TEST_JSONL_PATH}"
    )
