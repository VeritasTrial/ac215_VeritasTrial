# Model Finetuning

> [!WARNING]
> This step is legacy and not included in the final pipeline. Curating a sufficiently large and high-quality QA dataset and the subsequent LLM finetuning step costs too much which does not fit well into our pipeline.

Make sure you are in this directory. Also make sure to put `veritas-trial-deployment.json` under the `secrets/` folder in the root directory. To run the model finetuning:

```bash
make build
make run
```

This should bring you within the Docker container. Then inside the container, run:

```bash
# Choose 100% data from the "qa" dataset with 10% validation set, then choose
# 20000 data from the "pubmed-qa" dataset with 10% validation set, combine them
# together, and upload to GCS
python cli.py prepare -d qa,1.0,0.1 -d pubmed-qa,20000,0.1
# Specify train and test sets on GCS used for finetuning, which can be copied
# from the output of the previous prepare subcommand
python cli.py train ${TIMESTAMP}_train_${TRAIN_SIZE} ${TIMESTAMP}_test_${TEST_SIZE}
# Go to the model registry, click on a finetuned model and copy its ID below to
# start a chat (note there is no memory mechanism)
python cli.py chat ${ENDPOINT_ID}
```

> [!NOTE]
> - The prepare subcommand will automatically upload to GCS, so remember to regularly clean up old datasets on GCS that will no longer be used.
> - Use `--help` on `cli.py` to get an overview of what each subcommand does.
