# config.py
import os
from dotenv import load_dotenv

load_dotenv()

def get_reddit_credentials():
    client_id = os.getenv("client_id")
    client_secret = os.getenv("client_secret")
    user_agent = os.getenv("user_agent")
    return client_id, client_secret, user_agent

def get_gemini_api_key():
    return os.getenv("google_api_key")