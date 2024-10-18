"""The prepare subcommand."""

import json
import os
from io import StringIO

from google.cloud import storage
from sklearn.model_selection import train_test_split

from shared import default_progress

OUTPUT_FOLDER = "data"


def main():
    print("Preparing generated Q&A pairs for fine-tuning...")

    jsonl_file = os.path.join(OUTPUT_FOLDER, "clinical_trial_qa.jsonl")

    output_pairs = []
    errors = []

    # Open the JSONL file and process each line (each Q&A pair)
    try:
        with open(jsonl_file, "r") as file:
            for line in file:
                try:
                    # Load each line as a JSON object
                    qa_pair = json.loads(line.strip())
                    output_pairs.append(qa_pair)
                except Exception as e:
                    errors.append({"line": line, "error": str(e)})
    except FileNotFoundError as e:
        print(f"Error: {jsonl_file} not found.")
        return

    print("Number of errors:", len(errors))
    print(errors[:5] if errors else "No errors")

    # Convert to DataFrame
    output_pairs_df = pd.DataFrame(output_pairs)

    # Drop duplicates based on all columns, including 'id'
    output_pairs_df.drop_duplicates(inplace=True)
    output_pairs_df = output_pairs_df.dropna()
    print("Shape after dropping duplicates:", output_pairs_df.shape)
    print(output_pairs_df.head())

    # Save cleaned dataset to CSV
    filename = os.path.join(OUTPUT_FOLDER, "instruct-dataset.csv")
    output_pairs_df.to_csv(filename, index=False)

    # Build training format for Gemini fine-tuning (while retaining the 'id')
    output_pairs_df["contents"] = output_pairs_df.apply(
        lambda row: [
            {"role": "user", "parts": [{"text": row["question"]}]},
            {"role": "model", "parts": [{"text": row["answer"]}]},
        ],
        axis=1,
    )

    # Split into training and testing sets (retain 'id' field)
    df_train, df_test = train_test_split(
        output_pairs_df, test_size=0.1, random_state=42
    )

    # Limit validation dataset to 256 examples
    df_test = df_test[:256]

    # Save as JSONL for the next steps (with 'id' retained)
    with open(os.path.join(OUTPUT_FOLDER, "train.jsonl"), "w") as json_file:
        json_file.write(
            df_train[["id", "contents"]].to_json(orient="records", lines=True)
        )
    with open(os.path.join(OUTPUT_FOLDER, "test.jsonl"), "w") as json_file:
        json_file.write(
            df_test[["id", "contents"]].to_json(orient="records", lines=True)
        )

    print("Data prepared successfully for fine-tuning (id retained).")
