"""Task Scheduler Service"""
import asyncio
import logging
from typing import Dict, Any
from datetime import datetime

from telegram.ext import Application
from utils.logger import setup_logger
from database.manager import DatabaseManager

logger = setup_logger(__name__)


class Scheduler:
    """Manages scheduled posting"""

    def __init__(self, db: DatabaseManager, app: Application):
        """Initialize scheduler
        
        Args:
            db: Database manager
            app: Telegram application
        """
        self.db = db
        self.app = app
        self.running = False
        self.task = None

    async def start(self) -> None:
        """Start scheduler"""
        self.running = True
        self.task = asyncio.create_task(self._run())
        logger.info("Scheduler started")

    async def _run(self) -> None:
        """Main scheduler loop"""
        while self.running:
            try:
                await self._process_scheduled_posts()
                await asyncio.sleep(300)  # Check every 5 minutes
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
                await asyncio.sleep(300)

    async def _process_scheduled_posts(self) -> None:
        """Process scheduled posts"""
        try:
            posts = self.db.get_posts(status='pending')
            for post in posts:
                if post.scheduled_at and datetime.now() >= post.scheduled_at:
                    logger.info(f"Processing scheduled post {post.id}")
        except Exception as e:
            logger.error(f"Error processing scheduled posts: {e}")

    async def stop(self) -> None:
        """Stop scheduler"""
        self.running = False
        if self.task:
            self.task.cancel()
        logger.info("Scheduler stopped")
