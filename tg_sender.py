# twiscope/telegram_sender.py
# Handles sending formatted messages to Telegram through the bot API

import requests
import os
import logging
from typing import Optional

# Environment variables for Telegram configuration
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Configure module logger
logger = logging.getLogger(__name__)

def send_news_to_telegram(message: str) -> Optional[bool]:
    """
    Send a formatted message to Telegram using the bot API.
    
    Args:
        message (str): The message to send, can contain HTML formatting
        
    Returns:
        Optional[bool]: True if message was sent successfully, False on error, None if credentials missing
        
    Raises:
        requests.RequestException: If there's a network or API error
    """
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        logger.error("Telegram credentials (TELEGRAM_TOKEN or TELEGRAM_CHAT_ID) not set in environment variables")
        return None

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }

    try:
        response = requests.post(url, data=payload, timeout=30)
        response.raise_for_status()  # Raise exception for non-200 status codes
        
        logger.info("Message sent successfully")
        return True
        
    except requests.exceptions.Timeout:
        logger.error("Telegram API request timed out")
        return False
        
    except requests.exceptions.HTTPError as e:
        logger.error(f"Telegram API error: {response.text}")
        return False
        
    except Exception as e:
        logger.error(f"Unexpected error sending message: {str(e)}")
        return False
