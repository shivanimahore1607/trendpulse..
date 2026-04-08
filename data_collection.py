# Task 1 - Data Collection (TrendPulse Project)

import requests
import time
import json
from datetime import datetime
import os

print("Starting data collection...")

# create data folder if not exists
if not os.path.exists("data"):
    os.mkdir("data")

# function to decide category based on title
def get_category(title):
    title = title.lower()

    if "ai" in title or "tech" in title:
        return "technology"
    elif "war" in title or "government" in title:
        return "worldnews"
    elif "game" in title or "player" in title:
        return "sports"
    elif "science" in title or "research" in title:
        return "science"
    elif "movie" in title or "music" in title:
        return "entertainment"
    else:
        return "others"

# API call to get top story IDs
url = "https://hacker-news.firebaseio.com/v0/topstories.json"
response = requests.get(url)

story_ids = response.json()

my_data = []

# loop through first 100 stories
for i in story_ids[:100]:
    try:
        link = f"https://hacker-news.firebaseio.com/v0/item/{i}.json"
        res = requests.get(link)
        story = res.json()

        if story and "title" in story:
            item = {
                "post_id": story.get("id"),
                "title": story.get("title"),
                "category": get_category(story.get("title")),
                "score": story.get("score"),
                "num_comments": story.get("descendants", 0),
                "author": story.get("by"),
                "collected_at": str(datetime.now())
            }

            my_data.append(item)

    except:
        print("Error aaya kisi story me")

# save data into JSON file
date = datetime.now().strftime("%Y%m%d")
file_name = f"data/trends_{date}.json"

with open(file_name, "w") as f:
    json.dump(my_data, f, indent=4)

# final output
print(f"Collected {len(my_data)} stories. Saved to {file_name}")
print("Task 1 completed successfully!")