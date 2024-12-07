#!/bin/bash

ansible-playbook app/deploy-images.yaml -i inventory.yaml
CHROMADB_HOST=$(cat chromadb/.instance-ip) ansible-playbook app/deploy-k8s.yaml -i inventory.yaml --extra-vars cluster_state=present
