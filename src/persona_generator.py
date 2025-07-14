# persona_generator.py
import logging

logger = logging.getLogger(__name__)

class PersonaGenerator:
    def __init__(self, gemini_model):
        self.gemini_model = gemini_model

    def generate_persona(self, user_data, username):
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