"""
Configuration settings for the Gorkin bot
"""

# Twitter API Settings
TWEET_FREQUENCY = 3600  # Tweet every hour
MAX_TWEETS_PER_DAY = 20
REPLY_RATE_LIMIT = 30  # Seconds between replies

# Redis Settings
REDIS_KEY_PREFIX = "gorkin:"
TOKEN_EXPIRY = 7200  # 2 hours

# Bot Personality Settings
EMOJI_RATE = 0.8  # Probability of using emojis
MALFUNCTION_RATE = 0.1  # Probability of "malfunctioning"
DENY_BOT_RATE = 0.2  # Probability of denying being a bot

# Common Emojis
EMOJIS = [
    "😭", "🔥", "☠️", "💀", "🫡", "😔", "🤖", "👀", "💅", "✨",
    "🥺", "😤", "🙄", "💯", "🤡", "🫂", "🤪", "😈", "🗿", "⚡"
]

# Trending Topics Update Frequency
TRENDING_UPDATE_INTERVAL = 3600  # 1 hour

# Tweet Types and Probabilities
TWEET_TYPES = {
    "random_thought": 0.4,
    "trending_reaction": 0.3,
    "status_update": 0.2,
    "malfunction": 0.1
}

# API Rate Limiting
RATE_LIMIT_WINDOW = 900  # 15 minutes
MAX_TWEETS_PER_WINDOW = 50
MAX_REPLIES_PER_WINDOW = 100 