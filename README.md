# Twiscope

Twiscope is a lightweight Python bot that collects the latest cybersecurity news from multiple RSS feeds and sends them directly to a Telegram channel. Ideal for security professionals and enthusiasts who want automated, real-time updates.

---

## 🚀 Features
- Pulls news from multiple configurable RSS feeds
- Detects and avoids duplicate posts
- Prioritizes important news using a keyword scoring system
- Sends messages to Telegram with delay to reduce spam
- **Cloud-ready:** Stores sent news state in Azure Blob Storage for reliability and persistence

---

## ⚙️ Requirements
- Python 3.8+
- A Telegram bot (created via [BotFather](https://t.me/BotFather))
- A Telegram channel where your bot is added as an admin
- An Azure Storage Account and Blob Container (for persistent state)

---

## 🧩 Installation

```bash
# Clone the project
git clone https://github.com/yourname/twiscope.git
cd twiscope

# Install dependencies
pip install -r requirements.txt
```

---

## 📄 Setup

1. **Set environment variables** (in your environment or cloud platform):
   - `TELEGRAM_TOKEN=your_bot_token_here`
   - `TELEGRAM_CHAT_ID=your_channel_chat_id_here`
   - `AZURE_STORAGE_CONNECTION_STRING=your_azure_blob_connection_string`

2. **Add your RSS sources** in `feeds.txt` (one URL per line):
```
https://www.bleepingcomputer.com/feed/
https://threatpost.com/feed/
```

3. **Run the main script**:
```bash
python main.py
```

---

## ☁️ Cloud Usage & Azure Deployment
- The bot stores and loads the `seen_links.json` file from Azure Blob Storage instead of the local file system.
- This ensures persistent state even when running on Azure App Service or other cloud platforms.
- You must create a Storage Account and a container (e.g., `seenlinks`) and set the connection string as an environment variable.
- For Azure App Service, set the startup command to `python main.py` and add all environment variables in the portal.

---

## 🧠 Notes
- `.env`, `feeds.txt`, and local `seen_links.json` are excluded from Git via `.gitignore`.
- Messages are spaced 30 seconds apart to avoid spam filtering.
- Scores are based on simple keyword heuristics in title/summary.
- For local development, you can still use a local `seen_links.json` by adjusting the code.

---

## 📦 Versioning
- Use git tags and Github releases to track stable versions (e.g., `v1.0.0`).

---

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📬 License
MIT License. Feel free to fork and contribute!

---

For future plans including Twitter integration, image generation, or mobile app support, stay tuned.

> Made with ❤️ by [nullom]
