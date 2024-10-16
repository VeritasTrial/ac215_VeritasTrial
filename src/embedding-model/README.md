# Embedding Model

Make sure you are in this directory. Also make sure to put `veritas-trial-service.json` that contains credentials for the VeritasTrial data service account under the `secrets/` folder in the root directory. To run the embedding model:

```bash
make build
make run
```

This should start a Docker network (`make network`) if it does not already exist, start the ChromaDB server (`make chromadb`) if it is not running, and bring you within the Docker container. Then inside the container, run:

```bash
python cli.py embed  # Time-consuming without GPUs
python cli.py upload
python cli.py store
```

You can test querying the vector database or perform an evaluation:

```bash
python cli.py query "Get me some trials related to mental disorder"
python cli.py eval
```

> [!NOTE]
> - Use `make info` to check the Docker network and the ChromaDB server.
> - Use `--help` on `cli.py` to and its subcommands to get an overview of what each subcommand does.
