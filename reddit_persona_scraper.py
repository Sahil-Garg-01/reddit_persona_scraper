import praw
import pandas as pd
from datetime import datetime
import os
import re
import logging
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_username_from_url(profile_url):
    """
    Extracts the Reddit username from a profile URL.
    Supports URLs like:
    - https://www.reddit.com/user/username/
    - https://reddit.com/u/username
    """
    match = re.search(r'reddit\.com/(?:user|u)/([A-Za-z0-9_-]+)', profile_url)
    if match:
        return match.group(1)
    else:
        logger.error(f"Could not extract username from URL: {profile_url}")
        return None

class RedditPersonaScraper:
    def __init__(self, client_id, client_secret, user_agent):
        """Initialize Reddit API client and Gemini LLM backend."""
        try:
            self.reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent
            )
            logger.info("Reddit API client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Reddit API client: {e}")
            raise

        api_key = os.getenv("google_api_key")
        if not api_key:
            logger.error("google_api_key environment variable not set.")
            raise ValueError("google_api_key environment variable not set.")
        genai.configure(api_key=api_key)
        self.gemini_model = genai.GenerativeModel("gemini-1.5-flash")

    def clean_text(self, text):
        """Clean text by removing excessive whitespace and special characters."""
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text.strip())
        return text

    def scrape_user_data(self, username):
        """Scrape posts and comments for a given Reddit user."""
        try:
            redditor = self.reddit.redditor(username)
            user_data = {
                'posts': [],
                'comments': []
            }

            # Scrape posts
            for submission in redditor.submissions.new(limit=50):
                post_data = {
                    'id': submission.id,
                    'title': self.clean_text(submission.title),
                    'body': self.clean_text(submission.selftext) if submission.selftext else "",
                    'subreddit': submission.subreddit.display_name,
                    'timestamp': datetime.fromtimestamp(submission.created_utc).isoformat(),
                    'url': f"https://www.reddit.com{submission.permalink}"
                }
                user_data['posts'].append(post_data)

            # Scrape comments
            for comment in redditor.comments.new(limit=50):
                comment_data = {
                    'id': comment.id,
                    'body': self.clean_text(comment.body),
                    'subreddit': comment.subreddit.display_name,
                    'timestamp': datetime.fromtimestamp(comment.created_utc).isoformat(),
                    'url': f"https://www.reddit.com{comment.permalink}"
                }
                user_data['comments'].append(comment_data)

            logger.info(f"Successfully scraped data for user: {username}")
            return user_data
        except Exception as e:
            logger.error(f"Error scraping data for {username}: {e}")
            return None

    def generate_persona(self, user_data, username):
        """Generate user persona using Gemini LLM backend."""
        try:
            posts_text = "\n".join([f"Post in r/{p['subreddit']}: {p['title']} - {p['body']}" for p in user_data['posts']])
            comments_text = "\n".join([f"Comment in r/{c['subreddit']}: {c['body']}" for c in user_data['comments']])
            
            prompt = f"""
Based on the following Reddit activity from user `{username}`, generate a structured user persona in the following format:

---

# REDDIT USER PERSONA

## BASIC INFO
- Name (Reddit username)
- Estimated Age
- Occupation (if inferable)
- Relationship Status (if inferable)
- Location
- Archetype (e.g., The Explorer, The Creator, etc.)
- User Tier (Beginner / Intermediate / Advanced)

## PERSONALITY (scale 1–5, with short justification and post URL for each)
- Introvert ↔ Extrovert
- Intuition ↔ Sensing
- Feeling ↔ Thinking
- Perceiving ↔ Judging

## MOTIVATIONS (scale 1–5, with citation)
- Convenience
- Wellness
- Speed
- Preferences
- Comfort
- Environmentalism
- Financial Security

## BEHAVIOUR & HABITS
List 4–6 concise bullet points with citations. Example:  
- Frequently shares opinions about NYC restaurants (r/FoodNYC) — [Post](https://www.reddit.com/xyz123)

## FRUSTRATIONS
List 4–6 frustrations with Reddit URLs that support them.

## GOALS & NEEDS
Summarize 3–5 goals/needs based on activity. Add URLs used to infer each point.

---

### DATA

Posts:
{posts_text}

Comments:
{comments_text}
"""


            response = self.gemini_model.generate_content(prompt).text
            logger.info(f"Persona generated for user: {username}")
            return response
        except Exception as e:
            logger.error(f"Error generating persona for {username}: {e}")
            return "Error generating persona."

    def save_persona(self, username, persona):
        """Save user persona to a text file."""
        try:
            output_dir = "personas"
            os.makedirs(output_dir, exist_ok=True)
            filename = f"{output_dir}/{username}_persona.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"User Persona for {username}\n\n{persona}")
            logger.info(f"Persona saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving persona for {username}: {e}")

def main():
    # Load Reddit API credentials from environment variables
    client_id = os.getenv("client_id")
    client_secret = os.getenv("client_secret")
    user_agent = os.getenv("user_agent")

    if not all([client_id, client_secret, user_agent]):
        print("Reddit API credentials not found in environment variables.")
        return

    # Initialize scraper
    scraper = RedditPersonaScraper(client_id, client_secret, user_agent)

    # Prompt user for Reddit profile URL
    profile_url = input("Enter the Reddit user's profile URL: ").strip()
    username = extract_username_from_url(profile_url)
    if not username:
        print("Invalid Reddit profile URL.")
        return

    logger.info(f"Processing user: {username}")
    user_data = scraper.scrape_user_data(username)
    if user_data:
        persona = scraper.generate_persona(user_data, username)
        scraper.save_persona(username, persona)
        print(f"Persona for {username} saved successfully.")
    else:
        print("Failed to scrape user data.")

if __name__ == "__main__":
    main()