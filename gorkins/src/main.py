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
    print("🤖 Starting Gorkin bot...")
    print("📝 Loading environment variables...")
    
    # Load environment variables
    load_dotenv()
    
    print("🔄 Initializing bot and authenticating with Twitter...")
    # Initialize the bot (this will validate credentials)
    bot = GorkinBot()
    
    # Track last action times
    last_tweet_time = datetime.now() - timedelta(minutes=15)  # Start ready to tweet
    last_mention_check = datetime.now() - timedelta(minutes=5)  # Start ready to check mentions
    
    print("✨ Bot initialization complete!")
    print("🚀 Bot is now running...")
    print("ℹ️  - Will post random thoughts every 15-30 minutes (70% chance)")
    print("ℹ️  - Will check mentions every 2 minutes")
    print("\nPress Ctrl+C to stop the bot")
    print("-" * 50)
    
    while True:
        try:
            current_time = datetime.now()
            
            # Post random thoughts every 15-30 minutes
            if (current_time - last_tweet_time).total_seconds() >= 900:  # 15 minutes
                if random.random() < 0.7:  # 70% chance to tweet
                    print(f"💭 Attempting to post a random thought... ({datetime.now().strftime('%H:%M:%S')})")
                    bot.post_random_thought()
                last_tweet_time = current_time
            
            # Check mentions every 2 minutes
            if (current_time - last_mention_check).total_seconds() >= 120:
                print(f"👀 Checking for mentions... ({datetime.now().strftime('%H:%M:%S')})")
                bot.process_mentions()
                last_mention_check = current_time
            
            # Sleep for a bit to prevent hitting rate limits
            time.sleep(30)
            
        except KeyboardInterrupt:
            print("\n👋 Shutting down bot gracefully...")
            break
        except Exception as e:
            print(f"❌ Error in main loop: {e}")
            print("⏳ Waiting 60 seconds before retrying...")
            time.sleep(60)

if __name__ == "__main__":
    main() 