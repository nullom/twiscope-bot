# twiscope/rss_collector.py
# Fetches and parses entries from configured RSS feeds

import feedparser
import os
import logging
from typing import List, Dict, Any
from urllib.parse import urlparse
import requests
from requests.exceptions import RequestException
import time

# Configuration
FEEDS_FILE = "feeds.txt"
REQUEST_TIMEOUT = 30  # seconds
RETRY_DELAY = 5      # seconds
MAX_RETRIES = 3

# Configure module logger
logger = logging.getLogger(__name__)

def is_valid_url(url: str) -> bool:
    """
    Validate if the given string is a proper URL.
    
    Args:
        url (str): URL to validate
        
    Returns:
        bool: True if URL is valid, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def load_feed_urls() -> List[str]:
    """
    Read RSS feed URLs from the configuration file.
    
    Returns:
        List[str]: List of valid RSS feed URLs
        
    Note:
        - Ignores empty lines and comments (lines starting with #)
        - Validates URLs before returning
    """
    if not os.path.exists(FEEDS_FILE):
        logger.error(f"Feed configuration file '{FEEDS_FILE}' not found")
        return []

    try:
        with open(FEEDS_FILE, "r", encoding="utf-8") as file:
            lines = file.readlines()

        urls = []
        for line in lines:
            url = line.strip()
            if url and not url.startswith("#"):
                if is_valid_url(url):
                    urls.append(url)
                else:
                    logger.warning(f"Invalid URL found in {FEEDS_FILE}: {url}")
                    
        logger.info(f"Loaded {len(urls)} feed URLs from configuration")
        return urls
        
    except Exception as e:
        logger.error(f"Error reading feed URLs: {str(e)}")
        return []

def fetch_feed(url: str) -> List[Dict[str, Any]]:
    """
    Fetch and parse a single RSS feed with retry mechanism.
    
    Args:
        url (str): The RSS feed URL to fetch
        
    Returns:
        List[Dict[str, Any]]: List of parsed entries from the feed
    """
    entries = []
    retries = 0
    
    while retries < MAX_RETRIES:
        try:
            logger.info(f"Fetching feed: {url}")
            feed = feedparser.parse(url, timeout=REQUEST_TIMEOUT)

            if feed.bozo:
                logger.error(f"Feed parsing error for {url}: {feed.bozo_exception}")
                break

            for entry in feed.entries:
                item = {
                    "title": entry.get("title", "No Title"),
                    "link": entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "summary": entry.get("summary", ""),
                    "source_url": url
                }
                entries.append(item)

            logger.info(f"Successfully fetched {len(entries)} entries from {url}")
            break
            
        except Exception as e:
            retries += 1
            logger.warning(f"Attempt {retries}/{MAX_RETRIES} failed for {url}: {str(e)}")
            if retries < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
                
    return entries

def fetch_rss_entries() -> List[Dict[str, Any]]:
    """
    Fetch and parse all configured RSS feeds.
    
    Returns:
        List[Dict[str, Any]]: Combined list of entries from all feeds
        
    Note:
        Each entry contains:
        - title: Article title
        - link: Article URL
        - published: Publication date
        - summary: Article summary
        - source_url: Original RSS feed URL
    """
    all_entries = []
    urls = load_feed_urls()

    for url in urls:
        entries = fetch_feed(url)
        all_entries.extend(entries)

    logger.info(f"Total entries fetched from all feeds: {len(all_entries)}")
    return all_entries
