# App

Make sure you are under the current directory and that you have `veritas-trial-service.json` under the `/secrets/` directory. To build and run our application locally, simply run:

```bash
make
```

This command composes the backend and the frontend. This also requires proper access to the remotely deployed ChromaDB service. The frontend interface will be available at http://localhost:8080, and the backend service will be available at http://localhost:8001.

Alternatively, for development purposes, you may start the frontend and the backend separetely, First install necessarily dependencies. Make sure you have `node` and `pnpm` ready for the frontend, and `pipenv` ready for the backend. Run:

```bash
make devinstall
```

Then in two different terminals, run the following two commands to start the frontend and the backend separately:

```bash
make devfrontend
make devbackend
```

The `make devfrontend` command relies on the Vite server that supports live reload which makes frontend development much easier. The `make devbackend` builds the backend Docker container and starts its service.

## Frontend Interface

> [!NOTE]
> Our frontend interface is temporarily deployed at: https://34.57.211.196.sslip.io/. The deployment will be removed after the end of the semester.

Our frontend is build with React and TypeScript with the Vite framework. As follows is the structure of our frontend:

```
├── public/                  > Public assets
├── src
│  ├── components/           > React functional components
│  ├── api.ts                > Wrappers for backend API calls
│  ├── App.tsx               > Main application
│  ├── consts.ts             > Constants
│  ├── global.css            > Global style sheet
│  ├── main.tsx              > Application entrypoint
│  ├── types.ts              > Type definitions
│  ├── utils.ts              > Utility functions
│  └── vite-env.d.ts
├── .dockerignore
├── .prettierignore
├── Dockerfile
├── eslint.config.js
├── index.html
├── package.json
├── pnpm-lock.yaml
├── tsconfig.app.json
├── tsconfig.json
├── tsconfig.node.json
└── vite.config.ts
```

The retrieval panel:

![image](https://github.com/user-attachments/assets/b1a23299-aedc-40b8-9ea9-056e354afb66)

The chat session:

![image](https://github.com/user-attachments/assets/612b9e76-3d1c-442b-9a9a-e776eae71e58)

## Backend Service

> [!NOTE]
> Our backend service is temporarily deployed at: https://34.57.211.196.sslip.io/api/. The deployment will be removed after the end of the semester.

Our backend is built with FastAPI in Python. As follows are the API specifications:

![3e725c2d56915c5498715bdbb4dbb77](https://github.com/user-attachments/assets/9867b2cf-f0e5-4376-9339-5b247b07a2a6)
![993d09a705a4d79b42e3448f2d76f0f](https://github.com/user-attachments/assets/c5adecf4-2f36-4b4e-84f9-034392b57e19)
![9d6c2e387d7b385672bf5acdf0abbca](https://github.com/user-attachments/assets/600153e6-565a-4693-9a96-ca3279eabcf9)
![3588f8c7e28f6d92de1b5f73e249a2c](https://github.com/user-attachments/assets/f5152b71-9311-42f4-9172-f0157de6cee1)

## Continuous Integration Setup

We have continuous integration triggered per pull request targeting the main branch and per merged commit to the main branch. This includes:

- [Building](https://github.com/VeritasTrial/ac215_VeritasTrial/actions/workflows/build.yaml): Test that the images for the application can be successfully built.
- [Formatting and Linting](https://github.com/VeritasTrial/ac215_VeritasTrial/actions/workflows/lint.yaml): Check formatting and linting of the codebase to ensure code quality. This applies to both the frontend and the backend. The backend uses [black](https://black.readthedocs.io/en/stable/) for formatting, [ruff](https://docs.astral.sh/ruff/) for linting, and [mypy](https://mypy.readthedocs.io/en/stable/) for static type checking. The frontend uses [prettier](https://prettier.io/) for formatting, and [eslint](https://eslint.org/) and [typescript-eslint](https://typescript-eslint.io/) for linting and type checking.
- [Testing](https://github.com/VeritasTrial/ac215_VeritasTrial/actions/workflows/test.yaml): Test the codebase (backend only) and generate coverage report.

| CI success on merging to main | CI success on PR targetting main |
|:-----------------------------:|:--------------------------------:|
| ![3aad8e54105929421e7b67ceeb2370d](https://github.com/user-attachments/assets/48d2b329-d43f-41e5-b99c-b2eac8cab7fe) | ![2f56489e8d7674bf0a61451b42b5c34](https://github.com/user-attachments/assets/7263602c-457a-4bb6-aca4-f5fdf366a669) |

We have also configured the dependabot to automatically update the dependencies of our codebase and perform security checks.

## Automated Test Implementation

To run our backend test suite, you need to create a local development environment. Run the following:

```bash
make devtest
make devtestcov  # Also generate coverage report
```

We use [pytest](https://docs.pytest.org/en/stable/) for testing and [coverage.py](https://coverage.readthedocs.io/en/7.6.7/) for coverage report.

![image](https://github.com/user-attachments/assets/208453ae-2c3e-46c4-b1f2-393f452d10e6)
