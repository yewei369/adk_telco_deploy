# adk_telco_deploy
Deployment of the ADK agent project which aims to facilitate diagnosis service in telco industry.
Using Google ADK to develop multi-agent for Telco diagnostics

# to setup
cloudshell workspace ~

python3 -m venv .adk
source .adk/bin/activate

export PATH=$PATH:"/home/${USER}/.local/bin"
export GOOGLE_GENAI_USE_VERTEXAI=TRUE
export GOOGLE_CLOUD_PROJECT=hacker2025-team-212-dev
export GOOGLE_CLOUD_LOCATION=us-central1
export MODEL=gemini-2.0-flash-001

python3 -m pip install google-adk==1.2.1
python3 -m pip install -r requirements.txt

git clone https://github.com/yewei369/adk_telco.git

# to containerize
docker build -t telco .
docker run -it --name telco telco


# to deploy
## gcloud init
## gcloud auth application-default login
## GOOGLE_APPLICATION_CREDENTIALS= file from 'gcloud auth application-default login'

gcloud run deploy telco-agent-2 \
--source . \
--region europe-west1 \
--platform managed \
--allow-unauthenticated \
--project hacker2025-team-212-dev \
--set-env-vars="GOOGLE_GENAI_USE_VERTEXAI=TRUE,GOOGLE_CLOUD_PROJECT=hacker2025-team-212-dev,GOOGLE_CLOUD_LOCATION=us-central1,MODEL=gemini-2.0-flash-001,GOOGLE_APPLICATION_CREDENTIALS=application_default_credentials.json" \
--service-account only4cloudrun@hacker2025-team-212-dev.iam.gserviceaccount.com
