import praw
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Reddit API with environment variables
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    password=os.getenv("REDDIT_PASSWORD"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
    username=os.getenv("REDDIT_USERNAME"),
)

def fetch_posts(subreddit_name, limit=1000):
    try:
        reddit.user.me()
        
        subreddit = reddit.subreddit(subreddit_name)
        posts = []
        for submission in subreddit.hot(limit=limit):
            posts.append(submission)
        return posts
    except Exception as e:
        print(f"Error fetching posts: {str(e)}")
        raise Exception(f"Failed to connect to Reddit API: {str(e)}")

def chunkify(lst, n):
    """Split list `lst` into `n` roughly equal parts."""
    k, m = divmod(len(lst), n)
    return [lst[i*k + min(i, m):(i+1)*k + min(i, m)] for i in range(n)]

def process_posts(posts):
    results = []
    for submission in posts:
        submission.comments.replace_more(limit=0)
        top_comments = [c.body for c in submission.comments[:10]]
        results.append({
            "id": submission.id,
            "title": submission.title,
            "body": submission.selftext,
            "author": str(submission.author),
            "score": submission.score,
            "num_comments": submission.num_comments,
            "top_comments": top_comments
        })
    return results

def scrape_subreddit(subreddit_name, limit=1000):
    posts = fetch_posts(subreddit_name, limit=limit)
    chunks = chunkify(posts, 4)
    all_results = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_posts, chunk) for chunk in chunks]
        for f in futures:
            all_results.extend(f.result())
    df = pd.DataFrame(all_results)
    # df["all_comments"] = df["top_comments"].apply(lambda x: " ".join(x))
    csv_path = f"{subreddit_name}_posts_with_comments.csv"
    df.to_csv(csv_path, index=False)
    return csv_path