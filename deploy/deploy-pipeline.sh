#!/bin/bash

ansible-playbook pipeline/deploy-images.yaml -i inventory.yaml
./pipeline/pipeline.py
