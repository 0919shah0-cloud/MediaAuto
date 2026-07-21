"""Media Downloader Service"""
import asyncio
import logging
import os
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

import yt_dlp
import requests
from telethon import TelegramClient
from telethon.types import Message

from utils.logger import setup_logger
from utils.config import Config

logger = setup_logger(__name__)


class MediaDownloader:
    """Handles media downloading from various sources"""

    def __init__(self, config: Config):
        """Initialize media downloader
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.download_config = config.download
        self.download_dir = Path("downloads")
        self.download_dir.mkdir(exist_ok=True)

    async def download_from_telegram(self, message: Message, output_dir: str) -> Optional[str]:
        """Download media from Telegram message
        
        Args:
            message: Telethon Message object
            output_dir: Output directory path
            
        Returns:
            Path to downloaded file or None
        """
        try:
            if not message.media:
                return None
            
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            file_path = await message.download_media(str(output_path))
            logger.info(f"Downloaded from Telegram: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Error downloading from Telegram: {e}")
            return None

    async def download_from_youtube(self, url: str, output_dir: str = None) -> Optional[str]:
        """Download video from YouTube
        
        Args:
            url: YouTube URL
            output_dir: Output directory
            
        Returns:
            Path to downloaded file or None
        """
        try:
            if not output_dir:
                output_dir = str(self.download_dir / f"youtube/{datetime.now().strftime('%Y%m%d')}")
            
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            ydl_opts = {
                'format': self.download_config.get('quality', 'best'),
                'outtmpl': str(output_path / '%(title)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
                logger.info(f"Downloaded from YouTube: {file_path}")
                return file_path
                
        except Exception as e:
            logger.error(f"Error downloading from YouTube: {e}")
            return None

    async def download_from_instagram(self, url: str, output_dir: str = None) -> Optional[str]:
        """Download media from Instagram
        
        Args:
            url: Instagram URL
            output_dir: Output directory
            
        Returns:
            Path to downloaded file or None
        """
        try:
            if not output_dir:
                output_dir = str(self.download_dir / f"instagram/{datetime.now().strftime('%Y%m%d')}")
            
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            ydl_opts = {
                'outtmpl': str(output_path / '%(title)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
                logger.info(f"Downloaded from Instagram: {file_path}")
                return file_path
                
        except Exception as e:
            logger.error(f"Error downloading from Instagram: {e}")
            return None

    async def download_from_tiktok(self, url: str, output_dir: str = None) -> Optional[str]:
        """Download video from TikTok
        
        Args:
            url: TikTok URL
            output_dir: Output directory
            
        Returns:
            Path to downloaded file or None
        """
        try:
            if not output_dir:
                output_dir = str(self.download_dir / f"tiktok/{datetime.now().strftime('%Y%m%d')}")
            
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            ydl_opts = {
                'outtmpl': str(output_path / '%(title)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
                logger.info(f"Downloaded from TikTok: {file_path}")
                return file_path
                
        except Exception as e:
            logger.error(f"Error downloading from TikTok: {e}")
            return None

    async def download_from_facebook(self, url: str, output_dir: str = None) -> Optional[str]:
        """Download video from Facebook
        
        Args:
            url: Facebook URL
            output_dir: Output directory
            
        Returns:
            Path to downloaded file or None
        """
        try:
            if not output_dir:
                output_dir = str(self.download_dir / f"facebook/{datetime.now().strftime('%Y%m%d')}")
            
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            ydl_opts = {
                'outtmpl': str(output_path / '%(title)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
                logger.info(f"Downloaded from Facebook: {file_path}")
                return file_path
                
        except Exception as e:
            logger.error(f"Error downloading from Facebook: {e}")
            return None

    async def download_from_x(self, url: str, output_dir: str = None) -> Optional[str]:
        """Download media from X (Twitter)
        
        Args:
            url: X/Twitter URL
            output_dir: Output directory
            
        Returns:
            Path to downloaded file or None
        """
        try:
            if not output_dir:
                output_dir = str(self.download_dir / f"x/{datetime.now().strftime('%Y%m%d')}")
            
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            ydl_opts = {
                'outtmpl': str(output_path / '%(title)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
                logger.info(f"Downloaded from X: {file_path}")
                return file_path
                
        except Exception as e:
            logger.error(f"Error downloading from X: {e}")
            return None
