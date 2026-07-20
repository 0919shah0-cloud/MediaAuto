# 📦 MediaAuto Installation Guide

## Quick Start (Recommended)

### Prerequisites
- Ubuntu 20.04, 22.04, or 24.04 LTS
- Minimum 2GB RAM
- 10GB free disk space
- Internet connection
- Root or sudo access

### One-Command Installation

```bash
sudo bash install.sh
```

The installer will:
1. ✅ Update system packages
2. ✅ Install all dependencies
3. ✅ Create virtual environment
4. ✅ Configure the bot interactively
5. ✅ Set up database
6. ✅ Start services

---

## Configuration Setup

During installation, you'll be asked to provide:

### 1️⃣ Telegram Bot Token
```
💡 How to get:
  1. Message @BotFather on Telegram
  2. Type /newbot
  3. Follow the instructions
  4. Copy the token provided
```

### 2️⃣ Telegram API Credentials
```
💡 How to get:
  1. Visit https://my.telegram.org/apps
  2. Log in with your Telegram account
  3. Click "Create new application"
  4. Copy API ID and API Hash
```

### 3️⃣ Your Telegram Phone Number
```
Format: +989123456789
Include country code!
```

### 4️⃣ Channels to Monitor
```
Example:
  @channel1,@channel2,@channel3
  1234567890,-1001234567890
  
Mix of usernames and numeric IDs is supported
```

### 5️⃣ Output Destination
```
Where to post content:
  @mychannel (group/channel username)
  -1001234567890 (numeric ID)
```

### 6️⃣ AI Provider Selection
```
1) OpenAI (requires API key)
2) Google Gemini (requires API key)
3) Claude/Anthropic (requires API key)
4) None (disable AI features)
```

### 7️⃣ Scheduler Interval
```
1) Every 5 minutes
2) Every 10 minutes
3) Every 30 minutes
4) Every 1 hour
5) Custom (enter minutes)
```

### 8️⃣ Watermark Settings
```
Channel/username to add to posts:
  @MyChannel
  MyBrand
```

### 9️⃣ Web Panel Configuration
```
Username: admin
Password: (secure password)
Port: 5000 (or custom)
```

### 🔟 Database Selection
```
1) SQLite (simple, no setup)
2) PostgreSQL (production-ready)

For PostgreSQL, also provide:
  - Host (localhost)
  - Port (5432)
  - Database name (mediaauto)
  - Username (mediaauto)
  - Password
```

---

## Post-Installation

### ✅ Verify Installation

```bash
# Check bot status
sudo systemctl status mediaauto

# View bot logs
journalctl -u mediaauto -f

# Check web panel
curl http://localhost:5000
```

### 🌐 Access Web Dashboard

```
URL: http://YOUR_SERVER_IP:5000
Username: admin (or your chosen username)
Password: your-password
```

### 📁 Important Directories

```
/opt/mediaauto/
├── config/settings.json         # Configuration file
├── logs/                        # Log files
├── database/                    # Database files
├── downloads/                   # Downloaded media
└── backups/                     # Backup files
```

---

## Common Commands

### System Control

```bash
# Start the bot
sudo systemctl start mediaauto

# Stop the bot
sudo systemctl stop mediaauto

# Restart the bot
sudo systemctl restart mediaauto

# Check status
sudo systemctl status mediaauto

# Enable auto-start on reboot
sudo systemctl enable mediaauto

# Disable auto-start
sudo systemctl disable mediaauto
```

### View Logs

```bash
# Real-time logs
journalctl -u mediaauto -f

# Last 50 lines
journalctl -u mediaauto -n 50

# Show logs from last hour
journalctl -u mediaauto --since "1 hour ago"

# Show error logs only
journalctl -u mediaauto -p err
```

### Configuration Management

```bash
# View configuration
cat /opt/mediaauto/config/settings.json

# Edit configuration
sudo nano /opt/mediaauto/config/settings.json

# Validate JSON
python3 -m json.tool /opt/mediaauto/config/settings.json

# Backup configuration
cp /opt/mediaauto/config/settings.json \
   /opt/mediaauto/backups/settings_backup_$(date +%Y%m%d).json
```

### Database Operations

```bash
# SQLite - open database
sqlite3 /opt/mediaauto/database/mediaauto.db

# PostgreSQL - connect
psql -h localhost -U mediaauto -d mediaauto

# Backup database
/opt/mediaauto/scripts/backup_all.sh

# PostgreSQL backup
pg_dump -h localhost -U mediaauto mediaauto > backup.sql
```

---

## Troubleshooting

### Bot not starting?

```bash
# Check system logs
sudo journalctl -u mediaauto --no-pager | tail -100

# Check configuration
json_verify /opt/mediaauto/config/settings.json

# Test with verbose output
sudo -u mediaauto python3 /opt/mediaauto/main.py --verbose
```

### Connection Issues?

```bash
# Test internet
ping 8.8.8.8

# Test Telegram API
curl https://api.telegram.org/bot<YOUR_TOKEN>/getMe

# Check firewall
sudo ufw status

# Allow required ports
sudo ufw allow 80/tcp  # HTTP
sudo ufw allow 443/tcp # HTTPS
```

### High CPU/Memory Usage?

```bash
# Monitor resource usage
watch -n 1 'ps aux | grep mediaauto'

# Use htop
htop -p $(pgrep -f 'python3.*main.py')

# Check process threads
ps -eLf | grep mediaauto | wc -l
```

### Database Issues?

```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test database connection
sudo -u postgres psql -d mediaauto -c "SELECT 1;"

# Rebuild database
python3 /opt/mediaauto/scripts/init_db.py
```

---

## Security Recommendations

### 🔒 Change Default Password

```bash
# Reset admin credentials
sudo python3 /opt/mediaauto/scripts/reset_admin.py
```

### 🛡️ Firewall Configuration

```bash
# Enable firewall
sudo ufw enable

# Allow SSH
sudo ufw allow 22/tcp

# Allow web panel
sudo ufw allow 80/tcp

# Allow HTTPS (if using SSL)
sudo ufw allow 443/tcp

# View rules
sudo ufw status verbose
```

### 🔐 API Key Management

```bash
# Store sensitive keys securely
# Do NOT commit to git:
echo "config/settings.json" >> .gitignore

# Use environment variables for secrets
export TELEGRAM_BOT_TOKEN="your_token_here"
```

### 📅 Regular Backups

```bash
# Manual backup
/opt/mediaauto/scripts/backup_all.sh

# Automated daily backup
sudo crontab -e
# Add: 0 2 * * * /opt/mediaauto/scripts/backup_all.sh
```

---

## Updating MediaAuto

### Pull Latest Changes

```bash
cd /opt/mediaauto
git pull origin main

# Reinstall dependencies
source venv/bin/activate
pip install -r requirements.txt --upgrade

# Restart bot
sudo systemctl restart mediaauto
```

---

## Docker Installation (Alternative)

### Prerequisites
- Docker and Docker Compose installed

### Installation

```bash
cd /opt/mediaauto

# Create environment file
cp .env.example .env
# Edit .env with your settings

# Start with Docker Compose
sudo docker-compose up -d

# View logs
sudo docker-compose logs -f mediaauto

# Stop
sudo docker-compose down
```

---

## Getting Help

### Documentation
- README: `/opt/mediaauto/README.md`
- Guide: `/opt/mediaauto/INSTALLATION_GUIDE.md`
- API Docs: `http://your-server:5000/api/docs`

### Debug Mode

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
sudo systemctl restart mediaauto

# View debug logs
journalctl -u mediaauto -f | grep DEBUG
```

### Support
- Check logs for error messages
- Verify configuration syntax
- Ensure all API keys are correct
- Test with single channel first

---

## Next Steps

1. ✅ Complete installation
2. ✅ Access web dashboard
3. ✅ Add channels to monitor
4. ✅ Configure scheduler
5. ✅ Enable AI (optional)
6. ✅ Monitor logs
7. ✅ Set up backups
8. ✅ Customize watermark

---

**Happy bot hosting! 🚀**