# twiscope/telegram_sender.py
# Sends formatted messages to Telegram via bot

import requests
import os
import logging

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

logger = logging.getLogger("tg_sender")

def send_news_to_telegram(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        logger.error("Telegram credentials not set in environment variables.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }

    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            logger.error(f"Telegram error: {response.text}")
        else:
            logger.info("Message sent successfully.")
    except Exception as e:
        logger.error(f"Telegram exception: {str(e)}")
