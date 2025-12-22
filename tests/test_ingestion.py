import pytest
from music_of_the_day.ingestion.fetch_news import fetch_news
import types

def test_fetch_news_rss(monkeypatch):
    # --- Step 1: mock config ---
    dummy_config = {
        "news_api": {"api_key": None, "query": "world", "limit": 1},
        "rss_feeds": ["http://dummy.feed/"]
    }
    monkeypatch.setattr("music_of_the_day.ingestion.fetch_news.load_config", lambda: dummy_config)

    # --- Step 2: mock feedparser.parse ---
    class DummyEntry:
        title = "Test title"
        summary = "Test summary"

    class DummyFeed:
        entries = [DummyEntry()]

    import feedparser
    monkeypatch.setattr(feedparser, "parse", lambda url: DummyFeed())

    # --- Step 3: call fetch_news ---
    articles = fetch_news(api_key=None, limit=1)

    # --- Step 4: assertions ---
    assert len(articles) == 1
    assert "Test title" in articles[0]
    assert "Test summary" in articles[0]
