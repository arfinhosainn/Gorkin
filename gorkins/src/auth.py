"""
Twitter authentication script for Gorkin bot
"""

import os
import json
import base64
import hashlib
from flask import Flask, request, redirect
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# OAuth 2.0 Settings
client_id = os.getenv("API_KEY")
client_secret = os.getenv("API_KEY_SECRET")
auth_url = "https://twitter.com/i/oauth2/authorize"
token_url = "https://api.twitter.com/2/oauth2/token"
redirect_uri = "http://127.0.0.1:5000/callback"
scopes = ["tweet.read", "tweet.write", "users.read"]

# Generate PKCE challenge
code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8")
code_verifier = code_verifier.replace("=", "")
code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
code_challenge = code_challenge.replace("=", "")

def make_token():
    return OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scopes)

@app.route("/")
def auth():
    """Start the OAuth 2.0 authorization flow"""
    twitter = make_token()
    authorization_url, state = twitter.authorization_url(
        auth_url,
        code_challenge=code_challenge,
        code_challenge_method="S256"
    )
    return redirect(authorization_url)

@app.route("/callback")
def callback():
    """Handle the OAuth 2.0 callback"""
    twitter = make_token()
    token = twitter.fetch_token(
        token_url=token_url,
        client_secret=client_secret,
        code_verifier=code_verifier,
        authorization_response=request.url,
    )
    
    # Save tokens to .env file
    with open(".env", "a") as f:
        f.write(f"\nACCESS_TOKEN={token['access_token']}")
        f.write(f"\nREFRESH_TOKEN={token['refresh_token']}")
    
    return "Authentication successful! You can close this window and start your bot."

if __name__ == "__main__":
    print("Starting authentication server...")
    print("1. Make sure you're logged into your bot's Twitter account in your browser")
    print("2. Visit http://127.0.0.1:5000 to start the authentication process")
    app.run(debug=True) 