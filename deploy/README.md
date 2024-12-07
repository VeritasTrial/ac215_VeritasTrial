# Deploy

The deployment commands are automated with GitHub Actions. It is preffered to trigger the corresponding workflow instead of running the command manually. The following are only for demonstration purposes. Make sure you have `veritas-trial-deployment.json` and `veritas-trial-service.json` under the `/secrets/` directory if you are deploying manually. Now enter this directory, then build and run the container:

```bash
make build
make run
```

## App

The deployment uses Ansible. It will deploy the Docker images of the application and create/update the Kubernetes cluster to run the application. Inside the container, run:

```bash
./deploy-app.sh  # Deploy app (optionally --skip-rebuild-images=true)
./destroy-app.sh # Destroy app
```

## Pipeline

The deployment uses Ansible and Vertex AI pipeline. It will deploy the Docker images of the pipeline and run `/src/data-pipeline/` and `/src/embedding-model/` steps. Inside the container, run:

```bash
./deploy-pipeline.sh # Deploy pipeline (optionally --skip-rebuild-images=true)
```


## ChromaDB

The deployment uses Terraform, as suggested in [ChromaDB docs](https://docs.trychroma.com/deployment/gcp). It will deploy a VM instance that runs ChromaDB service. Note that redeploying ChromaDB requires redeploying the app and the pipeline as well. The following script will not do that, but the corresponding workflow in GitHub Actions will. Inside the container, run:

```bash
./deploy-chromadb.sh  # Deploy ChromaDB instance
./destroy-chromadb.sh # Destroy ChromaDB instance
```
