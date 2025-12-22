import os
import requests
import feedparser
import yaml
from pathlib import Path

CONFIG_PATH = Path("configs/sources.yaml")

def load_config():
    """
    Load configuration from YAML.
    Returns a dictionary with news_api and rss_feeds.
    """
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def fetch_news(api_key: str = None, query: str = "world", limit: int = 7):
    """
    Fetches recent news articles.
    - Uses NewsAPI if api_key is provided
    - Falls back to RSS feeds from configs if NewsAPI fails or api_key is missing
    Returns a list of article texts (title + description/summary)
    """
    config = load_config()
    articles = []

    # --- Step 1: Use NewsAPI if key provided ---
    api_key = api_key or os.environ.get("NEWS_API_KEY") or config["news_api"].get("api_key")
    query = query or config["news_api"].get("query", "world")
    limit = limit or config["news_api"].get("limit", 7)

    if api_key:
        url = "https://newsapi.org/v2/top-headlines"
        params = {"apiKey": api_key, "q": query, "pageSize": limit, "language": "en"}
        try:
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            for item in data.get("articles", []):
                text = item["title"]
                if item.get("description"):
                    text += ". " + item["description"]
                articles.append(text)
        except Exception as e:
            print(f"⚠️ NewsAPI fetch failed: {e}")

    # --- Step 2: Fallback to RSS feeds if necessary ---
    if len(articles) < limit:
        rss_feeds = config.get("rss_feeds", [])
        for feed_url in rss_feeds:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:limit]:
                    text = entry.title
                    if getattr(entry, "summary", None):
                        text += ". " + entry.summary
                    articles.append(text)
                if len(articles) >= limit:
                    break
            except Exception as e:
                print(f"⚠️ RSS feed fetch failed ({feed_url}): {e}")

    return articles[:limit]
