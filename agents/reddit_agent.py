import requests
from tools.openrouter_llm import call_llm


def fetch_reddit_posts():
    print("\n[Reddit Agent] Step 1: Fetching Reddit posts...\n")

    # 🔥 Primary (Reddit)
    reddit_url = "https://www.reddit.com/search.json?q=trading+signals+problem&limit=5"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        response = requests.get(reddit_url, headers=headers)

        if response.status_code == 200:
            data = response.json()

            posts = []

            for post in data.get("data", {}).get("children", []):
                title = post["data"].get("title", "")
                text = post["data"].get("selftext", "")
                link = "https://reddit.com" + post["data"].get("permalink", "")

                posts.append({
                    "title": title,
                    "text": text,
                    "link": link
                })

            if posts:
                return posts

        print("⚠️ Reddit blocked, switching to backup...")

    except Exception as e:
        print("Reddit primary failed:", str(e))

    # 🔥 BACKUP (Pushshift)
    try:
        backup_url = "https://api.pushshift.io/reddit/search/submission/?q=trading&size=5"
        response = requests.get(backup_url)
        data = response.json()

        posts = []

        for post in data.get("data", []):
            posts.append({
                "title": post.get("title", ""),
                "text": post.get("selftext", ""),
                "link": f"https://reddit.com{post.get('permalink', '')}"
            })

        return posts

    except Exception as e:
        print("Backup Reddit fetch failed:", str(e))
        return []


def extract_pain_and_reply(posts):
    print("\n[Reddit Agent] Step 2: Extracting pain + generating replies...\n")

    results = []

    for post in posts:
        content = f"{post['title']} {post['text']}"

        prompt = f"""
You are a real Reddit user (NOT a marketer).

1. Understand the main problem in the post
2. Write a natural, human-like reply
3. Share experience or advice
4. DO NOT sound promotional
5. Keep it relatable and helpful

Post:
{content}
"""

        try:
            reply = call_llm(prompt)

            results.append({
                "post": post["title"],
                "link": post["link"],
                "reply": reply
            })

        except Exception as e:
            print("Reply generation error:", str(e))

    return results