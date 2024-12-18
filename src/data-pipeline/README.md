# Data Pipeline

Make sure you are in this directory. Also make sure to put `veritas-trial-deployment.json` under the `secrets/` folder in the root directory. To run the data pipeline:

```bash
make build
make run
```

This should bring you within the Docker container. Then inside the container, run:

```bash
python cli.py fetch
python cli.py clean
python cli.py upload
```

> [!NOTE]
> - See [clean.py](./clean.py) for the structure of the cleaned data.
> - Use `--help` on `cli.py` to get an overview of what each subcommand does.
> - This step is automated in the "Deploy pipeline" workflow with GitHub Actions.
