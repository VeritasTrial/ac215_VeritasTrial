# Data Pipeline

## Instructions

Make sure you are in this directory. To run the data pipeline:

```bash
make build
make run
```

This should bring you within the Docker container. Then inside the container, you can:

```bash
python cli.py fetch   # Fetch data from API
python cli.py clean   # Clean fetched data
python cli.py upload  # Upload cleaned data to GCP
```
