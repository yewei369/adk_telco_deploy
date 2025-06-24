#!/bin/bash

# enable_apis.sh: Enables all necessary Google Cloud APIs for the ADK MVP project.

echo "--- Enabling required Google Cloud APIs ---"

# Define the list of APIs
APIS=(
    "artifactregistry.googleapis.com"
    "cloudbuild.googleapis.com"
    "run.googleapis.com"
    "cloudfunctions.googleapis.com"
    "aiplatform.googleapis.com"
    "bigquery.googleapis.com"
    "storage.googleapis.com"
    "calendar-json.googleapis.com"
    "sheets.googleapis.com"
    "customsearch.googleapis.com"
    "meet.googleapis.com"
    "dialogflow.googleapis.com"
)

PROJECT_ID=$(gcloud config get-value project)
echo "Project ID: $PROJECT_ID"

# Loop through the APIs and enable them
for API in "${APIS[@]}"; do
    echo "Enabling $API..."
    gcloud services enable "$API" --project="$PROJECT_ID"
    if [ $? -eq 0 ]; then
        echo "$API enabled successfully."
    else
        echo "WARNING: Failed to enable $API. Please check logs."
    fi
done

echo "--- API enablement process completed ---"