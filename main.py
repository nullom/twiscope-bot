# Main entry point for Twiscope bot
import time
import os
import logging
from logging.handlers import RotatingFileHandler
import signal
import json
from typing import Any, Callable, Optional
from dotenv import load_dotenv
from rss_collector import fetch_rss_entries
from priority_scoring import score_entries
from tg_sender import send_news_to_telegram

load_dotenv()

# Configuration
SEEN_LINKS_FILE = "data/seen_links.json"
LOGS_DIR = "logs"
CHECK_INTERVAL = 300
MESSAGE_DELAY = 30
MAX_LOG_SIZE = 5 * 1024 * 1024
LOG_BACKUP_COUNT = 3

running = True

def safe_execute(operation: Callable, error_message: str, default_return=None, log_level=logging.ERROR) -> Any:
    """Execute operation safely with error handling."""
    try:
        return operation()
    except Exception as e:
        logging.log(log_level, f"{error_message}: {e}")
        return default_return

def safe_file_operation(file_path: str, operation: str, data=None, encoding='utf-8') -> Any:
    """Perform file operations with unified error handling."""
    def read_operation():
        with open(file_path, 'r', encoding=encoding) as f:
            return json.load(f)
    
    def write_operation():
        with open(file_path, 'w', encoding=encoding) as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    
    operations = {
        'read': read_operation,
        'write': write_operation
    }
    
    if operation not in operations:
        raise ValueError(f"Unsupported operation: {operation}")
    
    return safe_execute(
        operations[operation],
        f"Error during {operation} operation on {file_path}",
        default_return=[] if operation == 'read' else False
    )

def setup_logging():
    """Setup logging configuration with file and console handlers."""
    os.makedirs(LOGS_DIR, exist_ok=True)
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
    return logger

def setup_directories():
    """Create necessary directories for data and logs."""
    directories = [LOGS_DIR, os.path.dirname(SEEN_LINKS_FILE)]
    for directory in directories:
        safe_execute(lambda: os.makedirs(directory, exist_ok=True), f"Error creating directory {directory}")

def setup_signal_handlers():
    """Setup signal handlers for graceful shutdown."""
    def signal_handler(signum, frame):
        global running
        logging.info("Shutdown signal received. Cleaning up...")
        running = False
    
    for sig in [signal.SIGINT, signal.SIGTERM]:
        signal.signal(sig, signal_handler)

def load_seen_links():
    """Load processed links from JSON file."""
    if not os.path.exists(SEEN_LINKS_FILE):
        return []
    
    data = safe_file_operation(SEEN_LINKS_FILE, 'read')
    if data is None:
        # Handle JSON decode error specifically
        try:
            with open(SEEN_LINKS_FILE, 'r', encoding='utf-8') as f:
                json.load(f)
        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error in seen_links: {e}")
        return []
    return data

def save_seen_links(links):
    """Save processed links to JSON file."""
    safe_file_operation(SEEN_LINKS_FILE, 'write', data=links)

def format_message(entry):
    """Format entry for Telegram message."""
    return f"\u2728 <b>{entry['title']}</b>\n{entry['link']}"

def process_entry(entry, seen_links):
    """Process and send a single entry."""
    def send_operation():
        message = format_message(entry)
        result = send_news_to_telegram(message)
        if result:
            logging.info(f"Sent: {entry['title']}")
            seen_links.append(entry['link'])
            save_seen_links(seen_links)
            time.sleep(MESSAGE_DELAY)
        return result
    
    return safe_execute(
        send_operation,
        f"Error sending entry {entry['title']}",
        default_return=False
    )

def run():
    """Fetch, score, filter, and send new RSS entries."""
    logger = logging.getLogger()
    
    def run_operation():
        logger.info("Checking for new RSS entries...")
        entries = fetch_rss_entries()
        scored_entries = score_entries(entries)
        seen_links = load_seen_links()
        new_entries = [e for e in scored_entries if e['link'] not in seen_links]
        
        if not new_entries:
            logger.debug("No new entries found.")
            return
        
        for entry in new_entries:
            if not running:
                break
            process_entry(entry, seen_links)
    
    safe_execute(
        run_operation,
        "Unhandled exception in run",
        log_level=logging.CRITICAL
    )
    time.sleep(60)  # Always wait on error

def wait_with_shutdown_check(seconds):
    """Wait for specified seconds while checking for shutdown signal."""
    for _ in range(seconds):
        if not running:
            break
        time.sleep(1)

def main():
    """Main loop."""
    setup_directories()
    logger = setup_logging()
    setup_signal_handlers()
    logger.info("Twiscope bot starting...")
    
    while running:
        def main_loop_operation():
            run()
            wait_with_shutdown_check(CHECK_INTERVAL)
        
        try:
            main_loop_operation()
        except KeyboardInterrupt:
            break
        except Exception as e:
            logger.critical(f"Critical error in main loop: {e}")
            time.sleep(60)
    
    logger.info("Twiscope bot shutting down...")

if __name__ == "__main__":
    main()
