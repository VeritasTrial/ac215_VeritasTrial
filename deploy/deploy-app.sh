#!/bin/bash

# This script is used by GitHub Actions
ansible-playbook app/deploy-images.yaml -i inventory.yaml
