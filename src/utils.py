# utils.py
import re
import logging

logger = logging.getLogger(__name__)

def extract_username_from_url(profile_url):
    match = re.search(r'reddit\.com/(?:user|u)/([A-Za-z0-9_-]+)', profile_url)
    if match:
        return match.group(1)
    else:
        logger.error(f"Could not extract username from URL: {profile_url}")
        return None