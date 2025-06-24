# ~/adk-comcast-mvp/main.py

import os
import logging
import json
from fastapi import FastAPI, Request
from google_generative_ai_toolkit.orchestrator import Orchestrator
from google_generative_ai_toolkit.orchestrator.orchestrator import AgentEngineOutput

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables (e.g., from a .env file for local development)
from dotenv import load_dotenv
load_dotenv()

# Initialize the FastAPI app
app = FastAPI()

# Initialize the Orchestrator using agent_registry.yaml
# The agent_registry.yaml should be in the same directory as this main.py
try:
    orchestrator = Orchestrator(agent_registry_path="agent_registry.yaml")
    logger.info("ADK Orchestrator initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize Orchestrator: {e}")
    # Exit or raise error, as orchestrator won't function
    raise e 

@app.get("/")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok", "message": "ADK Orchestrator is running."}

@app.post("/agent_engine")
async def handle_agent_engine(request: Request):
    """
    Endpoint for Dialogflow CX's webhook.
    This is where the ADK Orchestrator receives the session context
    and dispatches to the appropriate agents.
    """
    try:
        request_json = await request.json()
        logger.info(f"Received Agent Engine request: {json.dumps(request_json, indent=2)}")

        # Process the request with the ADK Orchestrator
        # The orchestrator will determine which agent to call based on its internal logic
        # and the state/input from the Dialogflow CX session.
        adk_output: AgentEngineOutput = await orchestrator.call_agent_engine(request_json)

        # The orchestrator's output is what Dialogflow CX expects back.
        # It contains messages, session_parameters, and a signal (e.g., END_SESSION).
        response_data = adk_output.to_dict()
        logger.info(f"Orchestrator response: {json.dumps(response_data, indent=2)}")

        return response_data

    except Exception as e:
        logger.error(f"Error handling agent_engine request: {e}", exc_info=True)
        # Return an error response that Dialogflow CX can understand
        return {
            "fulfillmentResponse": {
                "messages": [
                    {
                        "text": {
                            "text": [f"An internal error occurred: {str(e)}"]
                        }
                    }
                ]
            },
            "sessionInfo": {
                "parameters": {
                    "last_error": str(e)
                }
            }
        }