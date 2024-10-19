"""The prepare subcommand."""

import json

import jsonlines
import rich

from shared import (
    INSTRUCTION_JSONL_PATH,
    QA_JSON_PATH,
    default_progress,
    get_cleaned_data,
)

# The template for the questions in the instruction dataset
QUESTION_TEMPLATE = (
    "Please read the following clinical trial information, then answer a question.\n\n"
    "{study_repr}\n\n"
    "### Question\n\n"
    "{question}"
)


def get_study_repr(study):
    """Get the text representation of a study to be prepended to the question."""
    cleaned_study = study.copy()

    # Remove irrelevant fields that may interfere with the instruction
    cleaned_study.pop("id")
    cleaned_study.pop("references")
    cleaned_study.pop("documents")

    return json.dumps(cleaned_study, indent=2)


def main():
    if not QA_JSON_PATH.exists():
        rich.print(
            f"[bold red]Error:[/] Generated QA missing at: {QA_JSON_PATH}; run the "
            "fetch or generate subcommands first"
        )
        return

    with default_progress() as progress:
        # Load the cleaned data to pair with the generated QA
        task = progress.add_task("Loading cleaned data...", total=1)
        studies = get_cleaned_data()
        progress.update(task, advance=1)

        # Load the generated QA
        task = progress.add_task("Loading generated QA...", total=1)
        with QA_JSON_PATH.open("r", encoding="utf-8") as f:
            qa_data = json.load(f)
        progress.update(task, advance=1)

        # Convert into instruction dataset format
        # {
        #   "contents": [
        #     {"role": "user", "parts": [{"text": "QUESTION?"}]},
        #     {"role": "model", "parts": [{"text": "ANSWER."}]}
        #   ]
        # }
        # https://cloud.google.com/vertex-ai/generative-ai/docs/models/gemini-supervised-tuning-prepare#dataset_example_for_gemini-15-pro_and_gemini-15-flash
        task = progress.add_task("Construction dataset...", total=len(qa_data))
        n_written = 0
        with jsonlines.open(INSTRUCTION_JSONL_PATH, "w") as f:
            for nctid, qa_pairs in qa_data.items():
                # Find the corresponding study from cleaned data
                target_study = next(item for item in studies if item["id"] == nctid)
                target_study_repr = get_study_repr(target_study)

                for qa_pair in qa_pairs:
                    # The question will be combined with the study information to form
                    # the instruction, and the answer will be kept as is
                    formatted_question = QUESTION_TEMPLATE.format(
                        study_repr=target_study_repr, question=qa_pair["question"]
                    )
                    conversation = [
                        {"role": "user", "parts": [{"text": formatted_question}]},
                        {"role": "model", "parts": [{"text": qa_pair["answer"]}]},
                    ]
                    f.write({"contents": conversation})
                    n_written += 1
                progress.update(task, advance=1)

    rich.print(
        f"[bold green]->[/] {n_written} instruction data saved to "
        f"{INSTRUCTION_JSONL_PATH}"
    )
