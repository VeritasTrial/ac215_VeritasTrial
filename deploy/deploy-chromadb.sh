#!/bin/bash

cd chromadb
terraform init

terraform import \
  -var-file chroma.tfvars \
  google_compute_instance.chroma_instance \
  veritastrial/us-central1-a/veritas-trial-chromadb || true
terraform import \
  -var-file chroma.tfvars \
  google_compute_firewall.default \
  veritastrial/chroma-allow-ssh-http || true

terraform apply -var-file chroma.tfvars
echo "$(terraform output -raw chroma_instance_ip)" > .instance-ip
