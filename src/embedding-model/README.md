# Data Pipeline

Make sure you are in this directory. Also make sure to put `veritas-trial-data-service.json` that contains credentials for the VeritasTrial data service account under the `secrets/` folder in the root directory. To run the data pipeline:

```bash
make build
make run
```

This should bring you within the Docker container. Then inside the container, run:

```bash
python cli.py
```
