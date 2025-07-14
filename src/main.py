# main.py
import logging
import google.generativeai as genai
from config import get_reddit_credentials, get_gemini_api_key
from scraper import RedditPersonaScraper
from persona_generator import PersonaGenerator
from utils import extract_username_from_url

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    client_id, client_secret, user_agent = get_reddit_credentials()
    if not all([client_id, client_secret, user_agent]):
        print("Reddit API credentials not found in environment variables.")
        return

    api_key = get_gemini_api_key()
    if not api_key:
        print("google_api_key environment variable not set.")
        return
    genai.configure(api_key=api_key)
    gemini_model = genai.GenerativeModel("gemini-1.5-flash")

    scraper = RedditPersonaScraper(client_id, client_secret, user_agent, gemini_model)
    persona_gen = PersonaGenerator(gemini_model)

    profile_url = input("Enter the Reddit user's profile URL: ").strip()
    username = extract_username_from_url(profile_url)
    if not username:
        print("Invalid Reddit profile URL.")
        return

    logger.info(f"Processing user: {username}")
    user_data = scraper.scrape_user_data(username)
    if user_data:
        persona = persona_gen.generate_persona(user_data, username)
        scraper.save_persona(username, persona)
        print(f"Persona for {username} saved successfully.")
    else:
        print("Failed to scrape user data.")

if __name__ == "__main__":
    main()