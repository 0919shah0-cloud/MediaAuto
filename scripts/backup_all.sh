#!/bin/bash

###############################################################################
#                      MediaAuto Backup Script                               #
###############################################################################

BACKUP_DIR="/opt/mediaauto/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/mediaauto_backup_$TIMESTAMP.tar.gz"

echo "[INFO] Starting MediaAuto backup..."
echo "[INFO] Backup directory: $BACKUP_DIR"

# Create backup directory if not exists
mkdir -p "$BACKUP_DIR"

# Backup configuration and database
echo "[INFO] Backing up configuration and database..."
tar -czf "$BACKUP_FILE" \
    /opt/mediaauto/config/ \
    /opt/mediaauto/database/ \
    --exclude='*.log' \
    --exclude='.git'

if [ $? -eq 0 ]; then
    echo "[✓] Backup completed: $BACKUP_FILE"
    echo "[✓] File size: $(du -h "$BACKUP_FILE" | cut -f1)"
    
    # Keep only last 10 backups
    echo "[INFO] Cleaning up old backups..."
    ls -t "$BACKUP_DIR"/mediaauto_backup_*.tar.gz | tail -n +11 | xargs -r rm
    
    echo "[✓] All backups:"
    ls -lh "$BACKUP_DIR"/mediaauto_backup_*.tar.gz | tail -10
else
    echo "[✗] Backup failed!"
    exit 1
fi