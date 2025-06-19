# Twiscope

**An intelligent cybersecurity news aggregator that delivers critical security updates directly to your Telegram.**

Twiscope continuously monitors trusted RSS feeds and uses smart priority scoring to ensure you receive the most important security news first - from zero-day vulnerabilities to major breaches.

---

## ✨ Features

- **Smart Monitoring**: Tracks multiple RSS feeds with duplicate detection
- **Priority Scoring**: Keywords-based system prioritizes critical security news
- **Telegram Integration**: Real-time delivery with rate limiting
- **24/7 Operation**: Robust error handling and automatic recovery
- **Easy Deployment**: Cloud-ready with simple configuration
- **Comprehensive Logging**: Rotating logs with configurable levels

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Telegram bot token ([Create one](https://t.me/BotFather))
- Telegram chat/channel ID

### Installation
```bash
git clone https://github.com/nullom/twiscope-bot.git
cd twiscope-bot
pip install -r requirements.txt
```

### Configuration
1. **Environment Variables** (create `.env` file):
   ```env
   TELEGRAM_TOKEN=your_bot_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here
   ```

2. **RSS Feeds** (edit `feeds.txt`):
   ```
   https://www.bleepingcomputer.com/feed/
   https://threatpost.com/feed/
   ```

3. **Run**:
   ```bash
   python main.py
   ```

---

## ☁️ Cloud Deployment

### Oracle Cloud (Recommended)

**1. Create VM Instance**
- OS: Ubuntu 22.04+
- Shape: VM.Standard.E2.1.Micro (free tier)
- Enable public IP and SSH access

**2. Automated Setup** (paste in cloud-init):
```yaml
#cloud-config
package_update: true
packages: [python3-pip, supervisor]

write_files:
  - path: /opt/twiscope/.env
    content: |
      TELEGRAM_TOKEN=YOUR_BOT_TOKEN
      TELEGRAM_CHAT_ID=YOUR_CHAT_ID
    permissions: '0600'
  
  - path: /opt/twiscope/feeds.txt
    content: |
      https://www.bleepingcomputer.com/feed/
      https://threatpost.com/feed/
  
  - path: /etc/supervisor/conf.d/twiscope.conf
    content: |
      [program:twiscope]
      directory=/opt/twiscope
      command=python3 main.py
      user=ubuntu
      autostart=true
      autorestart=true
      stderr_logfile=/var/log/supervisor/twiscope.err.log

runcmd:
  - git clone https://github.com/nullom/twiscope-bot.git /opt/twiscope
  - chown -R ubuntu:ubuntu /opt/twiscope
  - cd /opt/twiscope && pip3 install -r requirements.txt
  - systemctl enable --now supervisor
```

**3. Monitor**
```bash
# Check status
sudo supervisorctl status

# View logs
tail -f /opt/twiscope/logs/twiscope.log
tail -f /var/log/supervisor/twiscope.err.log
```

### Other Cloud Providers
- **AWS**: Use EC2 with the same cloud-init script
- **DigitalOcean**: Create droplet with Ubuntu and run setup manually
- **Azure**: Use VM with custom data for automated setup

---

## 🔧 Configuration

### Environment Variables
| Variable | Description | Required |
|----------|-------------|----------|
| `TELEGRAM_TOKEN` | Bot token from BotFather | ✅ |
| `TELEGRAM_CHAT_ID` | Target chat/channel ID | ✅ |

### RSS Feeds (`feeds.txt`)
- One URL per line
- Comments start with `#`
- Invalid URLs are automatically skipped

### Scoring System
Priority keywords (higher score = higher priority):
- `0-day`: 10 points
- `exploit`: 9 points  
- `breach`: 8 points
- `ransomware`: 7 points
- `critical`: 6 points
- Title keywords get 2x weight

---

## 📊 Monitoring & Logs

### Log Locations
- **Application**: `logs/twiscope.log`
- **Supervisor**: `/var/log/supervisor/twiscope.*.log`

### Log Levels
- **INFO**: Normal operations, sent messages
- **WARNING**: Network timeouts, invalid URLs
- **ERROR**: API errors, file issues
- **CRITICAL**: System failures

### Commands
```bash
# Restart bot
sudo supervisorctl restart twiscope

# Check logs in real-time
tail -f logs/twiscope.log

# View recent errors
grep ERROR logs/twiscope.log | tail -20
```

---

## 🛠️ Development

### Project Structure
```
twiscope-bot/
├── main.py              # Entry point and orchestration
├── rss_collector.py     # RSS feed processing
├── priority_scoring.py  # News scoring algorithm
├── tg_sender.py         # Telegram API integration
├── requirements.txt     # Dependencies
├── feeds.txt           # RSS feed URLs
├── .env                # Environment variables (create)
├── data/               # Runtime data (auto-created)
└── logs/               # Application logs (auto-created)
```

### Adding Features
- **New scoring rules**: Edit `priority_scoring.py`
- **Additional feeds**: Add to `feeds.txt`
- **Custom formatting**: Modify `format_message()` in `main.py`

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📜 License

MIT License - see LICENSE file for details.

---

## 🆔 Version

**v2.0.2** - Production Ready
- Cloud deployment optimized
- Enhanced error handling
- Modular architecture
- Comprehensive documentation

---

*Built with ❤️ for the cybersecurity community*
