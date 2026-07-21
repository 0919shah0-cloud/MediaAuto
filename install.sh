#!/bin/bash

# MediaAuto Installation Script
# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════╗"
echo "║      MediaAuto Installation Script         ║"
echo "║   Telegram Media Automation Bot for VPS    ║"
echo "╚════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if running on Ubuntu
if ! grep -q "Ubuntu" /etc/os-release; then
    echo -e "${RED}[✗] This script is designed for Ubuntu. Please use Ubuntu 22 or 24.${NC}"
    exit 1
fi

echo -e "${GREEN}[✓] Ubuntu detected${NC}"

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}[!] Python3 not found. Installing...${NC}"
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1-2)
echo -e "${GREEN}[✓] Python3 version: $PYTHON_VERSION${NC}"

if [ "$(printf '%s\n' "3.10" "$PYTHON_VERSION" | sort -V | head -n1)" != "3.10" ]; then
    echo -e "${RED}[✗] Python 3.10 or higher is required. Current version: $PYTHON_VERSION${NC}"
    exit 1
fi

# Install system dependencies
echo -e "${YELLOW}[!] Installing system dependencies...${NC}"
sudo apt update
sudo apt install -y \
    build-essential \
    python3-dev \
    git \
    curl \
    wget \
    libssl-dev \
    libffi-dev \
    ffmpeg \
    imagemagick

echo -e "${GREEN}[✓] System dependencies installed${NC}"

# Create app directory
APP_DIR="/opt/mediaauto"
echo -e "${YELLOW}[!] Creating application directory at $APP_DIR...${NC}"
sudo mkdir -p $APP_DIR
sudo chown $USER:$USER $APP_DIR

# Clone or navigate to repo
if [ ! -d "$APP_DIR/.git" ]; then
    cd $APP_DIR
    git init
fi

cd $APP_DIR

# Create virtual environment
echo -e "${YELLOW}[!] Creating Python virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo -e "${YELLOW}[!] Upgrading pip...${NC}"
pip install --upgrade pip setuptools wheel

# Install requirements
echo -e "${YELLOW}[!] Installing Python dependencies...${NC}"
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo -e "${RED}[✗] requirements.txt not found${NC}"
    exit 1
fi

echo -e "${GREEN}[✓] Python dependencies installed${NC}"

# Create data directories
echo -e "${YELLOW}[!] Creating data directories...${NC}"
mkdir -p $APP_DIR/data
mkdir -p $APP_DIR/downloads
mkdir -p $APP_DIR/logs
mkdir -p $APP_DIR/sessions

echo -e "${GREEN}[✓] Directories created${NC}"

# Configuration
echo -e "${BLUE}"
echo "════════════════════════════════════════════"
echo "  Configuration Setup"
echo "════════════════════════════════════════════"
echo -e "${NC}"

# Copy example config
if [ ! -f "$APP_DIR/config.json" ]; then
    cp config/example.json $APP_DIR/config.json
    echo -e "${GREEN}[✓] Configuration file created${NC}"
fi

# Get Telegram Bot Token
echo -e "${YELLOW}[?] Enter Telegram Bot Token (from @BotFather):${NC}"
read -p "> " BOT_TOKEN

# Get API ID and Hash
echo -e "${YELLOW}[?] Enter Telegram API ID (from my.telegram.org):${NC}"
read -p "> " API_ID

echo -e "${YELLOW}[?] Enter Telegram API Hash (from my.telegram.org):${NC}"
read -p "> " API_HASH

# Get Phone Number
echo -e "${YELLOW}[?] Enter Telegram phone number (for Telethon session):${NC}"
read -p "> " PHONE_NUMBER

# Update config
echo -e "${YELLOW}[!] Updating configuration...${NC}"
python3 << EOF
import json
config_path = '$APP_DIR/config.json'
with open(config_path, 'r') as f:
    config = json.load(f)

config['bot']['token'] = '$BOT_TOKEN'
config['bot']['api_id'] = '$API_ID'
config['bot']['api_hash'] = '$API_HASH'
config['bot']['phone_number'] = '$PHONE_NUMBER'

with open(config_path, 'w') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

print("[✓] Configuration updated")
EOF

# Get destination channel
echo -e "${YELLOW}[?] Enter destination channel ID (can be changed later):${NC}"
read -p "> " DEST_CHANNEL

python3 << EOF
import json
config_path = '$APP_DIR/config.json'
with open(config_path, 'r') as f:
    config = json.load(f)

config['channels']['destination'] = int($DEST_CHANNEL) if '$DEST_CHANNEL' else 0

with open(config_path, 'w') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)
EOF

# Panel credentials
echo -e "${BLUE}"
echo "════════════════════════════════════════════"
echo "  Panel Setup"
echo "════════════════════════════════════════════"
echo -e "${NC}"

echo -e "${YELLOW}[?] Enter panel admin username:${NC}"
read -p "> " PANEL_USERNAME

echo -e "${YELLOW}[?] Enter panel admin password:${NC}"
read -sp "> " PANEL_PASSWORD
echo

python3 << EOF
import json
from utils.security import hash_password

config_path = '$APP_DIR/config.json'
with open(config_path, 'r') as f:
    config = json.load(f)

config['panel']['username'] = '$PANEL_USERNAME'
config['panel']['password_hash'] = hash_password('$PANEL_PASSWORD')
config['api']['secret_key'] = hash_password('$PANEL_PASSWORD')[:32]

with open(config_path, 'w') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)
EOF

echo -e "${GREEN}[✓] Panel credentials set${NC}"

# Create systemd service
echo -e "${YELLOW}[!] Creating systemd service...${NC}"

sudo tee /etc/systemd/system/mediaauto.service > /dev/null << EOF
[Unit]
Description=MediaAuto - Telegram Media Automation Bot
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
ExecStart=$APP_DIR/venv/bin/python3 main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
echo -e "${GREEN}[✓] Systemd service created${NC}"

# Create bot startup script
echo -e "${YELLOW}[!] Creating bot startup script...${NC}"
cat > $APP_DIR/main.py << 'MAIN_EOF'
"""Main entry point for MediaAuto"""
import asyncio
import logging
from pathlib import Path

from core.bot import MediaAutoBot
from utils.logger import setup_logger
from utils.config import Config
from database.manager import DatabaseManager

logger = setup_logger(
    __name__,
    log_file="logs/mediaauto.log"
)


async def main():
    """Main function"""
    try:
        logger.info("Starting MediaAuto...")
        
        # Initialize bot
        bot = MediaAutoBot("config.json")
        
        # Run bot
        await bot.run()
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
MAIN_EOF

echo -e "${GREEN}[✓] Startup script created${NC}"

# Database initialization
echo -e "${YELLOW}[!] Initializing database...${NC}"
python3 << EOF
from database.manager import DatabaseManager
from database.models import User
from utils.security import hash_password
import json

# Load config
with open('config.json', 'r') as f:
    config = json.load(f)

# Initialize database
db = DatabaseManager(config['database'])

# Create default admin user if doesn't exist
admin = db.get_user('admin')
if not admin:
    admin_user = User(
        username='admin',
        password_hash=hash_password('admin123'),
        role='admin',
        is_active=True
    )
    db.add_user(admin_user)
    print("[✓] Default admin user created (username: admin, password: admin123)")
else:
    print("[✓] Admin user already exists")
EOF

echo -e "${GREEN}[✓] Database initialized${NC}"

# Enable autostart
echo -e "${YELLOW}[!] Enabling autostart...${NC}"
sudo systemctl enable mediaauto
echo -e "${GREEN}[✓] Autostart enabled${NC}"

# Final instructions
echo -e "${BLUE}"
echo "════════════════════════════════════════════"
echo "  Installation Complete!"
echo "════════════════════════════════════════════"
echo -e "${NC}"

echo -e "${GREEN}[✓] MediaAuto has been installed successfully!${NC}"
echo
echo "📋 Next Steps:"
echo
echo "1. Start the bot:"
echo -e "   ${YELLOW}sudo systemctl start mediaauto${NC}"
echo
echo "2. Check status:"
echo -e "   ${YELLOW}sudo systemctl status mediaauto${NC}"
echo
echo "3. View logs:"
echo -e "   ${YELLOW}sudo journalctl -u mediaauto -f${NC}"
echo
echo "4. Access panel:"
echo -e "   ${YELLOW}http://localhost:8080${NC}"
echo
echo "5. API endpoint:"
echo -e "   ${YELLOW}http://localhost:8000/api${NC}"
echo
echo "🔐 Panel Credentials:"
echo -e "   Username: ${YELLOW}$PANEL_USERNAME${NC}"
echo -e "   Password: ${YELLOW}***${NC}"
echo
echo "📝 Configuration file:"
echo -e "   ${YELLOW}$APP_DIR/config.json${NC}"
echo
echo "💾 Data directory:"
echo -e "   ${YELLOW}$APP_DIR/data${NC}"
echo
echo -e "${BLUE}════════════════════════════════════════════${NC}"
echo
