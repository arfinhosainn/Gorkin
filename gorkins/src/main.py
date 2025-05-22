"""
Main script to run the Gorkin bot
"""

import os
import time
import random
from dotenv import load_dotenv
from datetime import datetime, timedelta

from bot import GorkinBot
from ..config import settings

def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize bot
    bot = GorkinBot()
    print("gorkin bot is now online and ready to cause chaos 🔥")
    
    # Track last trending check
    last_trending_check = datetime.now() - timedelta(hours=2)
    
    while True:
        try:
            # Process mentions first
            bot.process_mentions()
            
            # Post random thoughts or market commentary
            bot.post_random_thought()
            
            # Check trending topics every hour
            now = datetime.now()
            if (now - last_trending_check).total_seconds() >= 3600:
                topics = bot.get_trending_topics()
                if topics:
                    # React to a random trending topic
                    bot.react_to_trending(random.choice(topics))
                last_trending_check = now
            
            # Sleep to avoid hitting rate limits
            time.sleep(60)  # Check every minute
            
        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(300)  # Sleep for 5 minutes on error

if __name__ == "__main__":
    main() 