# twiscope/main.py
# Main entry point for the Twiscope bot

import time
from rss_collector import fetch_rss_entries
from priority_scoring import score_entries
from tg_sender import send_news_to_telegram
import json
import os
from datetime import datetime
import logging

SEEN_LINKS_FILE = "seen_links.json"

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Load already sent links
def load_seen_links():
    try:
        if os.path.exists(SEEN_LINKS_FILE):
            with open(SEEN_LINKS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        logging.error(f"Error loading seen links: {e}")
    return []

# Save updated seen links
def save_seen_links(links):
    try:
        with open(SEEN_LINKS_FILE, "w", encoding="utf-8") as f:
            json.dump(links, f, indent=2)
    except Exception as e:
        logging.error(f"Error saving seen links: {e}")

# Main job (single run)
def run():
    logging.info("Twiscope checking for new entries...")
    try:
        entries = fetch_rss_entries()
        scored_entries = score_entries(entries)

        seen_links = load_seen_links()
        new_entries = [e for e in scored_entries if e['link'] not in seen_links]

        if not new_entries:
            logging.info("No new entries found.")
            return

        for entry in new_entries:
            message = f"\u2728 <b>{entry['title']}</b>\n{entry['link']}"
            send_news_to_telegram(message)
            logging.info(f"Sent: {entry['title']}")
            seen_links.append(entry['link'])
            save_seen_links(seen_links)
            time.sleep(30)  # delay between messages to avoid spamming
    except Exception as e:
        logging.error(f"Unhandled exception in run: {e}")

if __name__ == "__main__":
    run()
