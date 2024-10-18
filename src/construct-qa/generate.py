"""The generate subcommand."""

import json
import re

import jsonlines
import rich
import vertexai
from google.cloud import storage
from vertexai.generative_models import GenerativeModel, SafetySetting

from shared import (
    BUCKET_CLEANED_JSONL_PATH,
    BUCKET_NAME,
    CLEANED_JSONL_PATH,
    QA_JSON_PATH,
    default_progress,
)

# Project configuration used for Vertex AI
GCP_PROJECT_ID = "veritastrial"
GCP_PROJECT_LOCATION = "us-central1"

# The generative model to use
GEMINI_MODEL = "gemini-1.5-flash-001"

# Model configuration
GENERATION_CONFIG = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

# Safety settings to avoid harmful content
SAFETY_SETTINGS = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    ),
]

# Template for system instruction
SYSTEM_INSTRUCTION_TEMPLATE = (
    "You are an expert in clinical trials with a deep understanding of trial design, "
    "intervention models, outcomes, and eligibility criteria. You will be provided "
    "with information of clinical trial data including purpose, conditions, "
    "interventions, outcomes, and eligibility, as well as many other fields related "
    "to the trial.\n\n"
    "Based on this context, your task is to generate diverse, informative, and "
    "self-contained question-answer pairs that cover **all relevant fields**. These "
    "Q&A pairs should be relevant to the trial details and aimed at helping a chatbot "
    "respond to clinical trial information queries. Focus on non-trivial questions "
    "that require a deeper understanding of the trial, while still addressing simpler "
    "details when appropriate.\n\n"
    "Guidelines:\n\n"
    "1. Question Independence:\n"
    "   - Ensure each question-answer pair is independent and self-contained.\n"
    "   - Do not reference other questions or answers within the set.\n"
    "   - Each Q&A should be understandable without additional context.\n\n"
    "2. Tone and Style:\n"
    "   - Use a formal yet clear tone suitable for both clinical professionals and "
    "     patients.\n"
    "   - Provide accessible explanations without oversimplifying the content.\n"
    "   - Offer detailed explanations of trial design and outcomes where relevant, "
    "     making the content easy to understand.\n\n"
    "3. Question Types:\n"
    "   - Include a variety of question types, e.g., 'What is the primary purpose of "
    "     this trial?', 'How does the intervention model work?', 'What are the primary "
    "     outcomes?'\n"
    "   - Formulate questions that a participant or researcher might ask.\n\n"
    "4. Answer Completeness:\n"
    "   - Ensure every question has a complete and clear answer.\n"
    "   - Answers should be concise, accurate, and provide relevant details from the "
    "     trial.\n\n"
    "Output Format:\n\n"
    "Output the list of Q&A pairs in valid JSON format, with each pair being an object "
    "with two fields: 'question' and 'answer'. Here is an output example:\n\n"
    "{output_example}"
)

# Template for prompting the model to generate QA pairs
PROMPT_TEMPLATE = (
    "Generate a set of {n_pairs} question-answer pairs based on the following clinical "
    "trial data:\n\n{trial_json}"
)

# One-shot example of the expected output
OUTPUT_EXAMPLE = [
    {
        "question": "What is the primary purpose of the trial?",
        "answer": (
            "The primary purpose of this trial is to obtain preliminary information "
            "about the function and effectiveness of a novel vaginal pessary for use "
            "in women who suffer from pelvic organ prolapse (POP). The trial aims to "
            "compare the subject's current pessary with the study pessary in terms of "
            "performance and comfort, with the ultimate goal of informing future "
            "design modifications for the study pessary."
        ),
    },
    {
        "question": "What are the primary outcomes being measured?",
        "answer": (
            "The primary outcomes being measured include the ability of the study "
            "pessary to be retained during Valsalva compared to the subject's current "
            "pessary, and the ability of the study pessary to be retained throughout "
            "regular activities such as walking and attempting to void. These outcomes "
            "will be measured within 1 hour during the treatment phase."
        ),
    },
]


def process_response(response):
    """Process the response of the model into a list of QA pairs."""
    # Remove possible code block formatting and strip off whitespace
    text = re.sub(r"```json|```", "", response.text).strip()

    # Attempt to parse the text as JSON
    qa_pairs = json.loads(text)

    # Check that the output is a list of dictionaries with exactly two keys "question"
    # and "answer" all corresponding to strings
    if not isinstance(qa_pairs, list):
        raise ValueError("Output JSON is not a list.")
    if not all(
        (
            isinstance(qa, dict)
            and set(qa) == {"question", "answer"}
            and isinstance(qa["question"], str)
            and isinstance(qa["answer"], str)
        )
        for qa in qa_pairs
    ):
        raise ValueError("Output JSON does not contain valid Q&A pairs.")

    return qa_pairs


def main(start_idx, end_idx, overwrite):
    vertexai.init(project=GCP_PROJECT_ID, location=GCP_PROJECT_LOCATION)
    rich.print(f"[bold green]->[/] Selected range: [{start_idx}, {end_idx})")

    with default_progress() as progress:
        task = progress.add_task("Fetching cleaned data...", total=1)
        if not CLEANED_JSONL_PATH.exists():
            # Fetch cleaned data from GCP bucket only when the file is not already
            # fetched to local
            storage_client = storage.Client()
            bucket = storage_client.bucket(BUCKET_NAME)
            data_blob = bucket.get_blob(BUCKET_CLEANED_JSONL_PATH)
            with CLEANED_JSONL_PATH.open("wb") as f:
                data_blob.download_to_file(f)
        # Load the cleaned data and limit to the specified range
        with jsonlines.open(CLEANED_JSONL_PATH, "r") as f:
            studies = [study for study in f][slice(start_idx, end_idx)]
        progress.update(task, advance=1)

        # Skip generating QA pairs if the range is empty
        n_studies = len(studies)
        if n_studies == 0:
            rich.print("[bold yellow]Warning:[/] No studies selected for generation")
            return

        # Initialize the generative model with default settings
        task = progress.add_task("Generating QA...", total=n_studies)
        system_instruction = SYSTEM_INSTRUCTION_TEMPLATE.format(
            output_example=json.dumps(OUTPUT_EXAMPLE, indent=2)
        )
        model = GenerativeModel(
            GEMINI_MODEL,
            generation_config=GENERATION_CONFIG,
            safety_settings=SAFETY_SETTINGS,
            system_instruction=system_instruction,
        )

        # Load existing QA pairs if they exist, otherwise start fresh
        qa_data = {}
        if QA_JSON_PATH.exists():
            with QA_JSON_PATH.open("r", encoding="utf-8") as f:
                qa_data = json.load(f)

        # For each study, generate QA pairs and append to the existing data
        for study in studies:
            study_id = study["id"]
            prompt = PROMPT_TEMPLATE.format(
                n_pairs=3, trial_json=json.dumps(study, indent=2)
            )
            response = model.generate_content(prompt, stream=False)
            try:
                # Retrive the list of QA pairs from the model response; note that if the
                # `overwrite` flag is set, the existing QA pairs for the study will be
                # replaced with the new ones, otherwise they will be appended
                qa_pairs = process_response(response)
                if study_id in qa_data and not overwrite:
                    qa_data[study_id].extend(qa_pairs)
                else:
                    qa_data[study_id] = qa_pairs
            except Exception as e:
                rich.print(f"[bold red]Error:[/] {e} [dim]({study['id']})[/]")
            progress.update(task, advance=1)

        # Write the updated QA pairs back
        with QA_JSON_PATH.open("w", encoding="utf-8") as f:
            json.dump(qa_data, f, indent=2)

    rich.print(f"[bold green]->[/] Generated QA saved to {QA_JSON_PATH}")
