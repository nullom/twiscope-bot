# twiscope/main.py
# Main entry point for the Twiscope bot - RSS feed collector and Telegram news sender

import time
from rss_collector import fetch_rss_entries
from priority_scoring import score_entries
from tg_sender import send_news_to_telegram
import json
import os
import logging
from logging.handlers import RotatingFileHandler
import signal
import sys

# Configuration
SEEN_LINKS_FILE = "data/seen_links.json"
LOGS_DIR = "logs"
CHECK_INTERVAL = 300  # 5 minutes (in seconds)
MESSAGE_DELAY = 30    # delay between messages (in seconds)
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB
LOG_BACKUP_COUNT = 3

# Create log and data directories
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(os.path.dirname(SEEN_LINKS_FILE), exist_ok=True)

# Logging configuration
log_formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
log_file = os.path.join(LOGS_DIR, 'twiscope.log')
log_handler = RotatingFileHandler(log_file, maxBytes=MAX_LOG_SIZE, backupCount=LOG_BACKUP_COUNT)
log_handler.setFormatter(log_formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)
logger.addHandler(console_handler)

# For graceful shutdown
running = True

def signal_handler(signum, frame):
    """Handle shutdown signals (SIGTERM, SIGINT)"""
    global running
    logging.info("Shutdown signal received. Cleaning up...")
    running = False

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def load_seen_links():
    """Load the list of already processed links from the JSON file"""
    try:
        if os.path.exists(SEEN_LINKS_FILE):
            with open(SEEN_LINKS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logging.error(f"Error loading seen_links: {e}")
    return []

def save_seen_links(links):
    """Save the updated list of processed links to the JSON file"""
    try:
        with open(SEEN_LINKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(links, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logging.error(f"Error saving seen_links: {e}")

def run():
    """Execute a single iteration of RSS feed checking and news sending"""
    logging.info("Twiscope checking for new entries...")
    try:
        # Fetch and score new entries
        entries = fetch_rss_entries()
        scored_entries = score_entries(entries)

        # Filter out already seen entries
        seen_links = load_seen_links()
        new_entries = [e for e in scored_entries if e['link'] not in seen_links]

        if not new_entries:
            logging.info("No new entries found.")
            return

        # Process and send new entries
        for entry in new_entries:
            if not running:  # Check for shutdown signal
                break
                
            try:
                message = f"\u2728 <b>{entry['title']}</b>\n{entry['link']}"
                send_news_to_telegram(message)
                logging.info(f"Sent: {entry['title']}")
                seen_links.append(entry['link'])
                save_seen_links(seen_links)
                time.sleep(MESSAGE_DELAY)
            except Exception as e:
                logging.error(f"Error sending entry {entry['title']}: {e}")
                continue

    except Exception as e:
        logging.error(f"Unhandled exception in run: {e}")
        time.sleep(60)  # Wait 1 minute on error before retry

def main():
    """Main loop - runs continuously until shutdown signal is received"""
    logging.info("Twiscope bot starting...")
    
    while running:
        try:
            run()
            # Wait for CHECK_INTERVAL seconds, checking for shutdown signal every second
            for _ in range(CHECK_INTERVAL):
                if not running:
                    break
                time.sleep(1)
        except KeyboardInterrupt:
            break
        except Exception as e:
            logging.error(f"Critical error in main loop: {e}")
            time.sleep(60)  # Wait 1 minute on critical error

    logging.info("Twiscope bot shutting down...")

if __name__ == "__main__":
    main()
