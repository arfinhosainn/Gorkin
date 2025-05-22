from datetime import datetime
import random

class Bot:
    def tweet(self, text: str) -> bool:
        """Post a tweet"""
        try:
            if self._can_tweet():
                print(f"📝 Attempting to post tweet: {text}")
                response = self.client.create_tweet(text=text.lower())  # Always lowercase
                if response and response.data:
                    tweet_id = response.data['id']
                    print(f"✅ Successfully posted tweet with ID: {tweet_id}")
                    self._increment_tweet_count()
                    self._update_last_tweet()
                    self.last_tweet_time = datetime.now()
                    return True
                else:
                    print("❌ Tweet creation failed - no response data")
                    return False
            else:
                print("⏳ Can't tweet yet - waiting for rate limit")
                return False
        except Exception as e:
            print(f"❌ Error tweeting: {str(e)}")
            print(f"Error details: {type(e).__name__}")
            return False

    def post_random_thought(self):
        """Post a random thought or market commentary"""
        if not self._can_tweet():
            print("⏳ Waiting for tweet cooldown...")
            return
            
        try:
            # Decide what type of tweet to post
            if random.random() < 0.6:  # 60% chance for market thoughts
                tweet = responses.get_market_thought()
                print(f"💭 Generated market thought: {tweet}")
            else:
                tweet = random.choice(responses.RANDOM_THOUGHTS).format(
                    count=random.randint(50, 150),
                    days=random.randint(1, 14),
                    emoji=random.choice(settings.EMOJIS)
                )
                print(f"💭 Generated random thought: {tweet}")
            
            # Post the tweet
            success = self.tweet(tweet)
            if success:
                print("✨ Tweet posted successfully!")
            else:
                print("❌ Failed to post tweet")
            
        except Exception as e:
            print(f"❌ Error in post_random_thought: {str(e)}")
            print(f"Error details: {type(e).__name__}") 