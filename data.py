import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define the JSON structure with placeholders
def get_json_structure():
    creds_template = {
        "type": os.getenv("TYPE", ""),
        "project_id": os.getenv("PROJECT_ID", ""),
        "private_key_id": os.getenv("PRIVATE_KEY_ID", ""),
        "private_key": os.getenv("PRIVATE_KEY", "").replace("\\n", "\n"),  # Handle multi-line keys
        "client_email": os.getenv("CLIENT_EMAIL", ""),
        "client_id": os.getenv("CLIENT_ID", ""),
        "auth_uri": os.getenv("AUTH_URI", ""),
        "token_uri": os.getenv("TOKEN_URI", ""),
        "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL", ""),
        "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL", ""),
        "universe_domain": os.getenv("UNIVERSE_DOMAIN", ""),
    }
    with open("creds.json", "w") as file:
        json.dump(creds_template, file, indent=4)