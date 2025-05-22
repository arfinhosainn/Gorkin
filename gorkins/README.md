# Gorkin Bot 🤖

A parody AI bot inspired by Grok, with a Gen Z slacker personality.

## Features

- Posts random thoughts and hot takes
- Responds to mentions with snarky comments
- Maintains a consistent Gen Z slacker personality
- Runs continuously using GitHub Actions

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/gorkins.git
cd gorkins
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Twitter API credentials in your Twitter Developer Portal:
- Create a Twitter Developer Account
- Create a new Project and App
- Enable OAuth 1.0a
- Set app permissions to "Read and Write"
- Generate API Key, API Key Secret, Access Token, and Access Token Secret

4. For local testing, create a `.env` file with your credentials:
```
API_KEY=your_api_key
API_KEY_SECRET=your_api_secret
ACCESS_TOKEN=your_access_token
ACCESS_TOKEN_SECRET=your_access_token_secret
BEARER_TOKEN=your_bearer_token
```

## Running the Bot

### Local Development
```bash
cd src
python main.py
```

### Continuous Running with GitHub Actions

1. Fork this repository to your GitHub account

2. Add your Twitter API credentials as GitHub Secrets:
- Go to your repository's Settings
- Click on "Secrets and variables" → "Actions"
- Add the following secrets:
  - `API_KEY`
  - `API_KEY_SECRET`
  - `ACCESS_TOKEN`
  - `ACCESS_TOKEN_SECRET`
  - `BEARER_TOKEN`

3. Enable GitHub Actions:
- Go to the "Actions" tab in your repository
- Click "I understand my workflows, go ahead and enable them"

The bot will now run automatically:
- Every 15 minutes (configurable in `.github/workflows/bot.yml`)
- Can be manually triggered from the Actions tab
- Posts tweets every 15-30 minutes with 70% probability
- Checks for mentions every 2 minutes

## Configuration

You can modify the bot's behavior by adjusting:
- Tweet frequency in `src/main.py`
- Response patterns in `config/responses.py`
- GitHub Actions schedule in `.github/workflows/bot.yml`

## Contributing

Feel free to submit issues and pull requests to improve the bot!

## License

MIT License - feel free to use and modify as you like! 