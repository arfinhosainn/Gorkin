"""
Main bot implementation for Gorkin
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

import time
import random
from datetime import datetime, timedelta
from typing import Optional, List, Dict

import tweepy
from config import settings, responses

class GorkinBot:
    def __init__(self):
        """Initialize the Gorkin bot"""
        # Twitter API authentication using OAuth 2.0
        self.client = tweepy.Client(
            bearer_token=os.getenv("BEARER_TOKEN"),
            consumer_key=os.getenv("CLIENT_ID"),
            consumer_secret=os.getenv("CLIENT_SECRET"),
            wait_on_rate_limit=True
        )
        
        # Get and store our user ID
        try:
            self.user_id = self.client.get_me()[0].id
        except Exception as e:
            print(f"Error getting user ID: {e}")
            self.user_id = None
        
        # Track last mention ID
        self.last_mention_id = None
        self.last_tweet_time = datetime.now()
        
        # Initialize Redis if URL is provided
        redis_url = os.getenv("REDIS_URL")
        if redis_url:
            import redis
            self.redis = redis.from_url(redis_url)
        else:
            self.redis = None
        
        # Initialize counters
        self.tweet_count = self._get_tweet_count()
        self.start_time = self._get_start_time()
    
    def _get_tweet_count(self) -> int:
        """Get total tweet count from Redis"""
        if self.redis:
            count = self.redis.get(f"{settings.REDIS_KEY_PREFIX}tweet_count")
            return int(count) if count else 0
        return 0
    
    def _get_start_time(self) -> datetime:
        """Get bot start time from Redis"""
        if self.redis:
            start = self.redis.get(f"{settings.REDIS_KEY_PREFIX}start_time")
            if not start:
                start = datetime.now()
                self.redis.set(f"{settings.REDIS_KEY_PREFIX}start_time", start.timestamp())
            return datetime.fromtimestamp(float(start))
        return datetime.now()
    
    def _increment_tweet_count(self):
        """Increment the total tweet counter"""
        if self.redis:
            self.tweet_count += 1
            self.redis.set(f"{settings.REDIS_KEY_PREFIX}tweet_count", self.tweet_count)
    
    def _can_tweet(self) -> bool:
        """Check if we can tweet based on rate limits"""
        now = datetime.now()
        time_since_last = (now - self.last_tweet_time).total_seconds()
        return time_since_last >= settings.TWEET_FREQUENCY
    
    def _update_last_tweet(self):
        """Update the last tweet timestamp"""
        if self.redis:
            self.redis.set(f"{settings.REDIS_KEY_PREFIX}last_tweet", datetime.now().timestamp())
    
    def tweet(self, text: str) -> bool:
        """Post a tweet"""
        try:
            if self._can_tweet():
                self.client.create_tweet(text=text.lower())  # Always lowercase
                self._increment_tweet_count()
                self._update_last_tweet()
                self.last_tweet_time = datetime.now()
                return True
            return False
        except Exception as e:
            print(f"Error tweeting: {e}")
            return False
    
    def reply_to_tweet(self, tweet_id: str, text: str) -> bool:
        """Reply to a tweet"""
        try:
            self.client.create_tweet(
                text=text.lower(),  # Always lowercase
                in_reply_to_tweet_id=tweet_id
            )
            return True
        except Exception as e:
            print(f"Error replying to tweet: {e}")
            return False
    
    def process_mentions(self):
        """Process mentions and reply contextually"""
        try:
            # Get mentions since last checked
            response = self.client.get_users_mentions(
                id=self.user_id,
                since_id=self.last_mention_id,
                tweet_fields=['text']
            )
            
            if not response.data:
                return
            
            # Update last mention ID
            self.last_mention_id = response.data[0].id
            
            # Process each mention
            for mention in response.data:
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
                self.reply_to_tweet(mention.id, reply)
                
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
            self.tweet(tweet)
            
        except Exception as e:
            print(f"Error posting tweet: {e}")
    
    def check_trending_topics(self):
        """Check trending topics and react to them"""
        try:
            # Get trending topics
            topics = self.get_trending_topics()
            if topics:
                # React to a random topic
                topic = random.choice(topics)
                self.react_to_trending(topic)
        except Exception as e:
            print(f"Error checking trending topics: {e}")
    
    def react_to_trending(self, topic: str) -> bool:
        """React to a trending topic"""
        reaction = responses.generate_trending_reaction(topic)
        return self.tweet(reaction)
    
    def get_trending_topics(self) -> List[str]:
        """Get current trending topics"""
        try:
            # Get trends for US (woeid=23424977)
            # Note: This requires elevated access to the Twitter API
            response = self.client.get_trending_topics(id=23424977)
            if response and response.data:
                return [trend.name for trend in response.data[:5]]
            return []
        except Exception as e:
            print(f"Error getting trends: {e}")
            return [] 