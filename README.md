# Twiscope

Twiscope is an intelligent cybersecurity news aggregator that brings critical security updates directly to your Telegram channel. By continuously monitoring multiple trusted RSS feeds, it ensures security professionals stay informed about emerging threats, vulnerabilities, and industry developments in real-time.

Using a sophisticated priority scoring system, Twiscope evaluates the significance of each security update based on carefully selected keywords and context. This ensures that high-priority news about zero-day vulnerabilities, active exploits, or major security breaches reaches you first, helping you maintain a proactive security posture.

Designed for reliability and 24/7 operation, Twiscope features robust error handling, comprehensive logging, and seamless cloud deployment capabilities, making it an invaluable tool for security teams, researchers, and cybersecurity enthusiasts.

---

## 🚀 Features
- Continuous monitoring of multiple configurable RSS feeds
- Smart duplicate detection and prevention
- Priority-based news scoring system using security keywords
- Rate-limited Telegram messaging to prevent spam
- Robust error handling and automatic recovery
- Comprehensive logging with rotation
- Graceful shutdown support
- Designed for 24/7 operation

---

## ⚙️ Requirements
- Python 3.8+
- A Telegram bot (created via [BotFather](https://t.me/BotFather))
- A Telegram channel where your bot is added as an admin
- Linux-based hosting environment (e.g., Oracle Cloud VM, AWS EC2, etc.)

---

## 🧩 Installation

```bash
# Clone the project
git clone https://github.com/nullom/twiscope-bot.git
cd twiscope-bot

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## 📄 Setup

1. **Set environment variables** (in your environment or .env file):
   - `TELEGRAM_TOKEN=your_bot_token_here`
   - `TELEGRAM_CHAT_ID=your_channel_chat_id_here`

2. **Add your RSS sources** in `feeds.txt` (one URL per line):
```
https://www.bleepingcomputer.com/feed/
https://threatpost.com/feed/
```

3. **Directory Structure**:
```
twiscope/
├── logs/          # Log files with rotation
├── data/          # Persistent data storage
└── feeds.txt      # RSS feed configuration
```

4. **Run the bot**:
```bash
python main.py
```

---

## ☁️ Cloud Deployment (Oracle Cloud)

1. **Create an Oracle Cloud VM Instance**:
   - Use Ubuntu 22.04 or later
   - Enable public IP
   - Configure security list for SSH access

2. **Use cloud-init for Automated Setup**:
   ```yaml
   #cloud-config
   package_update: true
   package_upgrade: true
   
   packages:
     - python3-pip
     - supervisor
   
   write_files:
     - path: /etc/supervisor/conf.d/twiscope.conf
       content: |
         [program:twiscope]
         directory=/opt/twiscope
         command=python3 main.py
         user=ubuntu
         autostart=true
         autorestart=true
         stderr_logfile=/var/log/supervisor/twiscope.err.log
         stdout_logfile=/var/log/supervisor/twiscope.out.log
   
   runcmd:
     - mkdir -p /opt/twiscope
     - git clone https://github.com/nullom/twiscope-bot.git /opt/twiscope
     - chown -R ubuntu:ubuntu /opt/twiscope
     - cd /opt/twiscope
     - pip3 install -r requirements.txt
     - systemctl enable supervisor
     - systemctl start supervisor
   ```

3. **Monitor the Bot**:
   - Check Supervisor status: `sudo supervisorctl status`
   - View logs: 
     - Application logs: `/opt/twiscope/logs/twiscope.log`
     - Supervisor logs: `/var/log/supervisor/twiscope.*.log`

---

## 🧠 Notes
- All configuration files (`.env`, `feeds.txt`) are excluded from Git
- Messages are spaced 30 seconds apart to avoid spam filtering
- News priority scoring is based on security-related keyword weights
- Automatic log rotation keeps disk usage under control
- Graceful shutdown ensures no messages are lost

---

## 📦 Versioning
Current version: v2.0.2
- v2.0.0: Major update with cloud deployment support
- v2.0.1: Code quality improvements and documentation updates
- v2.0.2: Enhanced project description and repository URL updates

---

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📬 License
MIT License. Feel free to fork and contribute!

---

## 🔮 Future Plans
- Sentiment analysis for threat intelligence
- Customizable scoring rules via configuration
- Web dashboard for monitoring and configuration
- Integration with additional news sources
- AI-powered relevance scoring
- Custom notification rules and filters

> Made with ❤️ by [nullom]
