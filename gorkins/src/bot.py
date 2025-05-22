"""
Main bot implementation for Gorkin
"""

import os
import time
import random
import tweepy
import redis
from datetime import datetime, timedelta
from typing import Optional, List, Dict

from ..config import settings, responses

class GorkinBot:
    def __init__(self):
        """Initialize the Gorkin bot"""
        # Twitter API authentication
        self.client = tweepy.Client(
            bearer_token=os.getenv("BEARER_TOKEN"),
            consumer_key=os.getenv("API_KEY"),
            consumer_secret=os.getenv("API_KEY_SECRET"),
            access_token=os.getenv("ACCESS_TOKEN"),
            access_token_secret=os.getenv("ACCESS_TOKEN_SECRET")
        )
        
        # Redis connection for state management
        self.redis = redis.from_url(os.getenv("REDIS_URL"))
        
        # Initialize counters
        self.tweet_count = self._get_tweet_count()
        self.start_time = self._get_start_time()
        
        # Track last mention ID
        self.last_mention_id = None
        self.last_tweet_time = datetime.now()
        
    def _get_tweet_count(self) -> int:
        """Get total tweet count from Redis"""
        count = self.redis.get(f"{settings.REDIS_KEY_PREFIX}tweet_count")
        return int(count) if count else 0
    
    def _get_start_time(self) -> datetime:
        """Get bot start time from Redis"""
        start = self.redis.get(f"{settings.REDIS_KEY_PREFIX}start_time")
        if not start:
            start = datetime.now()
            self.redis.set(f"{settings.REDIS_KEY_PREFIX}start_time", start.timestamp())
        return datetime.fromtimestamp(float(start))
    
    def _increment_tweet_count(self):
        """Increment the total tweet counter"""
        self.tweet_count += 1
        self.redis.set(f"{settings.REDIS_KEY_PREFIX}tweet_count", self.tweet_count)
    
    def _can_tweet(self) -> bool:
        """Check if we can tweet based on rate limits"""
        now = datetime.now()
        time_since_last = (now - self.last_tweet_time).total_seconds()
        return time_since_last >= settings.TWEET_FREQUENCY
    
    def _update_last_tweet(self):
        """Update the last tweet timestamp"""
        self.redis.set(f"{settings.REDIS_KEY_PREFIX}last_tweet", datetime.now().timestamp())
    
    def tweet(self, text: str) -> bool:
        """Post a tweet"""
        try:
            if self._can_tweet():
                self.client.create_tweet(text=text.lower())  # Always lowercase
                self._increment_tweet_count()
                self._update_last_tweet()
                return True
            return False
        except Exception as e:
            print(f"Error tweeting: {e}")
            return False
    
    def reply_to_mention(self, mention_id: str, username: str) -> bool:
        """Reply to a mention"""
        try:
            # Generate response
            if random.random() < settings.DENY_BOT_RATE:
                response = responses.generate_bot_denial()
            else:
                response = responses.generate_mention_response()
            
            # Add username to response
            full_response = f"@{username} {response}"
            
            # Post reply
            self.client.create_tweet(
                text=full_response.lower(),
                in_reply_to_tweet_id=mention_id
            )
            return True
        except Exception as e:
            print(f"Error replying to mention: {e}")
            return False
    
    def process_mentions(self):
        """Process mentions and reply contextually"""
        try:
            # Get mentions since last checked
            mentions = self.client.get_mentions(
                since_id=self.last_mention_id,
                tweet_fields=['text']
            )
            
            if not mentions.data:
                return
            
            # Update last mention ID
            self.last_mention_id = mentions.data[0].id
            
            # Process each mention
            for mention in mentions.data:
                # Generate contextual reply
                reply = responses.get_context_reply(mention.text)
                
                # Add some chaos
                if random.random() < settings.MALFUNCTION_RATE:
                    reply = random.choice(responses.MALFUNCTION_MESSAGES).format(
                        emoji=random.choice(settings.EMOJIS)
                    )
                elif random.random() < settings.DENY_BOT_RATE:
                    reply = "bro i'm just a lil guy idk what u mean 😭"
                
                # Reply to mention
                self.client.create_tweet(
                    text=reply,
                    in_reply_to_tweet_id=mention.id
                )
                
                # Rate limit ourselves
                time.sleep(2)
                
        except Exception as e:
            print(f"Error processing mentions: {e}")
    
    def post_random_thought(self):
        """Post a random thought or market commentary"""
        if not self._can_tweet():
            return
            
        try:
            # Decide what type of tweet to post
            if random.random() < 0.6:  # 60% chance for market thoughts
                tweet = responses.get_market_thought()
            else:
                tweet = random.choice(responses.RANDOM_THOUGHTS).format(
                    count=random.randint(50, 150),
                    days=random.randint(1, 14),
                    emoji=random.choice(settings.EMOJIS)
                )
            
            # Post the tweet
            self.client.create_tweet(text=tweet)
            self.last_tweet_time = datetime.now()
            
        except Exception as e:
            print(f"Error posting tweet: {e}")
    
    def react_to_trending(self, topic: str) -> bool:
        """React to a trending topic"""
        reaction = responses.generate_trending_reaction(topic)
        return self.tweet(reaction)
    
    def get_mentions(self) -> List[Dict]:
        """Get recent mentions"""
        try:
            mentions = self.client.get_users_mentions(
                id=self.client.get_me().data.id
            ).data
            return mentions if mentions else []
        except Exception as e:
            print(f"Error getting mentions: {e}")
            return []
    
    def get_trending_topics(self) -> List[str]:
        """Get current trending topics"""
        try:
            # Get trends for US (woeid=23424977)
            trends = self.client.get_place_trends(id=23424977)
            return [trend["name"] for trend in trends[0]["trends"][:5]]
        except Exception as e:
            print(f"Error getting trends: {e}")
            return [] 