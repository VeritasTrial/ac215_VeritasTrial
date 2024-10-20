# AC215 | Milestone 2 | VeritasTrial

- **Team Members:** Yao Xiao, Bowen Xu, Tong Xiao.
- **Group Name:** VeritasTrial

## Background

The rapid growth of clinical trial data, particularly from large repositories like ClinicalTrials.gov, presents significant opportunities for improving healthcare research and patient outcomes. However, the sheer volume of data makes it challenging for researchers, clinicians, and patients to easily find and understand specific trials relevant to their needs. 

To address this, we aim to develop an AI-powered application that enhances the information retrieval process for clinical trials. Leveraging state-of-the-art embedding models, the system will retrieve relevant trials from ClinicalTrials.gov based on user queries. Following retrieval, a conversational AI chatbot will enable users to discuss specific details about a trial, including endpoints, results, and eligibility criteria, providing an intuitive and interactive experience. This innovative approach seeks to streamline access to critical information, fostering more informed decisions in clinical research and patient care.

## Objective

This project aims to develop an AI-powered system that enables users to efficiently search and explore clinical trials within a database. The system will utilize a fine-tuned language model (LLM) to identify and retrieve the most relevant trials based on user queries. It will then allow users to interact with specific trials and provide accurate responses by leveraging both the fine-tuned model and structured clinical trial data stored in the database.

## Pipeline

![49d3be580e15094a994c21cbd1c16fb](https://github.com/user-attachments/assets/78dcfd73-b9bc-43e6-8c3b-d281fb499694)

In particular, we have four separate containers for our pipeline. Please see their respective directories for details:

- [data-pipeline](./src/data-pipeline/): Collect and clean datasets.
- [embedding-model](./src/embedding-model/): Create vector database for querying.
- [construct-qa](./src/construct-qa/): Construct QA pairs for finetuning.
- [finetune-model](./src/finetune-model/): Finetune the model.

## Data Collection

We collected clinical trial data from [ClinicalTrials.gov](https://clinicaltrials.gov/) and filtered 22K data with results. These are used both for creating our vector database, and for finetuning after construted into QA pairs. We also collected 211K medical QA data from the [PubMedQA](https://huggingface.co/datasets/qiaojin/PubMedQA) dataset and used a subset for finetuning, mixed with our constructed QA.

## Embedding Model

We used a small version of the [BGE](https://huggingface.co/BAAI/bge-small-en-v1.5) model for constructing our vector database (using ChromaDB). We have validated the quality of our embeddings by generating N random samples, with one of them being the correct sample, and see if the model can accurately retrieve the correct one. Both the AUROC score (area under the receiver operating characteristic curve) and the MRR score (mean reciprocal rank) are above 0.99, meaning high retrieval accuracy.

## Finetuning Results

We finetuned the Gemini 1.5 Flash model with 29,800 messages (15,764,259 tokens) and 3 epochs. The training metrics during the supervised finetuning progress are as follows:

<p align="center">
  <img width="300" alt="Total loss" src="https://github.com/user-attachments/assets/8ba85aaa-2f71-4f84-bbc5-7758b57edeed">
  <img width="300" alt="Num predictions" src="https://github.com/user-attachments/assets/bc84b82b-b296-4fe2-8396-7690c7a1fa67">
  <img width="300" alt="Fraction of correct next step preds" src="https://github.com/user-attachments/assets/e5491f66-e0a5-442b-be90-b25c006c797c">
</p>

The validation metrics (on a validation set of size 256) during the supervised finetuning progress are as follows:

<p align="center">
  <img width="300" alt="Total loss (validation)" src="https://github.com/user-attachments/assets/9c85ed42-22f0-4066-809d-16cda275fa2d">
  <img width="300" alt="Num predictions (validation)" src="https://github.com/user-attachments/assets/9595733a-19c6-4ea9-b4ee-bca1bcb38922">
  <img width="300" alt="Fraction of correct next step preds (validation)" src="https://github.com/user-attachments/assets/7d1c4a04-3f8e-4d13-a9fc-781375758068">
</p>

## App Interface Design

<p align="center">
  <img width="300" alt="6c82ae3fc63718a00f5b225fc49e447" src="https://github.com/user-attachments/assets/3ac90b63-92d0-48d9-a791-39ee5ae98938">
  <img width="300" alt="0251530ead34fc048822cfb2feacc95" src="https://github.com/user-attachments/assets/d2c419c9-c04e-404f-ab1b-55763c713b08">
  <img width="300" alt="4170d338f651db1b31cabccadb8ea88" src="https://github.com/user-attachments/assets/ec3e74fa-f6ae-47db-8d10-74922caf9213">
</p>
