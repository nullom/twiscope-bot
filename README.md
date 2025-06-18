# Twiscope

Twiscope is a lightweight Python bot that collects the latest cybersecurity news from multiple RSS feeds and sends them directly to a Telegram channel. Ideal for security professionals and enthusiasts who want automated, real-time updates.

---

## 🚀 Features
- Pulls news from multiple configurable RSS feeds
- Detects and avoids duplicate posts
- Prioritizes important news using a keyword scoring system
- Sends messages to Telegram with delay to reduce spam

---

## ⚙️ Requirements
- Python 3.8+
- A Telegram bot (created via [BotFather](https://t.me/BotFather))
- A Telegram channel where your bot is added as an admin

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

1. **Create a `.env` file**:
```env
TELEGRAM_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_channel_chat_id_here
```

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

## 🧠 Notes
- `.env`, `feeds.txt`, and `seen_links.json` are excluded from Git via `.gitignore`.
- Messages are spaced 30 seconds apart to avoid spam filtering.
- Scores are based on simple keyword heuristics in title/summary.

---

## 📬 License
MIT License. Feel free to fork and contribute!

---

For future plans including Twitter integration, image generation, or mobile app support, stay tuned.

> Made with ❤️ by [nullom]
