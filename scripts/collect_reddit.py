import requests
import pandas as pd
import time

url = "https://arctic-shift.photon-reddit.com/api/posts/search"

all_posts = []
after = None
batch_size = 100
target = 5000

print("Starting Reddit data collection...")

while len(all_posts) < target:
    params = {
        "subreddit": "Accutane",
        "limit": batch_size,
        "sort": "desc"
    }
    if after:
        params["after"] = after

    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        break

    data = response.json()
    posts = data["data"]

    if not posts:
        print("No more posts available.")
        break

    for post in posts:
        all_posts.append({
            "id": post.get("id"),
            "title": post.get("title"),
            "selftext": post.get("selftext"),
            "author": post.get("author"),
            "score": post.get("score"),
            "upvote_ratio": post.get("upvote_ratio"),
            "num_comments": post.get("num_comments"),
            "created_utc": post.get("created_utc"),
            "permalink": post.get("permalink"),
            "flair": post.get("link_flair_text"),
            "url": post.get("url")
        })

    after = posts[-1]["created_utc"]
    print(f"Collected {len(all_posts)} posts so far...")
    time.sleep(1)

df = pd.DataFrame(all_posts)
output_path = r"C:\Users\16315\Desktop\Python\Projects\Accutane Database\processed\reddit_accutane.csv"
df.to_csv(output_path, index=False)
print(f"\nDone. Saved {len(df)} posts to {output_path}")