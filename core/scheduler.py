"""Task Scheduler for posting content"""
import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Optional

from database.models import Post
from database.manager import DatabaseManager
from utils.logger import setup_logger
from utils.config import Config

logger = setup_logger(__name__)


class TaskScheduler:
    """Manages scheduled posting of content"""

    def __init__(self, db: DatabaseManager, config: Config):
        """Initialize scheduler
        
        Args:
            db: Database manager instance
            config: Configuration object
        """
        self.db = db
        self.config = config
        self.running = False
        self.interval = config.scheduler['interval']
        self.task = None

    async def start(self) -> None:
        """Start the scheduler"""
        self.running = True
        logger.info(f"Scheduler started with interval: {self.interval}s")
        
        try:
            self.task = asyncio.create_task(self._run())
        except Exception as e:
            logger.error(f"Error starting scheduler: {e}")
            self.running = False

    async def _run(self) -> None:
        """Main scheduler loop"""
        while self.running:
            try:
                await self._check_and_post()
                await asyncio.sleep(self.interval)
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
                await asyncio.sleep(self.interval)

    async def _check_and_post(self) -> None:
        """Check pending posts and send them"""
        try:
            pending_posts = self.db.get_posts(status='pending')
            
            for post in pending_posts:
                if self._should_post(post):
                    await self._post_message(post)
                    
        except Exception as e:
            logger.error(f"Error checking posts: {e}")

    def _should_post(self, post: Post) -> bool:
        """Check if post should be sent
        
        Args:
            post: Post object
            
        Returns:
            True if post should be sent
        """
        if not post.scheduled_at:
            return True
        
        return datetime.now() >= post.scheduled_at

    async def _post_message(self, post: Post) -> None:
        """Send scheduled message
        
        Args:
            post: Post object to send
        """
        try:
            # Implementation will be added in services
            logger.info(f"Posting message: {post.id}")
            post.status = 'sent'
            post.sent_at = datetime.now()
            self.db.update_post(post)
            
        except Exception as e:
            logger.error(f"Error posting message {post.id}: {e}")
            post.status = 'failed'
            post.error_message = str(e)
            self.db.update_post(post)

    async def stop(self) -> None:
        """Stop the scheduler"""
        self.running = False
        if self.task:
            self.task.cancel()
        logger.info("Scheduler stopped")

    async def schedule_post(self, post_id: int, delay_seconds: int) -> None:
        """Schedule a post for later
        
        Args:
            post_id: ID of post to schedule
            delay_seconds: Seconds to delay before posting
        """
        post = self.db.get_post(post_id)
        if post:
            post.scheduled_at = datetime.now() + timedelta(seconds=delay_seconds)
            self.db.update_post(post)
            logger.info(f"Post {post_id} scheduled for {delay_seconds}s from now")
