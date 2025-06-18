# twiscope/main.py
# Main entry point for the Twiscope bot

import time
import schedule
from rss_collector import fetch_rss_entries
from priority_scoring import score_entries
from tg_sender import send_news_to_telegram
import json
import os
from datetime import datetime

SEEN_LINKS_FILE = "seen_links.json"

# Load already sent links
def load_seen_links():
    if os.path.exists(SEEN_LINKS_FILE):
        with open(SEEN_LINKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Save updated seen links
def save_seen_links(links):
    with open(SEEN_LINKS_FILE, "w", encoding="utf-8") as f:
        json.dump(links, f, indent=2)

# Main scheduled job
def run():
    print(f"[i] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Twiscope checking for new entries...")
    entries = fetch_rss_entries()
    scored_entries = score_entries(entries)

    seen_links = load_seen_links()
    new_entries = [e for e in scored_entries if e['link'] not in seen_links]

    if not new_entries:
        print("[~] No new entries found.")
        return

    for entry in new_entries:
        message = f"\u2728 <b>{entry['title']}</b>\n{entry['link']}"
        send_news_to_telegram(message)
        print(f"[+] Sent: {entry['title']}")
        seen_links.append(entry['link'])
        save_seen_links(seen_links)
        time.sleep(30)  # delay between messages to avoid spamming

# Schedule every 3 hours
schedule.every(3).hours.do(run)

# Initial run
run()

print("[i] Scheduler running. Press Ctrl+C to stop.")
while True:
    schedule.run_pending()
    time.sleep(60)
