# Model Finetuning

Make sure you are in this directory. Also make sure to put `veritas-trial-service.json` that contains credentials for the VeritasTrial data service account under the `secrets/` folder in the root directory. To run the model finetuning:

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
python cli.py train ${TIMESTAMP}_train_${SIZE} ${TIMESTAMP}_test_${SIZE}
```

> [!NOTE]
> - The prepare subcommand will automatically upload to GCS, so remember to regularly clean up old datasets on GCS that will no longer be used.
> - Use `--help` on `cli.py` to get an overview of what each subcommand does.
