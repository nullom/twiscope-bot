# RSS feed collector for Twiscope
import feedparser
import os
import logging
from typing import List, Dict, Any, Optional, Callable
from urllib.parse import urlparse
import requests
import time

FEEDS_FILE = "feeds.txt"
REQUEST_TIMEOUT = 30
RETRY_DELAY = 5
MAX_RETRIES = 3

logger = logging.getLogger(__name__)

def safe_request_operation(operation: Callable, url: str, attempt: int) -> Optional[Any]:
    """Execute request operation with unified error handling."""
    try:
        return operation()
    except requests.Timeout:
        logger.warning(f"Timeout on attempt {attempt}/{MAX_RETRIES} for {url}")
        return None
    except requests.RequestException as e:
        logger.error(f"Request failed on attempt {attempt}/{MAX_RETRIES} for {url}: {str(e)}")
        return None
    except Exception as e:
        logger.critical(f"Unexpected error on attempt {attempt}/{MAX_RETRIES} for {url}: {str(e)}")
        return None

def is_valid_url(url: str) -> bool:
    """Return True if the string is a valid URL."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def read_feed_file() -> List[str]:
    """Read lines from feeds file."""
    if not os.path.exists(FEEDS_FILE):
        logger.error(f"Feed configuration file '{FEEDS_FILE}' not found")
        return []
    try:
        with open(FEEDS_FILE, "r", encoding="utf-8") as file:
            return file.readlines()
    except Exception as e:
        logger.error(f"Error reading feed URLs: {str(e)}")
        return []

def validate_and_filter_urls(lines: List[str]) -> List[str]:
    """Validate and filter URLs from file lines."""
    urls = []
    for line in lines:
        url = line.strip()
        if url and not url.startswith("#"):
            if is_valid_url(url):
                urls.append(url)
            else:
                logger.warning(f"Invalid URL in {FEEDS_FILE}: {url}")
    return urls

def load_feed_urls() -> List[str]:
    """Read and validate RSS feed URLs from file."""
    lines = read_feed_file()
    urls = validate_and_filter_urls(lines)
    logger.debug(f"Loaded {len(urls)} feed URLs from configuration")
    return urls

def create_entry_item(entry, source_url: str) -> Dict[str, Any]:
    """Create standardized entry item from feedparser entry."""
    return {
        "title": entry.get("title", "No Title"),
        "link": entry.get("link", ""),
        "published": entry.get("published", ""),
        "summary": entry.get("summary", ""),
        "source_url": source_url
    }

def parse_feed_content(response_content: bytes, url: str) -> List[Dict[str, Any]]:
    """Parse feed content and extract entries."""
    feed = feedparser.parse(response_content)
    if feed.bozo and feed.bozo_exception:
        logger.error(f"Feed parsing error for {url}: {feed.bozo_exception}")
        return []
    entries = []
    for entry in feed.entries:
        entries.append(create_entry_item(entry, url))
    return entries

def handle_request_attempt(url: str, attempt: int) -> Optional[List[Dict[str, Any]]]:
    """Handle a single request attempt with error handling."""
    def request_operation():
        logger.info(f"Fetching feed: {url}")
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        entries = parse_feed_content(response.content, url)
        logger.debug(f"Successfully fetched {len(entries)} entries from {url}")
        return entries
    
    return safe_request_operation(request_operation, url, attempt)

def fetch_feed_with_retries(url: str) -> List[Dict[str, Any]]:
    """Fetch feed with retry mechanism."""
    for attempt in range(1, MAX_RETRIES + 1):
        entries = handle_request_attempt(url, attempt)
        if entries is not None:
            return entries
        if attempt < MAX_RETRIES:
            time.sleep(RETRY_DELAY)
    return []

def fetch_feed(url: str) -> List[Dict[str, Any]]:
    """Fetch and parse a single RSS feed with retries."""
    return fetch_feed_with_retries(url)

def fetch_rss_entries() -> List[Dict[str, Any]]:
    """Fetch and parse all configured RSS feeds."""
    all_entries = []
    urls = load_feed_urls()
    for url in urls:
        entries = fetch_feed(url)
        all_entries.extend(entries)
    logger.info(f"Total entries fetched from all feeds: {len(all_entries)}")
    return all_entries
