import requests
import time

# TODO:
# 1) check if the post currently has a comment that contains an archive.ph link (used to get around paywalls)
# 2) if the post doesn't currently have an archive link and is behind a paywall, go ahead and post the link
# 3) Allow users to comment on my comments saying remove: X or add: X, if enough users do this X will be removed or added to the list of paywalled_sites
# 4) Figure out a way to have this running "continuously" without overloading the API


def is_paywalled(url):
    paywalled_sites = [
        "nytimes.com",
        "washingtonpost.com",
        "ft.com",
        "theguardian.com",
        "bloomberg.com",
        "hbr.org",  # harvard business review
        "wsj.com",
        "https://www.economist.com/",
        "nationalpost.com",
        "https://www.haaretz.com/",
        "bostonglobe.com",
        "theaustralian.com.au",
        "smh.com.au",
        "theage.com.au",
        "latimes.com",
        "theglobeandmail.com",
        "thetimes.co.uk",
        "thesundaytimes.co.uk",
        "kyivpost.com",
        "independent.co.uk",
    ]

    return any(site in url for site in paywalled_sites)


def get_recent_hn_posts(minutes=10):
    base_url = "https://hacker-news.firebaseio.com/v0"
    new_stories_url = f"{base_url}/newstories.json"
    item_url = f"{base_url}/item/{{}}.json"

    # Calculate the cutoff time (current time - 10 minutes)
    cutoff_time = time.time() - (minutes * 60)

    # Get the latest story IDs
    response = requests.get(new_stories_url)
    if response.status_code != 200:
        print("Error fetching new stories.")
        return []

    story_ids = response.json()
    recent_stories = []

    for story_id in story_ids:
        story_response = requests.get(item_url.format(story_id))
        if story_response.status_code != 200:
            continue

        story = story_response.json()
        # Check if the story has a `time` field and if it's recent
        if "time" in story and story["time"] > cutoff_time:
            recent_stories.append(story)

    return recent_stories


# Fetch recent posts from the last 10 minutes
recent_posts = get_recent_hn_posts(10)
for post in recent_posts:
    print(
        f"Title: {post.get('title')}, URL: {post.get('url')}, Time: {post.get('time')}")
    if (post.get('url') is not None):
        # avoid making additional API calls where possible
        this_url = post.get('url')
        if is_paywalled(this_url):
            print(f"The URL '{this_url}' is likely behind a paywall.")
        else:
            print(
                f"The URL '{this_url}' does not match known paywalled sites.")
    print()
