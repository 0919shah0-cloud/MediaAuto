"""Telegram Sender Service"""
import asyncio
import logging
from typing import Optional
from pathlib import Path

from telegram import Bot
from telethon import TelegramClient
from telethon.tl.types import InputPeerChannel, InputPeerChat

from utils.logger import setup_logger
from utils.config import Config
from database.manager import DatabaseManager
from database.models import Post

logger = setup_logger(__name__)


class TelegramSender:
    """Handles sending messages to Telegram"""

    def __init__(self, config: Config, telethon_client: TelegramClient):
        """Initialize Telegram sender
        
        Args:
            config: Configuration object
            telethon_client: Telethon client instance
        """
        self.config = config
        self.telethon_client = telethon_client

    async def send_message(self, chat_id: int, caption: str, media_path: Optional[str] = None) -> bool:
        """Send message to chat
        
        Args:
            chat_id: Telegram chat ID
            caption: Message caption/text
            media_path: Path to media file (optional)
            
        Returns:
            True if sent successfully
        """
        try:
            if media_path and Path(media_path).exists():
                await self.telethon_client.send_file(chat_id, media_path, caption=caption)
            else:
                await self.telethon_client.send_message(chat_id, caption)
            
            logger.info(f"Message sent to {chat_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending message to {chat_id}: {e}")
            return False

    async def send_photo(self, chat_id: int, photo_path: str, caption: str = None) -> bool:
        """Send photo to chat
        
        Args:
            chat_id: Telegram chat ID
            photo_path: Path to photo file
            caption: Photo caption
            
        Returns:
            True if sent successfully
        """
        try:
            await self.telethon_client.send_file(chat_id, photo_path, caption=caption)
            logger.info(f"Photo sent to {chat_id}")
            return True
        except Exception as e:
            logger.error(f"Error sending photo to {chat_id}: {e}")
            return False

    async def send_video(self, chat_id: int, video_path: str, caption: str = None) -> bool:
        """Send video to chat
        
        Args:
            chat_id: Telegram chat ID
            video_path: Path to video file
            caption: Video caption
            
        Returns:
            True if sent successfully
        """
        try:
            await self.telethon_client.send_file(chat_id, video_path, caption=caption)
            logger.info(f"Video sent to {chat_id}")
            return True
        except Exception as e:
            logger.error(f"Error sending video to {chat_id}: {e}")
            return False

    async def send_document(self, chat_id: int, document_path: str, caption: str = None) -> bool:
        """Send document to chat
        
        Args:
            chat_id: Telegram chat ID
            document_path: Path to document file
            caption: Document caption
            
        Returns:
            True if sent successfully
        """
        try:
            await self.telethon_client.send_file(chat_id, document_path, caption=caption)
            logger.info(f"Document sent to {chat_id}")
            return True
        except Exception as e:
            logger.error(f"Error sending document to {chat_id}: {e}")
            return False
