# Reddit Persona Scraper

This project scrapes a Reddit user's posts and comments, then uses Google's Gemini LLM to generate a detailed user persona, citing specific posts and comments as evidence. The persona is saved as a text file for easy review.

## Features

- Scrapes up to 50 posts and 50 comments from any public Reddit user profile
- Generates a structured persona using Gemini 1.5 Flash LLM
- Cites Reddit posts and comments for each persona trait
- Saves the persona as a text file in the `personas` directory

## Project Structure

```
reddit_persona_scraper/
│
├── src/
│   ├── main.py                # Entry point for running the scraper
│   ├── scraper.py             # Reddit scraping logic
│   ├── persona_generator.py   # Persona generation using Gemini LLM
│   ├── utils.py               # Utility functions (e.g., URL parsing)
│   ├── config.py              # Loads environment variables
│   └── __pycache__/           # Python cache files
├── personas/                  # Output folder for generated personas
├── requirements.txt           # Python dependencies
├── .env.example               # Example environment file
└── README.md                  # Project documentation file
```

## Setup Instructions

### 1. Clone the Repository

```sh
git clone https://github.com/Sahil-Garg-01/reddit_persona_scraper.git
cd reddit_persona_scraper
```

### 2. Install Dependencies

Make sure you have Python 3.7+ installed. Then run:

```sh
pip install -r requirements.txt
```

### 3. Create a Reddit App for API Credentials

1. Go to [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)
2. Click **"create another app"** at the bottom
3. Fill in:
   - **name:** Any name (e.g., PersonaScraper)
   - **type:** script
   - **redirect uri:** http://localhost:8080
4. After creation, copy your **client_id** (under the app name) and **client_secret** (labeled "secret")

### 4. Get a Google Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click **"Create API key"** and copy the key

### 5. Configure Environment Variables

Create a `.env` file in the project root with the following content:

```env
client_id=YOUR_CLIENT_ID
client_secret=YOUR_CLIENT_SECRET
user_agent=RedditPersonaScraper/1.0 by u/YOUR_REDDIT_USERNAME
google_api_key=YOUR_GOOGLE_API_KEY
```

Replace the placeholders with your actual credentials.

## Usage

1. **Run the script from the `src` directory:**

   ```sh
   python src/main.py
   ```

2. **When prompted, enter the Reddit user's profile URL:**

   Example:
   ```
   https://www.reddit.com/user/spez/
   ```

3. **Output:**

   - The script will scrape the user's posts and comments, generate a persona, and save it as `personas/<username>_persona.txt`
   - Check the `personas` folder for the result

## Example Output

The generated persona will be saved in the `personas` folder as a text file named after the username (e.g., `spez_persona.txt`). It will contain a structured analysis with sections like:

- Basic Info
- Personality traits
- Motivations
- Behavior & Habits
- Frustrations
- Goals & Needs

Each characteristic will cite specific Reddit posts or comments as evidence.

## Troubleshooting

- **Missing modules?**  
  Run `pip install -r requirements.txt` again

- **Invalid credentials?**  
  Double-check your `.env` file and ensure all keys are correct

- **API limits or errors?**  
  Ensure your Reddit and Google API keys are active and have not exceeded usage limits

## License

This project is for educational and research purposes. Respect Reddit's [API Terms of Use](https://www.reddit.com/wiki/api-terms)