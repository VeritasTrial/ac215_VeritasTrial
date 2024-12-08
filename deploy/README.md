# Deploy

The deployment commands are automated with GitHub Actions. It is preffered to trigger the corresponding workflow instead of running the command manually. The following are only for demonstration purposes. Make sure you have `veritas-trial-deployment.json` and `veritas-trial-service.json` under the `/secrets/` directory if you are deploying manually. You should also have `certificate.crt` and `private.key` under the `/secrets/` directory, which are for SSL certification (e.g., from ZeroSSL). Now enter this directory, then build and run the container:

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

## Others

<details>
<summary>Obtaining SSL certificate from ZeroSSL</summary>
<p>

Here we demonstrate how to obtain a ZeroSSL certificate. When verifying the domain, one should choose verify by file upload. Suppose `XXXXXX.txt` is the file you are given. Then do the following modifications locally (not to be committed):

- In the `run` target in `Makefile`, add the following to the docker run command:

  ```
  --volume $(PWD)/../secrets/XXXXXX.txt:/secrets/pki-validation.txt:ro \
  ```

- Just before the step of waiting for nginx-ingress to get ready in `app/deploy-k8s.yaml`, add the following steps:

  ```yaml
  - name: Create PKI validation config map
    when: cluster_state == "present"
    kubernetes.core.k8s:
      state: present
      definition:
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: pki-validation-config
          namespace: "{{ cluster_name }}-namespace"
        data:
          XXXXXX.txt: "{{ lookup('file', '/secrets/pki-validation.txt') }}"

  - name: Create PKI validation pod
    when: cluster_state == "present"
    kubernetes.core.k8s:
      state: present
      definition:
        apiVersion: v1
        kind: Pod
        metadata:
          name: pki-validation-pod
          namespace: "{{ cluster_name }}-namespace"
          labels:
            app: pki-validation
        spec:
          containers:
            - name: pki-validation-container
              image: nginx:stable
              volumeMounts:
                - name: pki-validation-volume
                  mountPath: /usr/share/nginx/html/.well-known/pki-validation
          volumes:
            - name: pki-validation-volume
              configMap:
                name: pki-validation-config

  - name: Create PKI validation service
    when: cluster_state == "present"
    kubernetes.core.k8s:
      state: present
      definition:
        apiVersion: v1
        kind: Service
        metadata:
          name: pki-validation-service
          namespace: "{{ cluster_name }}-namespace"
        spec:
          ports:
            - port: 80
              targetPort: 80
          selector:
            app: pki-validation
          type: NodePort
  ```

- In the step of creating ingress controller, for the host under `kubernetes.core.k8s.definition.spec.rules`, add the following to its `http.paths`:

  ```yaml
  - path: /.well-known/pki-validation/XXXXXX.txt
    pathType: Exact
    backend:
      service:
        name: pki-validation-service
        port:
          number: 80
  ```

Now run:

```bash
make build
make run command="./deploy-app.sh --skip-rebuild-images=true"
```

This should bring the file to its desired location within a few minutes after successful execution. Then click verify on ZeroSSL. Again, do not commit these to the repository so that next time a workflow is triggered, this validation file will be from the deployment.

</p>
</details>
