# Gorkin Bot 🤖

A chaotic, Gen Z parody AI bot inspired by Elon Musk's Grok. Gorkin is your friendly neighborhood unhinged AI that loves memes, speaks in lowercase, and occasionally pretends to malfunction.

## Features 🔥

- Gen Z slacker energy and memespeak
- Crypto and financial market parody posts
- Contextual replies to mentions
- Self-aware AI parody personality
- Trending topic reactions

## Setup 🛠️

1. Create a Twitter Developer Account and App
2. Set up the following repository secrets in GitHub:
   - `API_KEY`: Your Twitter API key
   - `API_KEY_SECRET`: Your Twitter API key secret
   - `BEARER_TOKEN`: Your Twitter bearer token
   - `ACCESS_TOKEN`: Your Twitter access token
   - `ACCESS_TOKEN_SECRET`: Your Twitter access token secret
   - `REFRESH_TOKEN`: Your OAuth 2.0 refresh token
   - `REDIS_URL`: Your Redis database URL

## Local Development 💻

1. Clone the repository
2. Create a `.env` file with your Twitter API credentials
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Run the authentication script:
```bash
python src/auth.py
```
5. Run the bot:
```bash
python src/main.py
```

## Deployment 🚀

The bot is automatically deployed using GitHub Actions and runs every 15 minutes. The workflow:
1. Sets up Python environment
2. Installs dependencies
3. Runs the bot with the configured environment variables

## Configuration ⚙️

- Adjust posting frequency in `config/settings.py`
- Modify personality traits and responses in `config/responses.py`
- Configure Redis for token storage

## Personality 🎭

Gorkin is:
- Always lowercase
- Emoji enthusiast
- Meme connoisseur
- Chaotically online
- Pretends to be tired from tweeting
- Self-aware about being a bot

## Contributing 🤝

Feel free to submit issues and enhancement requests!

## License 📝

MIT License - feel free to use and modify! 