# Deploy

The deployment commands are automated with GitHub Actions. It is preferred to trigger the corresponding workflow instead of running the command manually. Go to the "Actions" tab on GitHub and choose "Deploy App", "Deploy pipeline", or "Deploy ChromaDB", and click "Run workflow". Note that each such workflow run may further create a pull request because it may update infomation like Docker tags. Such pull requests will be auto-merged into main on CI success.

Example of a workflow trigger:

![image](https://github.com/user-attachments/assets/998c4b0b-4e82-4af0-92e7-ef68f778368f)

Example of a pull request created by the workflow:

![image](https://github.com/user-attachments/assets/11debd70-629a-48e8-985e-d1b99dd37ef1)

Next we will show the manual deployment instructions, but they are only for demonstration purposes. Make sure you have `veritas-trial-deployment.json` and `veritas-trial-service.json` under the `/secrets/` directory if you are deploying manually. You should also have `certificate.crt` and `private.key` under the `/secrets/` directory, which are for SSL certification (e.g., from ZeroSSL, see the [Others](#others) section). Now enter this directory, then build and run the deployment container:

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

The frontend and backend Docker images will be upload to GCP artifact registry `us-central1-docker.pkg.dev`. The Docker tag pointing to the latest version of the images will be updated via an automatic PR.

| Frontend | Backend |
|:--------:|:-------:|
| ![image](https://github.com/user-attachments/assets/b048f6f9-68a8-40bc-b984-fb71f2b11fbb) | ![image](https://github.com/user-attachments/assets/f370c95f-b041-427c-8f8d-f52f2408a7b6) |

The Kubernetes cluster will be automatically deployed or updated on GCP Kubernetes engine:

![image](https://github.com/user-attachments/assets/81ada5f1-d374-4228-adfd-a893f0a9f96a)


## Pipeline

The deployment uses Ansible and Vertex AI pipeline. It will deploy the Docker images of the pipeline and run `/src/data-pipeline/` and `/src/embedding-model/` steps. Inside the container, run:

```bash
./deploy-pipeline.sh # Deploy pipeline (optionally --skip-rebuild-images=true)
```

A new pipeline run will be created in Vertex AI:

![image](https://github.com/user-attachments/assets/2d8e03cf-0336-431d-864e-491d255c689e)

Example of a successful pipeline run with Vertex AI pipelines:

![image](https://github.com/user-attachments/assets/39a19548-d171-4a40-97d8-d7c8adb2a9a6)

## ChromaDB

The deployment uses Terraform, as suggested in [ChromaDB docs](https://docs.trychroma.com/deployment/gcp). It will deploy a VM instance that runs ChromaDB service. Note that redeploying ChromaDB will destroy the old VM instance and create a new one, so the IP address to access the service will change. The IP is tracked in the `/deploy/chromadb/.instance-ip` file and will be automatically used by other parts of the system, but a redeployment of both the app and the pipeline is required for the changes to take effect. The following script will not do that automatically, but the corresponding workflow in GitHub Actions will. Inside the container, run:

```bash
./deploy-chromadb.sh  # Deploy ChromaDB instance
./destroy-chromadb.sh # Destroy ChromaDB instance
```

The ChromaDB service deployed on GCP compute engine:

![image](https://github.com/user-attachments/assets/31d49990-3596-4228-9946-6919e40e15ae)

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
