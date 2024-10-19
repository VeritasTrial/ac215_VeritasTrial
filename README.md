# AC215 | Milestone 2 | VeritasTrial

**Team Members:** Yao Xiao, Bowen Xu, Tong Xiao.

**Group Name:** VeritasTrial

**Project:** This project aims to develop an AI-powered system that enables users to efficiently search and explore clinical trials within a database. The system will utilize a fine-tuned language model (LLM) to identify and retrieve the most relevant trials based on user queries. It will then allow users to interact with specific trials and provide accurate responses by leveraging both the fine-tuned model and structured clinical trial data stored in the database.

![49d3be580e15094a994c21cbd1c16fb](https://github.com/user-attachments/assets/78dcfd73-b9bc-43e6-8c3b-d281fb499694)

We have four parts for our pipeline:

- [data-pipeline](./src/data-pipeline/): Collect and clean datasets.
- [embedding-model](./src/embedding-model/): Create vector database for querying.
- [construct-qa](./src/construct-qa/): Construct QA pairs for finetuning.
- [finetune-model](./src/finetune-model/): Finetune the model.

As follows is our app design:

<img width="600" alt="6c82ae3fc63718a00f5b225fc49e447" src="https://github.com/user-attachments/assets/3ac90b63-92d0-48d9-a791-39ee5ae98938">
<img width="600" alt="0251530ead34fc048822cfb2feacc95" src="https://github.com/user-attachments/assets/d2c419c9-c04e-404f-ab1b-55763c713b08">
<img width="600" alt="4170d338f651db1b31cabccadb8ea88" src="https://github.com/user-attachments/assets/ec3e74fa-f6ae-47db-8d10-74922caf9213">
