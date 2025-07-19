from dotenv import load_dotenv
import os

load_dotenv()

# jangan di edit, bikin .env
PROJECT_ID = os.getenv('GCP_PROJECT_ID')
ZONE = os.getenv('GCP_ZONE')
INSTANCE_NAME = os.getenv('GCP_INSTANCE_NAME')
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not all([PROJECT_ID, ZONE, INSTANCE_NAME, BOT_TOKEN]):
    raise ValueError("KURANG .ENV THINGY")
