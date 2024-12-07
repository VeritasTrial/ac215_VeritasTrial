#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <CHROMADB_HOST>"
  exit 1
fi

python cli.py embed
python cli.py upload
python cli.py store --host "$1"
