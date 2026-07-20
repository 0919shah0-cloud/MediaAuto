#!/bin/bash

###############################################################################
#                         MediaAuto Install Script                            #
#                      Professional Installation & Setup                      #
###############################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="MediaAuto"
PROJECT_DIR="/opt/mediaauto"
VENV_DIR="$PROJECT_DIR/venv"
CONFIG_FILE="$PROJECT_DIR/config/settings.json"
LOG_DIR="$PROJECT_DIR/logs"
DB_DIR="$PROJECT_DIR/database"

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Check if running as root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        print_error "This script must be run as root. Please use: sudo bash install.sh"
        exit 1
    fi
}

# Detect Ubuntu version
detect_ubuntu() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        UBUNTU_VERSION=$VERSION_ID
        print_success "Detected Ubuntu $UBUNTU_VERSION"
    else
        print_error "Could not detect Ubuntu version"
        exit 1
    fi
}

# Update system packages
update_system() {
    print_info "Updating system packages..."
    apt-get update -qq
    apt-get upgrade -y -qq
    print_success "System packages updated"
}

# Install system dependencies
install_dependencies() {
    print_info "Installing system dependencies..."
    
    apt-get install -y -qq \
        python3.11 \
        python3.11-venv \
        python3-pip \
        git \
        curl \
        wget \
        ffmpeg \
        postgresql \
        postgresql-contrib \
        redis-server \
        nginx \
        supervisor \
        build-essential \
        libssl-dev \
        libffi-dev \
        python3-dev \
        sqlite3 \
        htop \
        nano \
        vim \
        tmux
    
    print_success "System dependencies installed"
}

# Create project directory
create_directories() {
    print_info "Creating project directories..."
    
    mkdir -p "$PROJECT_DIR"
    mkdir -p "$LOG_DIR"
    mkdir -p "$DB_DIR"
    mkdir -p "$PROJECT_DIR/config"
    mkdir -p "$PROJECT_DIR/downloads"
    mkdir -p "$PROJECT_DIR/tmp"
    mkdir -p "$PROJECT_DIR/backups"
    
    print_success "Directories created"
}

# Clone or download project files
setup_project_files() {
    print_info "Setting up project files..."
    
    if [ ! -d "$PROJECT_DIR/.git" ]; then
        print_info "Cloning MediaAuto repository..."
        cd /tmp
        git clone https://github.com/0919shah0-cloud/MediaAuto.git mediaauto_temp
        cp -r mediaauto_temp/* "$PROJECT_DIR/"
        rm -rf mediaauto_temp
    fi
    
    print_success "Project files setup complete"
}

# Create Python virtual environment
setup_venv() {
    print_info "Creating Python virtual environment..."
    
    python3.11 -m venv "$VENV_DIR"
    source "$VENV_DIR/bin/activate"
    
    pip install --upgrade pip setuptools wheel -q
    
    print_success "Virtual environment created"
}

# Install Python dependencies
install_python_packages() {
    print_info "Installing Python packages..."
    
    source "$VENV_DIR/bin/activate"
    pip install -r "$PROJECT_DIR/requirements.txt" -q
    
    print_success "Python packages installed"
}

# Interactive configuration setup
configure_bot() {
    print_info "Starting interactive configuration setup..."
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}         MEDIAAUTO - CONFIGURATION SETUP${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
    echo ""
    
    # Initialize config file
    cat > "$CONFIG_FILE" << 'EOF'
{
  "bot": {},
  "telegram": {},
  "ai": {},
  "scheduler": {},
  "panel": {},
  "database": {},
  "sources": [],
  "channels": []
}
EOF
    
    # Bot configuration
    echo -e "${YELLOW}1. Telegram Bot Token${NC}"
    print_info "Get your bot token from @BotFather on Telegram"
    read -p "Enter Telegram Bot Token: " BOT_TOKEN
    
    # Telegram API configuration
    echo ""
    echo -e "${YELLOW}2. Telegram API Credentials${NC}"
    print_info "Get these from https://my.telegram.org/apps"
    read -p "Enter Telegram API ID: " API_ID
    read -p "Enter Telegram API HASH: " API_HASH
    
    # Phone number
    echo ""
    echo -e "${YELLOW}3. Telegram Account${NC}"
    read -p "Enter your Telegram phone number (with country code, e.g., +989123456789): " PHONE_NUMBER
    
    # Channels to monitor
    echo ""
    echo -e "${YELLOW}4. Channels to Monitor${NC}"
    print_info "Enter channel usernames or IDs (comma-separated, e.g., @channel1,@channel2)"
    read -p "Enter channels: " CHANNELS
    
    # Output channel/group
    echo ""
    echo -e "${YELLOW}5. Output Destination${NC}"
    print_info "Where should the bot post content?"
    read -p "Enter output channel/group username or ID: " OUTPUT_CHANNEL
    
    # AI settings
    echo ""
    echo -e "${YELLOW}6. AI Settings${NC}"
    print_info "Choose AI provider:"
    echo "1) OpenAI"
    echo "2) Google Gemini"
    echo "3) Claude (Anthropic)"
    echo "4) None (disable AI features)"
    read -p "Select option (1-4): " AI_CHOICE
    
    AI_PROVIDER="none"
    AI_KEY=""
    if [ "$AI_CHOICE" = "1" ]; then
        AI_PROVIDER="openai"
        read -p "Enter OpenAI API Key: " AI_KEY
    elif [ "$AI_CHOICE" = "2" ]; then
        AI_PROVIDER="google"
        read -p "Enter Google Gemini API Key: " AI_KEY
    elif [ "$AI_CHOICE" = "3" ]; then
        AI_PROVIDER="anthropic"
        read -p "Enter Claude API Key: " AI_KEY
    fi
    
    # Scheduler settings
    echo ""
    echo -e "${YELLOW}7. Scheduler Settings${NC}"
    print_info "Choose posting interval:"
    echo "1) Every 5 minutes"
    echo "2) Every 10 minutes"
    echo "3) Every 30 minutes"
    echo "4) Every 1 hour"
    echo "5) Custom (minutes)"
    read -p "Select option (1-5): " SCHEDULER_CHOICE
    
    case $SCHEDULER_CHOICE in
        1) SCHEDULER_INTERVAL=5 ;;
        2) SCHEDULER_INTERVAL=10 ;;
        3) SCHEDULER_INTERVAL=30 ;;
        4) SCHEDULER_INTERVAL=60 ;;
        5) read -p "Enter interval in minutes: " SCHEDULER_INTERVAL ;;
        *) SCHEDULER_INTERVAL=30 ;;
    esac
    
    # Watermark settings
    echo ""
    echo -e "${YELLOW}8. Watermark Settings${NC}"
    read -p "Enter your channel username for watermark (e.g., @MyChannel): " WATERMARK_TEXT
    
    # Panel settings
    echo ""
    echo -e "${YELLOW}9. Web Panel Configuration${NC}"
    read -p "Enter panel admin username (default: admin): " PANEL_USERNAME
    PANEL_USERNAME=${PANEL_USERNAME:-admin}
    read -sp "Enter panel admin password: " PANEL_PASSWORD
    echo ""
    read -p "Enter panel port (default: 5000): " PANEL_PORT
    PANEL_PORT=${PANEL_PORT:-5000}
    
    # Database choice
    echo ""
    echo -e "${YELLOW}10. Database Selection${NC}"
    print_info "Choose database:"
    echo "1) SQLite (recommended for small deployments)"
    echo "2) PostgreSQL (recommended for production)"
    read -p "Select option (1-2): " DB_CHOICE
    
    if [ "$DB_CHOICE" = "2" ]; then
        DB_TYPE="postgresql"
        read -p "Enter PostgreSQL host (default: localhost): " DB_HOST
        DB_HOST=${DB_HOST:-localhost}
        read -p "Enter PostgreSQL port (default: 5432): " DB_PORT
        DB_PORT=${DB_PORT:-5432}
        read -p "Enter database name (default: mediaauto): " DB_NAME
        DB_NAME=${DB_NAME:-mediaauto}
        read -p "Enter database user (default: mediaauto): " DB_USER
        DB_USER=${DB_USER:-mediaauto}
        read -sp "Enter database password: " DB_PASS
        echo ""
    else
        DB_TYPE="sqlite"
        DB_HOST="localhost"
        DB_PORT="0"
        DB_NAME="$DB_DIR/mediaauto.db"
        DB_USER=""
        DB_PASS=""
    fi
    
    # Notification settings
    echo ""
    echo -e "${YELLOW}11. Additional Settings${NC}"
    read -p "Enable error notifications via Telegram? (y/n): " NOTIFICATIONS
    
    # Write configuration to JSON
    print_info "Saving configuration..."
    
    python3 << PYEOF
import json
from datetime import datetime

config = {
    "bot": {
        "token": "$BOT_TOKEN",
        "enabled": True
    },
    "telegram": {
        "api_id": "$API_ID",
        "api_hash": "$API_HASH",
        "phone_number": "$PHONE_NUMBER",
        "session_name": "mediaauto_session"
    },
    "channels": [ch.strip() for ch in "$CHANNELS".split(",") if ch.strip()],
    "output_channel": "$OUTPUT_CHANNEL",
    "ai": {
        "provider": "$AI_PROVIDER",
        "api_key": "$AI_KEY",
        "enabled": "$AI_PROVIDER" != "none"
    },
    "scheduler": {
        "interval_minutes": $SCHEDULER_INTERVAL,
        "enabled": True
    },
    "watermark": {
        "text": "$WATERMARK_TEXT",
        "enabled": True,
        "position": "bottom_right"
    },
    "panel": {
        "username": "$PANEL_USERNAME",
        "password": "$PANEL_PASSWORD",
        "port": $PANEL_PORT,
        "host": "0.0.0.0",
        "debug": False
    },
    "database": {
        "type": "$DB_TYPE",
        "host": "$DB_HOST",
        "port": "$DB_PORT",
        "name": "$DB_NAME",
        "user": "$DB_USER",
        "password": "$DB_PASS",
        "timezone": "UTC"
    },
    "logging": {
        "level": "INFO",
        "max_bytes": 10485760,
        "backup_count": 5
    },
    "sources": {
        "telegram": True,
        "instagram": False,
        "youtube": False,
        "tiktok": False,
        "facebook": False,
        "twitter": False
    },
    "created_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "version": "1.0.0"
}

with open("$CONFIG_FILE", "w") as f:
    json.dump(config, f, indent=4, ensure_ascii=False)

print("Configuration saved successfully!")
PYEOF
    
    print_success "Configuration completed"
}

# Setup PostgreSQL (if selected)
setup_postgresql() {
    if grep -q '"postgresql"' "$CONFIG_FILE"; then
        print_info "Initializing PostgreSQL database..."
        
        # Start PostgreSQL
        systemctl start postgresql
        systemctl enable postgresql
        
        # Create database and user
        DB_NAME=$(grep -o '"name": "[^"]*"' "$CONFIG_FILE" | head -1 | cut -d'"' -f4)
        DB_USER=$(grep -o '"user": "[^"]*"' "$CONFIG_FILE" | head -1 | cut -d'"' -f4)
        DB_PASS=$(grep -o '"password": "[^"]*"' "$CONFIG_FILE" | head -1 | cut -d'"' -f4)
        
        sudo -u postgres psql << PGEOF
CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';
CREATE DATABASE $DB_NAME OWNER $DB_USER;
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO $DB_USER;
PGEOF
        
        print_success "PostgreSQL database initialized"
    fi
}

# Create systemd service
create_systemd_service() {
    print_info "Creating systemd service..."
    
    cat > /etc/systemd/system/mediaauto.service << EOF
[Unit]
Description=MediaAuto - Automated Media Distribution Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$VENV_DIR/bin"
ExecStart=$VENV_DIR/bin/python3 $PROJECT_DIR/main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF
    
    systemctl daemon-reload
    systemctl enable mediaauto
    
    print_success "Systemd service created and enabled"
}

# Create nginx configuration
create_nginx_config() {
    print_info "Configuring nginx..."
    
    PANEL_PORT=$(grep -o '"port": [0-9]*' "$CONFIG_FILE" | cut -d' ' -f2)
    
    cat > /etc/nginx/sites-available/mediaauto << EOF
server {
    listen 80;
    server_name _;
    client_max_body_size 100M;

    location / {
        proxy_pass http://127.0.0.1:$PANEL_PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_redirect off;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:$PANEL_PORT/api/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF
    
    # Enable site
    ln -sf /etc/nginx/sites-available/mediaauto /etc/nginx/sites-enabled/mediaauto
    rm -f /etc/nginx/sites-enabled/default
    
    # Test and reload
    nginx -t && systemctl restart nginx
    
    print_success "Nginx configured"
}

# Initialize database
initialize_database() {
    print_info "Initializing database..."
    
    source "$VENV_DIR/bin/activate"
    cd "$PROJECT_DIR"
    python3 scripts/init_db.py
    
    print_success "Database initialized"
}

# Set permissions
set_permissions() {
    print_info "Setting file permissions..."
    
    chown -R www-data:www-data "$PROJECT_DIR"
    chmod -R 755 "$PROJECT_DIR"
    chmod -R 775 "$LOG_DIR"
    chmod -R 775 "$DB_DIR"
    chmod 600 "$CONFIG_FILE"
    
    print_success "Permissions set"
}

# Start services
start_services() {
    print_info "Starting services..."
    
    systemctl start redis-server
    systemctl enable redis-server
    
    systemctl start nginx
    systemctl enable nginx
    
    systemctl start mediaauto
    
    print_success "Services started"
}

# Display post-installation information
display_info() {
    echo ""
    echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}     ✓ MediaAuto Installation Complete!${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
    echo ""
    print_success "All components installed successfully"
    echo ""
    echo -e "${BLUE}📊 Important Information:${NC}"
    echo ""
    
    PANEL_PORT=$(grep -o '"port": [0-9]*' "$CONFIG_FILE" | cut -d' ' -f2)
    PANEL_USER=$(grep -o '"username": "[^"]*"' "$CONFIG_FILE" | head -1 | cut -d'"' -f4)
    
    echo "  📱 Bot Status: Check with 'systemctl status mediaauto'"
    echo "  🌐 Web Panel: http://$(hostname -I | awk '{print $1}'):$PANEL_PORT"
    echo "  👤 Panel Username: $PANEL_USER"
    echo "  📁 Project Directory: $PROJECT_DIR"
    echo "  📋 Configuration: $CONFIG_FILE"
    echo "  📝 Logs: $LOG_DIR"
    echo ""
    echo -e "${BLUE}Useful Commands:${NC}"
    echo "  • View bot logs: journalctl -u mediaauto -f"
    echo "  • Restart bot: systemctl restart mediaauto"
    echo "  • Stop bot: systemctl stop mediaauto"
    echo "  • View configuration: cat $CONFIG_FILE"
    echo "  • Edit configuration: nano $CONFIG_FILE (then restart bot)"
    echo ""
    echo -e "${YELLOW}📌 Next Steps:${NC}"
    echo "  1. Access the web panel at the URL above"
    echo "  2. Monitor the bot with: journalctl -u mediaauto -f"
    echo "  3. Configure additional sources from the panel"
    echo "  4. Check logs for any errors"
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
    echo ""
}

# Main installation flow
main() {
    clear
    echo -e "${BLUE}╔═══════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║         MediaAuto - Professional Setup            ║${NC}"
    echo -e "${BLUE}║     Automated Media Distribution & Management     ║${NC}"
    echo -e "${BLUE}╚═══════════════════════════════════════════════════╝${NC}"
    echo ""
    
    check_root
    detect_ubuntu
    
    print_info "Starting installation process..."
    echo ""
    
    update_system
    install_dependencies
    create_directories
    setup_project_files
    setup_venv
    install_python_packages
    configure_bot
    setup_postgresql
    create_systemd_service
    create_nginx_config
    initialize_database
    set_permissions
    start_services
    
    display_info
}

# Run main function
main "$@"
