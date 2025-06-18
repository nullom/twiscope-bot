# twiscope/main.py
# Main entry point for the Twiscope bot

import time
from rss_collector import fetch_rss_entries
from priority_scoring import score_entries
from tg_sender import send_news_to_telegram
from azure.storage.blob import BlobServiceClient
import json
import os
import logging

SEEN_LINKS_CONTAINER = "seenlinks"  # Azure Blob Storage container adı
SEEN_LINKS_BLOB = "seen_links.json" # Blob adı

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def get_blob_service_client():
    conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if not conn_str:
        logging.error("AZURE_STORAGE_CONNECTION_STRING ortam değişkeni bulunamadı!")
        raise Exception("Azure Storage bağlantı dizesi eksik.")
    return BlobServiceClient.from_connection_string(conn_str)

# Load already sent links
def load_seen_links():
    try:
        blob_service_client = get_blob_service_client()
        container_client = blob_service_client.get_container_client(SEEN_LINKS_CONTAINER)
        blob_client = container_client.get_blob_client(SEEN_LINKS_BLOB)
        if blob_client.exists():
            data = blob_client.download_blob().readall()
            return json.loads(data.decode("utf-8"))
    except Exception as e:
        logging.error(f"Azure Blob'dan seen_links yüklenemedi: {e}")
    return []

# Save updated seen links
def save_seen_links(links):
    try:
        blob_service_client = get_blob_service_client()
        container_client = blob_service_client.get_container_client(SEEN_LINKS_CONTAINER)
        # Container yoksa oluştur
        try:
            container_client.create_container()
        except Exception:
            pass  # Zaten varsa hata verme
        blob_client = container_client.get_blob_client(SEEN_LINKS_BLOB)
        blob_client.upload_blob(json.dumps(links, indent=2), overwrite=True)
    except Exception as e:
        logging.error(f"Azure Blob'a seen_links kaydedilemedi: {e}")

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
