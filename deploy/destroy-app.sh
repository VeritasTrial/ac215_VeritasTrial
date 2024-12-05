#!/bin/bash

ansible-playbook app/deploy-k8s.yaml -i inventory.yaml --extra-vars cluster_state=absent
