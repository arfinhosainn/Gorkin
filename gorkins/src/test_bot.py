"""
Test script for the Gorkin bot
"""

import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import tweepy
import json

def mask_value(value):
    """Mask a value for secure display"""
    if not value:
        return None
    if len(value) <= 8:
        return "***"
    return value[:4] + "..." + value[-4:]

def test_connection():
    # Try to find .env file
    env_path = find_dotenv()
    print(f"\nLooking for .env file:")
    if env_path:
        print(f"✅ Found .env file at: {env_path}")
        print("\nReading .env file contents:")
        try:
            with open(env_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        try:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip()
                            print(f"Found key: {key} = {mask_value(value)}")
                        except ValueError:
                            print(f"Warning: Invalid line format: {line}")
        except Exception as e:
            print(f"Error reading .env file: {e}")
    else:
        print("❌ Could not find .env file")
        
    # Try loading from project root
    project_root = Path(__file__).parent.parent
    alt_env_path = project_root / '.env'
    print(f"\nChecking project root for .env:")
    print(f"Project root: {project_root}")
    print(f"Looking for: {alt_env_path}")
    if alt_env_path.exists():
        print(f"✅ Found .env file in project root")
        load_dotenv(alt_env_path)
    else:
        print(f"❌ No .env file found in project root")
        
    # Load environment variables
    load_dotenv()
    
    # Debug: Print environment variables (with partial masking for security)
    print("\nChecking environment variables:")
    oauth_keys = ["API_KEY", "API_KEY_SECRET", "ACCESS_TOKEN", "ACCESS_TOKEN_SECRET"]
    for key in oauth_keys:
        value = os.getenv(key)
        if value:
            print(f"✅ {key} is set: {mask_value(value)}")
        else:
            print(f"❌ {key} is not set")
    
    print("\nTesting OAuth 1.0a Authentication:")
    try:
        # Set up OAuth 1.0a authentication
        auth = tweepy.OAuthHandler(
            os.getenv("API_KEY"),
            os.getenv("API_KEY_SECRET")
        )
        auth.set_access_token(
            os.getenv("ACCESS_TOKEN"),
            os.getenv("ACCESS_TOKEN_SECRET")
        )
        
        # Initialize API client
        api = tweepy.API(auth)
        
        # Verify credentials
        me = api.verify_credentials()
        print(f"\n✅ OAuth 1.0a Authentication successful")
        print(f"✅ Authenticated as: @{me.screen_name}")
        
        # Initialize v2 client with OAuth 1.0a tokens
        client = tweepy.Client(
            consumer_key=os.getenv("API_KEY"),
            consumer_secret=os.getenv("API_KEY_SECRET"),
            access_token=os.getenv("ACCESS_TOKEN"),
            access_token_secret=os.getenv("ACCESS_TOKEN_SECRET")
        )
        
        # Try to post a test tweet
        try:
            tweet = client.create_tweet(text="test tweet from gorkin bot... loading... 🤖")
            print(f"✅ Successfully posted test tweet")
        except Exception as e:
            print(f"❌ Failed to post tweet: {e}")
            
    except Exception as e:
        print(f"\n❌ OAuth 1.0a Authentication failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_data = e.response.json()
                print("\nError details:")
                print(json.dumps(error_data, indent=2))
            except:
                if hasattr(e.response, 'status_code'):
                    print(f"Response status code: {e.response.status_code}")
                if hasattr(e.response, 'text'):
                    print(f"Response text: {e.response.text}")

if __name__ == "__main__":
    test_connection() 