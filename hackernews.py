import requests
import time

# TODO:
# 1) Check if the post currently has a comment that contains an archive.ph link (used to get around paywalls)
# 2) It appears there's no way to make posts using the HN API, so instead we could analyze the posts and maintain a list of recent posts that contain links that might be behind a paywall that don't already have an 'archive.ph' link commented.
# 3) This way, it would allow anyone with a mind to do some civic service to manually step through those posts and add archive links to them.
# 4) Figure out a way to have this running "continuously" without overloading the API
# 5) A possible addition might be to go ahead and grab an 'archive.ph' link and provide that to the user to minimize repetative tasks.


def is_paywalled(url):
    paywalled_sites = [
        "nytimes.com",
        "washingtonpost.com",
        "ft.com",
        "theguardian.com",
        "bloomberg.com",
        "hbr.org",
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
        "independent.co.uk"
    ]

    return any(site in url for site in paywalled_sites)


def get_recent_hn_posts(minutes=10):
    base_url = "https://hacker-news.firebaseio.com/v0"
    new_stories_url = f"{base_url}/newstories.json"
    item_url = f"{base_url}/item/{{}}.json"

    # Calculate the cutoff time (current time - N minutes)
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

if __name__ == "__main__":
    # Fetch recent posts from the last 10 minutes
    recent_posts = get_recent_hn_posts(10)
    for post in recent_posts:
        # avoid making additional API calls where possible
        article_url = post.get('url');
        print(
            f"Title: {post.get('title')}, URL: {article_url}, Time: {post.get('time')}")
        if (article_url is not None):
            if is_paywalled(article_url):
                print(f"The URL '{article_url}' is likely behind a paywall.")
            else:
                print(
                    f"The URL '{article_url}' does not match known paywalled sites.")
        print()
