# QA Construction

Make sure you are in this directory. Also make sure to put `veritas-trial-service.json` that contains credentials for the VeritasTrial data service account under the `secrets/` folder in the root directory. To run the QA construction:

```bash
make build
make run
```

This should bring you within the Docker container. Then inside the container, run:

```bash
python cli.py generate
python cli.py prepare
python cli.py upload
```

> [!NOTE]
> - The generate subcommand supports generating for a range of cleaned data by specifying `-s/--start` and/or `-e/--end` options. The `--overwrite` flag controls that, if an ID is already seen in the existing QA dataset, whether we will overwrite its QA pairs or append to them.
> - Use `--help` on `cli.py` and its subcommands to get an overview of what each subcommand does.
