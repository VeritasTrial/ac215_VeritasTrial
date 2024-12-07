#!/bin/bash

usage() {
  echo "Usage: $0 [--skip-rebuild-images=false|true]"
  exit 1
}

SKIP_REBUILD_IMAGES="false" # Do not skip by default

if [[ $# -gt 1 ]]; then
  usage
elif [[ $# -eq 1 ]]; then
  case "$1" in
    --skip-rebuild-images=false)
      SKIP_REBUILD_IMAGES="false"
      ;;
    --skip-rebuild-images=true)
      SKIP_REBUILD_IMAGES="true"
      ;;
    *)
      echo "Invalid argument: $1"
      usage
      ;;
  esac
fi

if [[ "${SKIP_REBUILD_IMAGES}" == "false" ]]; then
  ansible-playbook pipeline/deploy-images.yaml -i inventory.yaml
fi
./pipeline/pipeline.py
