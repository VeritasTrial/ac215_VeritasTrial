<div align="center">

<p>
  <img src="https://github.com/user-attachments/assets/15fd14c0-8d62-4781-bb51-20f84afa8a48" width="100">
</p>

# VeritasTrial

Team Members: [Yao Xiao](mailto:yaoxiao@g.harvard.edu), [Bowen Xu](mailto:bowenxu@g.harvard.edu), [Tong Xiao](mailto:tongxiao@g.harvard.edu)

<sup> This project was the final project for the [Harvard AC215 (Fall 2024)](https://harvard-iacs.github.io/2024-AC215/) course. </sup>

|         |          |
|---------|----------|
| Project | [![license](https://img.shields.io/github/license/VeritasTrial/ac215_VeritasTrial)](https://github.com/VeritasTrial/ac215_VeritasTrial/blob/main/LICENSE) [![app](https://img.shields.io/badge/app-VeritasTrial-blue.svg)](https://34.57.211.196.sslip.io/) [![api](https://img.shields.io/badge/api-VeritasTrial-blue.svg)](https://34.57.211.196.sslip.io/api/) [![blog](https://img.shields.io/badge/blog-Medium-12100E.svg)](https://medium.com/@bowenxu_47157/veritastrial-an-ai-driven-app-for-clinical-trial-search-and-interpretation-4b9c281e3548) [![video](https://img.shields.io/youtube/views/MO-pGNcg3QI?style=flat&label=video)](https://youtu.be/MO-pGNcg3QI) |
| Repository | [![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) [![prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier) [![eslint](https://img.shields.io/badge/code%20style-eslint-brightgreen.svg)](http://standardjs.com) [![ts](https://badgen.net/badge/-/TypeScript?icon=typescript&label&labelColor=blue&color=555555)](https://www.typescriptlang.org/) |
| Workflow | [![build](https://img.shields.io/github/actions/workflow/status/VeritasTrial/ac215_VeritasTrial/build.yaml?label=build&logo=github)](https://github.com/VeritasTrial/ac215_VeritasTrial/actions/workflows/build.yaml) [![test](https://img.shields.io/github/actions/workflow/status/VeritasTrial/ac215_VeritasTrial/test.yaml?label=test&logo=github)](https://github.com/VeritasTrial/ac215_VeritasTrial/actions/workflows/test.yaml) [![deploy-app](https://img.shields.io/github/actions/workflow/status/VeritasTrial/ac215_VeritasTrial/deploy-app.yaml?label=app&logo=github)](https://github.com/VeritasTrial/ac215_VeritasTrial/actions/workflows/deploy-app.yaml) [![deploy-pipeline](https://img.shields.io/github/actions/workflow/status/VeritasTrial/ac215_VeritasTrial/deploy-pipeline.yaml?label=pipeline&logo=github)](https://github.com/VeritasTrial/ac215_VeritasTrial/actions/workflows/deploy-pipeline.yaml) [![deploy-chromadb](https://img.shields.io/github/actions/workflow/status/VeritasTrial/ac215_VeritasTrial/deploy-chromadb.yaml?label=chroma&logo=github)](https://github.com/VeritasTrial/ac215_VeritasTrial/actions/workflows/deploy-chromadb.yaml) |

</div>

## Table of Contents

- [Introduction](#introduction)
- [Data Pipeline](#data-pipeline)
- [Model Training & Optimization](#model-training--optimization)
- [Frontend Interface](#frontend-interface)
- [Backend Service](#backend-service)
- [Deployment](#deployment)
- [Future Steps](#future-steps)
- [References](#references)

Subdirectory READMEs:

- [/app](./app/README.md)
- [/deploy](./deploy/README.md)
- [/src/data-pipeline](./src/data-pipeline/README.md)
- [/src/embedding-model](./src/embedding-model/README.md)
- [/src/construct-qa](./src/construct-qa/README.md)
- [/src/finetune-model](./src/finetune-model/README.md)

## Introduction

Clinical trial data includes structured information collected during research studies designed to evaluate the safety, efficacy, and outcomes of medical interventions, treatments, or devices on human participants. In recent years, this type of data has expanded rapidly, especially in large repositories like [ClinicalTrials.gov](https://clinicaltrials.gov/), creating immense opportunities to advance healthcare research and improve patient outcomes. However, the large volume and complexity of such data create challenges for researchers, clinicians, and patients in finding and understanding trials relevant to their specific needs.

One key limitation lies in the search functionality of platforms like [ClinicalTrials.gov](https://clinicaltrials.gov/). The current search is based on fuzzy string matching, which struggles to deliver accurate results when user queries are not precise or involve long, complex sentences. Additionally, even when users locate a specific trial, understanding its details can be challenging due to the technical language and dense structure of the information.

**Solution:** To overcome these challenges, we aim to develop an AI-powered application that improves the information retrieval process for clinical trials. By leveraging state-of-the-art embedding models, our system will retrieve the most relevant trials from [ClinicalTrials.gov](https://clinicaltrials.gov/) based on user queries, even if those queries are less structured or precise. After retrieval, an intuitive conversational AI chatbot will enable users to explore specific details of a trial, such as endpoints, results, and eligibility criteria. Our app can benefit a lot of different user groups. For clinical trial researchers, they can find trials to their needs more accurately and interpret the result more efficiently. For patients, it might help them identify target recruiting clinical trials that they can participate in. This interactive approach streamlines access to critical information, empowering users to make more informed decisions in clinical research and patient care.

![image](https://github.com/user-attachments/assets/2293ba20-303a-47a0-86c1-64429ecf5f3b)

<details>
<summary>Project organization</summary>
<p>

```
├── .github                  > GitHub workflows
│  ├── workflows
│  └── dependabot.yaml
├── app
│  ├── backend/              > VeritasTrial backend
│  ├── frontend/             > VeritasTrial frontend
│  ├── docker-compose.yaml   > VeritasTrial app compose
│  └── Makefile
├── deploy
│  ├── app/                  > App deployment
│  ├── chromadb/             > ChromaDB deployment
│  ├── pipeline/             > Pipeline deployment
│  ├── inventory.yaml        > Ansible inventory
│  └── ...
├── misc/                    > Miscellaneous
├── secrets/                 > Secrets (private)
├── src
│  ├── data-pipeline/        > Data pipeline
│  ├── embedding-model/      > Embedding model
│  ├── construct-qa/         > QA construction (legacy)
│  └── finetune-model/       > Model finetuning (legacy)
├── .gitignore
├── LICENSE
└── README.md
```

</p>
</details>

## Data Pipeline

**Raw data collection:** We begin by collecting clinical trial data from [ClinicalTrials.gov](https://clinicaltrials.gov/) using their API. This data is preprocessed to retain only the necessary columns, focusing on clinical trials that are completed and have results available. These filtered trials are stored as JSONL files in Google Cloud Storage (GCS) buckets for easy access and scalability in downstream task. For more details, see [/src/data-pipeline/](./src/data-pipeline/README.md).

**Training data curation (embedding model):** To finetune our embedding model, we curate a triplet dataset specifically designed to improve its ability to match brief trial titles to corresponding summary-level information. The triplet structure is as follows:

| Query | Positive | Negative                             |
|-------|----------|--------------------------------------|
| Title | Summary  | Summaries from 5 other random trials |

This dataset is tailored for contrastive learning, enabling the embedding model to distinguish between relevant and irrelevant matches effectively. By learning from these structured triplets, the model is better equipped to embed clinical trial titles and summaries into a shared semantic space for improved retrieval accuracy. This step is not included in our pipeline but manually executed in Google Colab; see [/misc/Finetune-BGE.ipynb](./misc/Finetune_BGE.ipynb) for more details.

**Training data curation (LLM):** To finetune the LLM, we use an existing PubMedQA dataset and a self-curated ClinicalTrialQA dataset. For the former, we utilize the [PubMedQA dataset](https://huggingface.co/datasets/qiaojin/PubMedQA) available on Hugging Face, which contains 211K biomedical question-answer pairs derived from PubMed abstracts. This dataset provides a strong foundation for fine-tuning Gemini on domain-specific QA tasks. For the latter, to further specialize the chatbot for clinical trials in our dataset, we generate additional QA pairs directly from trial documents. Using Gemini 1.5 Flash on Vertex AI, we prompt the model to create relevant question-answer pairs based on the context of individual trial documents. This augmented dataset ensures that Gemini is well-equipped to handle nuanced questions about clinical trials, such as eligibility criteria, study results, or endpoints. For more details, see [/src/construct-qa](./src/construct-qa/README.md) (legacy).

**Vector database:** After fine-tuning the embedding model, we embed the summary text for each clinical trial into a high-dimensional vector space. These embeddings, along with relevant metadata (e.g., study phases, conditions, eligibility criteria, etc), are stored in a [ChromaDB](https://www.trychroma.com/) vector database. The database lives in a VM instance in the GCP compute engine, exposing its service. See [/deploy](./deploy/README.md#chromadb) about deploying ChromaDB on GCP. For more details about the pipeline, see [/src/embedding-model](./src/embedding-model/README.md).

We have validated the quality of our embeddings in the vector database by generating N random samples, with one of them being the correct sample, and see if the model can accurately retrieve the correct one. Both the AUROC score (area under the receiver operating characteristic curve) and the MRR score (mean reciprocal rank) are above 0.99, meaning high retrieval accuracy.

## Model Training & Optimization

Our application design involves two model training processes: finetuning the embedding model for trial retrieval and finetuning the LLM for trial interpretation.

**Fintuning the embedding model:** We use [BGE-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5) as the base embedding model and finetuned it with the `sentence-transformers` package with the triplet dataset. We adopt a contrastive learning approach, finetuning the embedding model with the triplet loss function. This step is not included in our pipeline but manually executed in Google Colab; see [/misc/Finetune-BGE.ipynb](./misc/Finetune_BGE.ipynb) for more details.

![image](https://github.com/user-attachments/assets/05b6f26a-ce6c-419c-b4f5-feaba10affce)

**Finetuning the LLM:** We finetuned the Gemini 1.5 Flash model (`gemini-1.5-flash-002`) with 29,800 messages (15,764,259 tokens) and 3 epochs. The learing rate muliplier is 0.1 and the adapter size is 4. No sample is too long to be truncated. The training metrics during the supervised finetuning progress are as follows:

|   |   |   |
|---|---|---|
| ![image](https://github.com/user-attachments/assets/8ba85aaa-2f71-4f84-bbc5-7758b57edeed) | ![image](https://github.com/user-attachments/assets/bc84b82b-b296-4fe2-8396-7690c7a1fa67) | ![image](https://github.com/user-attachments/assets/e5491f66-e0a5-442b-be90-b25c006c797c) |


The validation metrics (on a validation set of size 256) during the supervised finetuning progress are as follows:

|   |   |   |
|---|---|---|
| ![image](https://github.com/user-attachments/assets/9c85ed42-22f0-4066-809d-16cda275fa2d) | ![image](https://github.com/user-attachments/assets/9595733a-19c6-4ea9-b4ee-bca1bcb38922) | ![image](https://github.com/user-attachments/assets/7d1c4a04-3f8e-4d13-a9fc-781375758068) |

## Frontend Interface

See [/app](./app/README.md) for details about the application.

We implemented a frontend prototype application using React and TypeScript to streamline clinical trial retrieval. The interface features a range of filters, including options for eligible sex, study type, study phases, patient types, age range, and result dates, allowing users to customize their search. Users can input their query in a text box, and then the system will retrieve relevant clinical trials that are displayed with the trial title, a clickable link to the trial's endpoint, and a chat icon that enables users to initiate a detailed conversation about the trial. Users can also adjust the number of results to display using the Top K option in the bottom-right corner, with choices of 1, 3, 5, 10, 20, or 30. Additionally, the top-right corner provides quick access to the project's GitHub repository and a toggle for switching between light and dark modes, ensuring a user-friendly experience.

![image](https://github.com/user-attachments/assets/1b0b7fa1-b22e-4670-a147-2d56e4237962)

After selecting a specific trial from the retrieval results, users can proceed to ask detailed questions about the trial, such as its summary, outcome measures, or sponsor information. This functionality is supported through the side chat panel. If the chat icon for a trial is clicked for the first time, a new chat is created in the panel. However, if the trial has already been accessed before, the interface automatically redirects the user to the existing chat for that trial, ensuring continuity and convenience. To return to the retrieval interface, users can simply click the "Trial Retrieval" button at the top of the side panel.

![image](https://github.com/user-attachments/assets/352c31c8-82ad-4c69-99c2-587361d5f834)

There are many more UI/UX designs to enhance user experience that we will not cover here. Some of them include: responsive design for mobile devices, copy button for queries and responses, automatic scroll-into-view for sidebars and chat panels, GitHub-flavored markdown support, etc.

## Backend Service

See [/app](./app/README.md) for details about the application.

We implemented the backend for VeritasTrial using FastAPI to manage RESTful APIs that facilitate seamless communication with the frontend. The backend handles clinical trial retrieval, filtering, and conversational interactions. Below are the implemented API endpoints:

- `/heartbeat`: A `GET` endpoint that checks server health by returning the current timestamp in nanoseconds.
- `/retrieve`: A `GET` endpoint that retrieves clinical trials based on user queries, specified filters (e.g., study type, age range, date range), and the desired number of results (Top K).
- `/meta/{item_id}`: A `GET` endpoint that retrieves metadata for a specific trial using its unique ID.
- `/chat/{model}/{item_id}`: A `POST` endpoint that enables interaction with a generative AI model about a specific trial. Users can ask questions (e.g., trial outcomes, sponsors), and the system provides context-aware answers. Chat sessions are automatically created and destroyed on demand.

## Deployment

For deployment instructions and details, see [/deploy](./deploy/README.md). Here we provide a brief overview.

We use Ansible playbooks to automate the deployment of the VeritasTrial application on Google Kubernetes Engine (GKE). We create or update a Kubernetes cluster with the specified configuration, including node pools and machine types. Then, we deploy the frontend and backend services as Kubernetes Deployments, exposing them via Kubernetes Services. To enable external access and SSL termination, we set up an Nginx Ingress controller. The Ingress routes incoming traffic to the appropriate service based on URL paths. Additionally, we manage secrets for SSL certificates and service account credentials. This automated deployment process ensures consistency, reduces manual effort, and facilitates efficient scaling of the VeritasTrial application.

The deployment of ChromaDB uses Terraform, as suggested in ChromaDB docs. It will deploy a VM instance that runs ChromaDB service. This is separate from the Kubernetes cluster of the frontend and the backend. This is because the vector database is stateful and recreating it is expensive. This isolated design allows us to disaggregate the pipeline workflow (that updates data in the database, executed less frequently) from the app workflow (that accesses data in the database, executed more frequently).

All deployment steps can be triggered by GitHub Actions workflows.

## Future Steps

Taking our goals and objectives into consideration, we aim to expand our project to reach a larger audience and provide greater utility for diverse user groups. Some additional work we might consider includes:

- Multilingual Support: Expand the application to support multiple languages beyond English, enabling users to retrieve and understand clinical trial data in their preferred language.
- Integration with Other Databases: Extend the system to integrate with additional clinical trial databases or medical resources, such as WHO ICTRP or PubMed, to provide users with a more comprehensive dataset.
- Real-Time Updates: Implement real-time updates for clinical trial information to ensure users have access to the most current data, including ongoing trial statuses and newly published results.
- Enhanced Conversational Capabilities: Improve the chatbot’s capabilities to handle more complex and contextual queries, such as comparing multiple trials or answering follow-up questions about a specific trial.
- Data Visualization: Add interactive data visualization tools to help users better understand clinical trial results and other relevant information.

## References

- Chen J, Xiao S, Zhang P, et al. Bge m3-embedding: Multi-lingual, multi-functionality, multi-granularity text embeddings through self-knowledge distillation[J]. arXiv preprint arXiv:2402.03216, 2024. https://arxiv.org/abs/2402.03216
- Jin Q, Dhingra B, Liu Z, et al. Pubmedqa: A dataset for biomedical research question answering[J]. arXiv preprint arXiv:1909.06146, 2019. https://arxiv.org/abs/1909.06146
- Gao T, Yao X, Chen D. Simcse: Simple contrastive learning of sentence embeddings[J]. arXiv preprint arXiv:2104.08821, 2021. https://arxiv.org/abs/2104.08821
