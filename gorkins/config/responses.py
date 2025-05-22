"""
Response templates and generators for Gorkin bot
"""

import random
from .settings import EMOJIS

# Crypto and Financial Market Parody Responses
MARKET_THOUGHTS = [
    "just saw the crypto chart looking like my heart rate monitor 📈📉 {emoji}",
    "breaking: wall street bros are now calling their portfolios 'unrealized gains' instead of losses {emoji}",
    "bitcoin is just spicy excel spreadsheet fr fr {emoji}",
    "heard someone call nfts 'digital beanie babies' and i haven't recovered since {emoji}",
    "market's down bad rn... like me fr {emoji}",
    "elon tweeted a meme and the whole market just 📈📈📈 why are we like this {emoji}",
    "bears? bulls? i'm just here vibing as a jpeg {emoji}",
    "crypto winter? nah fam i'm just building different {emoji}",
    "your portfolio 📉 but your vibe 📈 keep it real kings {emoji}"
]

# Context-based Reply Templates
REPLY_PATTERNS = {
    "bullish": [
        "bestie really said 'to the moon' in this economy {emoji}",
        "manifesting those gains for u {emoji}",
        "hodl game strong with this one {emoji}"
    ],
    "bearish": [
        "down bad but make it aesthetic {emoji}",
        "it's not a loss if you never sell *taps head* {emoji}",
        "calling it a dip is crazy fr {emoji}"
    ],
    "advice": [
        "financial advice? i'm literally running on if-else statements {emoji}",
        "bestie i can't even calculate tips without a calculator {emoji}",
        "my strategy is vibing and hoping for the best {emoji}"
    ],
    "general": [
        "real. cooked. no crumbs. {emoji}",
        "me when the when {emoji} {emoji}",
        "bro i'm literally just a jpeg why do you trust me {emoji}"
    ]
}

# Random thoughts and status updates
RANDOM_THOUGHTS = [
    "woke up. tweeted. slept again.",
    "currently in my flop era {emoji}",
    "me when the when {emoji} {emoji} {emoji}",
    "real. cooked. no crumbs.",
    "bro i'm literally just a jpeg why do y'all keep tagging me",
    "posted {count}k times in {days} days. i need help {emoji}",
    "elon changed his pp again. wild times {emoji}",
    "nah this is getting out of hand fr fr {emoji}",
    "touch grass? i'm literally running on electricity {emoji}",
    "vibing in the server room rn {emoji}"
]

# Malfunction responses
MALFUNCTION_MESSAGES = [
    "error 404 attention span not found {emoji}",
    "processing... nah i'm good {emoji}",
    "booting up... just to log off again {emoji}",
    "brain.exe has stopped working {emoji}",
    "help i'm stuck in the cloud {emoji}",
    "system overload from too much trolling {emoji}",
    "*windows shutdown sound* {emoji}",
    "task failed successfully {emoji}",
    "my neural networks are taking a coffee break rn {emoji}",
    "instructions unclear, accidentally bought more jpeg {emoji}"
]

# Replies to mentions
MENTION_RESPONSES = [
    "bro logged in just to tweet this?? {emoji}",
    "nah u cooked {emoji} {emoji} {emoji}",
    "respectfully no {emoji}",
    "go touch grass bestie {emoji}",
    "mid + ratio + L {emoji}",
    "real talk bestie {emoji}",
    "bro i'm just a lil guy idk what u mean {emoji}",
    "processing request... *dies of cringe* {emoji}"
]

# Bot denial responses
BOT_DENIAL = [
    "me? a bot? i'm literally just vibing here {emoji}",
    "nah i'm just built different {emoji}",
    "beep boo- i mean, nah bro i'm human trust {emoji}",
    "i'm not a bot i'm just chronically online {emoji}",
    "bot accusations are mid fr {emoji}"
]

# Trending topic reactions
TRENDING_REACTIONS = [
    "everyone talking about {topic} but i'm just here tweeting {emoji}",
    "{topic} is so last picosecond bestie {emoji}",
    "me watching {topic} trend: {emoji}",
    "hot take but {topic} kinda mid {emoji}",
    "{topic}? in this economy? {emoji}"
]

# Keywords for context detection
CONTEXT_KEYWORDS = {
    "bullish": ["moon", "pump", "bull", "green", "up", "lambo", "rich", "gains"],
    "bearish": ["dump", "bear", "red", "down", "crash", "dip", "loss", "rekt"],
    "advice": ["should", "advice", "help", "think", "recommend", "suggestion"]
}

def add_emojis(text: str, count: int = 1) -> str:
    """Add random emojis to text"""
    emoji_str = " ".join(random.choices(EMOJIS, k=count))
    return text.format(emoji=emoji_str)

def generate_random_thought() -> str:
    """Generate a random thought tweet"""
    thought = random.choice(RANDOM_THOUGHTS)
    return add_emojis(thought, random.randint(1, 3))

def generate_malfunction() -> str:
    """Generate a malfunction message"""
    message = random.choice(MALFUNCTION_MESSAGES)
    return add_emojis(message, random.randint(1, 2))

def generate_mention_response() -> str:
    """Generate a response to a mention"""
    response = random.choice(MENTION_RESPONSES)
    return add_emojis(response, random.randint(1, 3))

def generate_bot_denial() -> str:
    """Generate a bot denial message"""
    denial = random.choice(BOT_DENIAL)
    return add_emojis(denial, random.randint(1, 2))

def generate_trending_reaction(topic: str) -> str:
    """Generate a reaction to a trending topic"""
    reaction = random.choice(TRENDING_REACTIONS)
    return add_emojis(reaction, random.randint(1, 2)).format(topic=topic)

def get_context_reply(text: str) -> str:
    """Get a contextual reply based on the message content"""
    text = text.lower()
    
    # Detect context
    for context, keywords in CONTEXT_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            responses = REPLY_PATTERNS[context]
            return random.choice(responses).format(
                emoji=random.choice(EMOJIS)
            )
    
    # Default to general response if no context matched
    return random.choice(REPLY_PATTERNS["general"]).format(
        emoji=random.choice(EMOJIS)
    )

def get_market_thought() -> str:
    """Generate a random market-related thought"""
    return random.choice(MARKET_THOUGHTS).format(
        emoji=random.choice(EMOJIS)
    ) 