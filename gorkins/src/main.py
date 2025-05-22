"""
Main script for running the Gorkin bot continuously
"""

import os
import time
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
from bot import GorkinBot

def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize the bot
    bot = GorkinBot()
    
    # Track last action times
    last_tweet_time = datetime.now() - timedelta(minutes=15)  # Start ready to tweet
    last_mention_check = datetime.now() - timedelta(minutes=5)  # Start ready to check mentions
    
    print("🤖 Gorkin bot is starting up...")
    
    while True:
        try:
            current_time = datetime.now()
            
            # Post random thoughts every 15-30 minutes
            if (current_time - last_tweet_time).total_seconds() >= 900:  # 15 minutes
                if random.random() < 0.7:  # 70% chance to tweet
                    bot.post_random_thought()
                last_tweet_time = current_time
            
            # Check mentions every 2 minutes
            if (current_time - last_mention_check).total_seconds() >= 120:
                bot.process_mentions()
                last_mention_check = current_time
            
            # Sleep for a bit to prevent hitting rate limits
            time.sleep(30)
            
        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(60)  # Wait a minute before retrying on error

if __name__ == "__main__":
    main() 