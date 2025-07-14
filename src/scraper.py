# scraper.py
import praw
from datetime import datetime
import os
import logging

logger = logging.getLogger(__name__)

class RedditPersonaScraper:
    def __init__(self, client_id, client_secret, user_agent, gemini_model):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        self.gemini_model = gemini_model

    def clean_text(self, text):
        import re
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text.strip())
        return text

    def scrape_user_data(self, username):
        try:
            redditor = self.reddit.redditor(username)
            user_data = {'posts': [], 'comments': []}
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

    def save_persona(self, username, persona):
        try:
            output_dir = "personas"
            os.makedirs(output_dir, exist_ok=True)
            filename = f"{output_dir}/{username}_persona.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"User Persona for {username}\n\n{persona}")
            logger.info(f"Persona saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving persona for {username}: {e}")