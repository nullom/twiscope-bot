# Telegram message sender for Twiscope

import requests
import os
import logging
from typing import Optional, Tuple, Callable

logger = logging.getLogger(__name__)

def safe_telegram_request(operation: Callable, error_context: str) -> Optional[bool]:
    """Execute Telegram API request with unified error handling."""
    try:
        return operation()
    except requests.exceptions.Timeout:
        logger.warning(f"Telegram API request timed out - {error_context}")
        return False
    except requests.exceptions.HTTPError as e:
        logger.error(f"Telegram API error - {error_context}: {e}")
        return False
    except Exception as e:
        logger.critical(f"Unexpected error - {error_context}: {str(e)}")
        return False

def get_telegram_credentials() -> Tuple[Optional[str], Optional[str]]:
    """Get Telegram credentials from environment variables."""
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    logger.debug(f"[SENDER] TELEGRAM_TOKEN exists: {'Yes' if token else 'No'}")
    logger.debug(f"[SENDER] TELEGRAM_CHAT_ID exists: {'Yes' if chat_id else 'No'}")
    return token, chat_id

def validate_credentials(token: Optional[str], chat_id: Optional[str]) -> bool:
    """Validate that required credentials are present."""
    if not token or not chat_id:
        logger.error("Telegram credentials (TELEGRAM_TOKEN or TELEGRAM_CHAT_ID) not set in environment variables")
        return False
    return True

def create_telegram_payload(chat_id: str, message: str) -> dict:
    """Create payload for Telegram API request."""
    return {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }

def execute_telegram_request(url: str, payload: dict) -> bool:
    """Execute the actual Telegram API request."""
    def request_operation():
        response = requests.post(url, data=payload, timeout=30)
        response.raise_for_status()
        logger.info("Message sent successfully")
        return True
    
    return safe_telegram_request(request_operation, "sending message")

def send_news_to_telegram(message: str) -> Optional[bool]:
    """Send a message to Telegram chat."""
    token, chat_id = get_telegram_credentials()
    if not validate_credentials(token, chat_id):
        return None
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = create_telegram_payload(chat_id, message)
    
    return execute_telegram_request(url, payload)
