# Deploy

Enter this directory, then build and run the container:

```bash
make build
make run
```

## App

The deployment uses Ansible. Inside the container:

```bash
./deploy-app.sh  # Deploy app images and K8S cluster
```

The deployment command is automated with GitHub Actions. It is preferred to trigger the corresponding workflow instead of running the command manually.

## ChromaDB

The deployment uses Terraform, as suggested in [ChromaDB docs](https://docs.trychroma.com/deployment/gcp). Inside the container:

```bash
./deploy-chromadb.sh  # Deploy ChromaDB instance
./destroy-chromadb.sh # Destroy ChromaDB instance
```

Both commands are not automated and need to be run manually when necessary.
