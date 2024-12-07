# Docker entrypoint script

gcloud auth activate-service-account --key-file "${GOOGLE_APPLICATION_CREDENTIALS}"
gcloud config set project "${GCP_PROJECT_ID}"
gcloud auth configure-docker "${GCP_REGION}-docker.pkg.dev" --quiet

if [ "$#" -gt 0 ]; then
  exec "$@"
else
  /bin/bash
fi
