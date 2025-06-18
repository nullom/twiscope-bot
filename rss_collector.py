# twiscope/rss_collector.py
# Fetches and parses entries from configured RSS feeds

import feedparser
import os

FEEDS_FILE = "feeds.txt"

def load_feed_urls():
    """Reads RSS feed URLs from a text file, ignoring comments and empty lines."""
    if not os.path.exists(FEEDS_FILE):
        print(f"[!] Feed file '{FEEDS_FILE}' not found.")
        return []

    with open(FEEDS_FILE, "r", encoding="utf-8") as file:
        lines = file.readlines()

    urls = [line.strip() for line in lines if line.strip() and not line.strip().startswith("#")]
    return urls

def fetch_rss_entries():
    """Parses all feeds and returns a flat list of entries."""
    entries = []
    urls = load_feed_urls()

    for url in urls:
        print(f"[*] Fetching feed: {url}")
        feed = feedparser.parse(url)

        if feed.bozo:
            print(f"[!] Failed to parse feed: {url}")
            continue

        for entry in feed.entries:
            item = {
                "title": entry.get("title", "No Title"),
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
                "summary": entry.get("summary", "")
            }
            entries.append(item)

    print(f"[+] Total entries fetched: {len(entries)}")
    return entries
