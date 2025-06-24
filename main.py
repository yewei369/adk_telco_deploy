import logging
from telco_agent.agent import root_agent

if __name__=='__main__':
    logging.info(f"Initializing OrderRequesterAgent with:")
    logging.info(f"  Project ID: {os.getenv('GOOGLE_CLOUD_PROJECT')}")
    logging.info(f"  Location: {os.getenv('GOOGLE_CLOUD_LOCATION')}")
    root_agent.run()