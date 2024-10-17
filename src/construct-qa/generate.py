"""The generate subcommand."""

import os
import argparse
import pandas as pd
import json
import glob
from google.cloud import storage
import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting
import vertexai.generative_models as generative_models
from io import StringIO
from shared import (
    BUCKET_CLEANED_JSONL_PATH,
    GCP_PROJECT,
    GCP_LOCATION,
    BUCKET_NAME,
    GENERATIVE_MODEL,
    default_progress,
)

# Configuration settings for the content generation
generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

# Safety settings to filter out harmful content
safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
    )
]

SYSTEM_INSTRUCTION = """
You are an expert in clinical trials with a deep understanding of trial design, intervention models, outcomes, and eligibility criteria. 
You will be provided with information of clinical trial data including purpose, conditions, interventions, outcomes, and eligibility, as well as many other fields related to the trial. 

Based on this context, your task is to generate diverse, informative, and self-contained question-answer pairs that cover **all relevant fields**. 
These Q&A pairs should be relevant to the trial details and aimed at helping a chatbot respond to clinical trial information queries. 
Focus on non-trivial questions that require a deeper understanding of the trial, while still addressing simpler details when appropriate.

Guidelines:
1. Question Independence:
   - Ensure each question-answer pair is independent and self-contained.
   - Do not reference other questions or answers within the set.
   - Each Q&A should be understandable without additional context.

2. Tone and Style:
   - Use a formal yet clear tone suitable for both clinical professionals and patients.
   - Provide accessible explanations without oversimplifying the content.
   - Offer detailed explanations of trial design and outcomes where relevant, making the content easy to understand.

3. Question Types:
   - Include a variety of question types (e.g., "What is the primary purpose of this trial?", "How does the intervention model work?", "What are the primary outcomes?").
   - Formulate questions that a participant or researcher might ask.

4. Answer Completeness:
   - Ensure every question has a complete and clear answer.
   - Answers should be concise, accurate, and provide relevant details from the trial data.

Output Format:
Provide the Q&A pairs in JSON format, with each pair as an object containing 'question' and 'answer' fields, within a JSON array.
Follow these strict guidelines:
1. Use double quotes for JSON keys and string values.
2. For any quotation marks within the text content, use single quotes (') instead of double quotes.
3. If a single quote (apostrophe) appears in the text, escape it with a backslash (\').
4. Ensure there are no unescaped special characters that could break the JSON structure.

Here's an example of the expected format:
Sample JSON Output:
[
  {
    "question": "What is the primary purpose of the trial?",
    "answer": "The primary purpose of this trial is to obtain preliminary information about the function and effectiveness of a novel vaginal pessary for use in women who suffer from pelvic organ prolapse (POP). The trial aims to compare the subject's current pessary with the study pessary in terms of performance and comfort, with the ultimate goal of informing future design modifications for the study pessary."
  },
  {
    "question": "What are the primary outcomes being measured?",
    "answer": "The primary outcomes being measured include the ability of the study pessary to be retained during Valsalva compared to the subject's current pessary, and the ability of the study pessary to be retained throughout regular activities such as walking and attempting to void. These outcomes will be measured within 1 hour during the treatment phase."
  }
]
"""

# Fetch the cleaned_data.jsonl file from GCP with progress bar
def fetch_cleaned_data(bucket_name, file_path):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.get_blob(file_path)
    
    if blob is None:
        raise FileNotFoundError(f"File {file_path} not found in the bucket.")
    
    with default_progress() as progress:
        task = progress.add_task("Fetching cleaned data...", total=1)
        file_data = blob.download_as_text(encoding='utf-8')
        progress.update(task, advance=1)  

    data_df = pd.read_json(StringIO(file_data), lines=True)
    return data_df


# Generate QA pairs using the clinical trial data and system prompt
def generate_qa_pairs(trial_data, num_pairs=3):
    input_prompt = f"""
    Generate a set of {num_pairs} question-answer pairs based on the following clinical trial data. 
    Clinical trial data: {json.dumps(trial_data, indent=4)}
    """
    
    model = GenerativeModel(GENERATIVE_MODEL, system_instruction=SYSTEM_INSTRUCTION)
    responses = model.generate_content(
        [input_prompt],  
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=False
    )
    
    return responses.text  


def main():
    print("Starting to generate Q&A pairs...")
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    vertexai.init(project=GCP_PROJECT, location=GCP_LOCATION)
    
    # Fetch cleaned data from GCP bucket
    cleaned_data = fetch_cleaned_data(BUCKET_NAME, BUCKET_CLEANED_JSONL_PATH)
    qa_output_file = f"{OUTPUT_FOLDER}/clinical_trial_qa.jsonl" 

    with default_progress() as progress:
        task = progress.add_task("Generating Q&A pairs...", total=len(cleaned_data))

        # Generate QA pairs for each trial
        with open(qa_output_file, "a") as output_file:  
            for index, trial in cleaned_data.iterrows():
                if index >= 5:  # TODO: remove after testing
                    break

                trial_data = trial.to_dict()
                trial_id = trial_data.get("id", f"trial_{index}")  
                print(f"Generating Q&A for trial {trial_id}...")
                
                try:
                    generated_text = generate_qa_pairs(trial_data)
                    # Parse the generated text (assuming it's valid JSON)
                    qa_pairs = json.loads(generated_text)

                    # Add trial ID to each Q&A pair and write to the file
                    for qa in qa_pairs:
                        qa['id'] = trial_id  
                        output_file.write(json.dumps(qa) + '\n')  # Save in JSONL format

                except Exception as e:
                    print(f"Error occurred while generating content: {e}")
                
                progress.update(task, advance=1)
