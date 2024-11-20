# AC215 | Milestone 4 | VeritasTrial

- **Team Members:** Yao Xiao, Bowen Xu, Tong Xiao.
- **Group Name:** VeritasTrial

## Solution architecture

<img width="742" alt="8e56709f3f5c7044a3e64889bbd83f9" src="https://github.com/user-attachments/assets/a7a53cd4-e2f8-4d76-92ff-d9926b033666">

### Process

1. **Fetch Clinical Trial Data**: Retrieve data from the ClinicalTrials.gov API endpoint.
2. **Data Processing**: Clean and preprocess the fetched data to prepare it for downstream tasks.
3. **Create Vector Embeddings**: Use an embedding model to generate dense vector representations of the data, enabling semantic search and retrieval.
4. **Model Fine-Tuning**: Customize a pre-trained language model to specialize in clinical trial-related tasks for improved accuracy and relevance.
5. **Build Integrated App**: Develop a user-facing application that integrates the fine-tuned model to provide the following functionalities: (1) Find Relevant Clinical Trials: Users can search and retrieve clinical trials using semantic search capabilities. (2) Ask About Specific Trials: Enable a question-answering (QA) functionality for detailed insights into clinical trials.

### Execution

1. **Query Handling**: (1) Generate a vector embedding for the user query. (2) Retrieve the most similar embeddings from the **ChromaDB vector database**.
2. **Metadata Retrieval**: Load and present metadata for the matching clinical trial(s).
3. **RAG for QA**: Use **Retrieval-Augmented Generation (RAG)** to enhance the question-answering process with relevant and contextually accurate data.
4. **LLM for Chatting**: Provide conversational AI capabilities powered by a fine-tuned language model for an interactive and seamless user experience.

### State Management

1. **Data Storage**: (1) Save fetched clinical trial data on **Google Cloud Platform (GCP)**. (2) Store generated QA datasets securely on **GCP**.
2. **Vector Database**: Save vector embeddings in **ChromaDB** to enable efficient search and retrieval of clinical trial information.
3. **Model Hosting**: Deploy and manage the fine-tuned model using **VertexAI**, ensuring robust and scalable inference capabilities.
4. **Source Code Repository**: Use a centralized repository for collaboration and version control, streamlining the development and deployment process.

## Technical architecture

<img width="740" alt="ea0cbf5d4e63f549fc148dc9bc25d58" src="https://github.com/user-attachments/assets/7d0c0fa5-4b7d-4fd1-92b3-75efb1977ccb">

## API & Frontend Implementation

To build our application, simply run:

```bash
cd app
make
```

This composes the backend, the frontend, and the ChromaDB service. See [docker-compose.yaml](./app/docker-compose.yaml). The frontend is built into static assets and served with [nginx](https://nginx.org/).

You may also separately start the backend and the frontend by running the following in two different terminals:

```bash
cd app
make devbackend
make devfrontend  # Supports live reload via Vite
```

Our backend is built with [FastAPI](https://fastapi.tiangolo.com/) in Python. To see the API specifications, start the backend server and visit http://localhost:8001/.

![3e725c2d56915c5498715bdbb4dbb77](https://github.com/user-attachments/assets/9867b2cf-f0e5-4376-9339-5b247b07a2a6)
![993d09a705a4d79b42e3448f2d76f0f](https://github.com/user-attachments/assets/c5adecf4-2f36-4b4e-84f9-034392b57e19)
![9d6c2e387d7b385672bf5acdf0abbca](https://github.com/user-attachments/assets/600153e6-565a-4693-9a96-ca3279eabcf9)
![3588f8c7e28f6d92de1b5f73e249a2c](https://github.com/user-attachments/assets/f5152b71-9311-42f4-9172-f0157de6cee1)

Our frontend is built in React and TypeScript with the [Vite](https://vite.dev/) framework. As follows is the structure of our frontend:

```
frontend/src
├── api.ts       # Wrapper for calling backend APIs
├── App.tsx      # Main application
├── components   # See top comment of each component
│  ├── ChatCollapsibleHint.tsx
│  ├── ChatErrorMessage.tsx
│  ├── ChatInput.tsx
│  ├── ChatPanel.tsx
│  ├── ChatPort.tsx
│  ├── CopyButton.tsx
│  ├── ExternalLink.tsx
│  ├── FCClearHistoryButton.tsx
│  ├── FCDeleteChatButton.tsx
│  ├── FCSendButton.tsx
│  ├── FCTopKSelector.tsx
│  ├── Header.tsx
│  ├── MessageDocs.tsx
│  ├── MessageRetrieved.tsx
│  ├── RetrievePanel.tsx
│  ├── RetrievePanelCommandPalette.tsx
│  └── Sidebar.tsx
├── consts.ts    # Constants
├── main.tsx     # Application entrypoint
├── types.ts     # Type definitions
├── utils.ts     # Utility functions
└── vite-env.d.ts
```

Trial retrieval panel:

![4048c4e3ca8518afe3618319b3fc493](https://github.com/user-attachments/assets/8c3521ac-4294-482f-a8f1-f838767f720e)

Chat panel:

![69a3bf11b423ba4fa47ff0df566b9a4](https://github.com/user-attachments/assets/2fd1d542-8c22-49b1-a98f-011e93c7e521)

Support for dark/light theme:

![88df7f4b4cc8eee3bb2fe09ee902787](https://github.com/user-attachments/assets/3393c49a-da36-42a1-85ac-48cd1fce8634)

## Continuous Integration Setup

We have continuous integration triggered per pull request targeting the main branch and per merged commit to the main branch. This includes:

- [Building](https://github.com/VeritasTrial/ac215_VeritasTrial/actions/workflows/build.yaml): Test that the images for the application can be successfully built.
- [Formatting and Linting](https://github.com/VeritasTrial/ac215_VeritasTrial/actions/workflows/lint.yaml): Check formatting and linting of the codebase to ensure code quality. This applies to both the frontend and the backend. The backend uses [black](https://black.readthedocs.io/en/stable/) for formatting, [ruff](https://docs.astral.sh/ruff/) for linting, and [mypy](https://mypy.readthedocs.io/en/stable/) for static type checking. The frontend uses [prettier](https://prettier.io/) for formatting, and [eslint](https://eslint.org/) and [typescript-eslint](https://typescript-eslint.io/) for linting and type checking.
- [Testing](https://github.com/VeritasTrial/ac215_VeritasTrial/actions/workflows/test.yaml): Test the codebase (backend only) and generate coverage report.

CI success on merged commits to the main branch:

![3aad8e54105929421e7b67ceeb2370d](https://github.com/user-attachments/assets/48d2b329-d43f-41e5-b99c-b2eac8cab7fe)

CI success on pull requests targeting the main branch:

![2f56489e8d7674bf0a61451b42b5c34](https://github.com/user-attachments/assets/7263602c-457a-4bb6-aca4-f5fdf366a669)

We have also configured the dependabot to automatically update the dependencies of our codebase and perform security checks.

![53deadd17b42ecc4d29e1be1eb78ea7](https://github.com/user-attachments/assets/af97a9cd-e519-463b-abf7-6864bfe7194f)

## Automated Test Implementation

To run our backend test suite, you need to create a local development environment. Run the following:

```bash
cd app
make devinstall
make devtest
make devtestcov  # Also generate coverage report
```

We use [pytest](https://docs.pytest.org/en/stable/) for testing and [coverage.py](https://coverage.readthedocs.io/en/7.6.7/) for coverage report.

![4d17e66373660490959fedc0c468e0f](https://github.com/user-attachments/assets/819de5ce-d0f1-4df7-b883-9e36ea41f510)
