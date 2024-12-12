# QA Construction

> [!WARNING]
> This step is legacy and not included in the final pipeline. Curating a sufficiently large and high-quality QA dataset and the subsequent LLM finetuning step costs too much which does not fit well into our pipeline.

Make sure you are in this directory. Also make sure to put `veritas-trial-deployment.json` under the `secrets/` folder in the root directory. To run the QA construction:

```bash
make build
make run
```

This should bring you within the Docker container. Then inside the container, if you want to have a fresh run or overwrite whatever existing in GCS, run:

```bash
python cli.py generate
python cli.py prepare
python cli.py upload
```

If you want to build on top of what already exists in GCS, run:

```bash
python cli.py fetch
python cli.py generate
python cli.py prepare
python cli.py upload
```

> [!NOTE]
> - See [generate.py](./generate.py) for the prompts used for generating QA.
> - The fetch subcommand overwrites local QA data, so be sure to backup your local data if you need them.
> - The generate subcommand by default appends to local QA data, but the `--overwrite` flag can change this behavior to such that, if an ID is seen in existing QA data, then that ID will be overwritten. The generate subcommand also supports generate only for a range of cleaned data via the `-s/--start` and/or `-e/--end` options.
> - Use `--help` on `cli.py` and its subcommands to get an overview of what each subcommand does.
