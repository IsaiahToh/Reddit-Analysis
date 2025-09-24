import praw
from dotenv import load_dotenv
import os

load_dotenv()

print("Testing Reddit API credentials...")
print(f"Client ID: {os.getenv('REDDIT_CLIENT_ID')}")
print(f"Username: {os.getenv('REDDIT_USERNAME')}")
print(f"User Agent: {os.getenv('REDDIT_USER_AGENT')}")

try:
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        password=os.getenv("REDDIT_PASSWORD"),
        user_agent=os.getenv("REDDIT_USER_AGENT"),
        username=os.getenv("REDDIT_USERNAME"),
    )
    
    user = reddit.user.me()
    print(f"Successfully authenticated as: {user}")
    
except Exception as e:
    print(f"Authentication failed: {e}")