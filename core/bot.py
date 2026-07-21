"""Main Bot Class for MediaAuto"""
import json
import asyncio
import logging
from pathlib import Path
from datetime import datetime

from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError

from database.models import Channel, Post, User
from database.manager import DatabaseManager
from handlers import message_handler, command_handler
from services import MediaDownloader, CaptionProcessor, Scheduler
from utils.logger import setup_logger
from utils.config import Config

logger = setup_logger(__name__)


class MediaAutoBot:
    """Main bot class handling Telegram operations"""

    def __init__(self, config_path: str = "config.json"):
        """Initialize MediaAutoBot
        
        Args:
            config_path: Path to configuration file
        """
        self.config = Config(config_path)
        self.db = DatabaseManager(self.config.database)
        self.app = None
        self.telethon_client = None
        self.scheduler = None
        self.media_downloader = MediaDownloader(self.config)
        self.caption_processor = CaptionProcessor(self.config)
        
        logger.info("MediaAutoBot initialized")

    async def setup(self) -> None:
        """Setup bot application and handlers"""
        self.app = Application.builder().token(self.config.bot['token']).build()
        
        # Add handlers
        self.app.add_handler(CommandHandler('start', command_handler.start))
        self.app.add_handler(CommandHandler('help', command_handler.help_command))
        self.app.add_handler(MessageHandler(filters.ALL, message_handler.process_message))
        
        # Setup error handler
        self.app.add_error_handler(self.error_handler)
        
        # Setup post and pre checkout query handlers
        self.app.post_init = self.post_init
        
        logger.info("Bot setup completed")

    async def setup_telethon(self) -> None:
        """Setup Telethon client for automatic post fetching"""
        try:
            self.telethon_client = TelegramClient(
                self.config.bot['session_name'],
                self.config.bot['api_id'],
                self.config.bot['api_hash']
            )
            
            await self.telethon_client.connect()
            
            if not await self.telethon_client.is_user_authorized():
                await self.telethon_client.send_code_request(self.config.bot['phone_number'])
                code = input("Enter the code you received: ")
                try:
                    await self.telethon_client.sign_in(self.config.bot['phone_number'], code)
                except SessionPasswordNeededError:
                    password = input("Two-factor authentication is enabled. Enter password: ")
                    await self.telethon_client.sign_in(password=password)
            
            logger.info("Telethon client connected")
            
        except Exception as e:
            logger.error(f"Failed to setup Telethon: {e}")
            raise

    async def start_listening(self) -> None:
        """Start listening to source channels"""
        if not self.telethon_client:
            await self.setup_telethon()
        
        sources = self.db.get_channels(channel_type='source')
        
        @self.telethon_client.on(events.NewMessage)
        async def handle_new_message(event):
            """Handle new messages from monitored channels"""
            try:
                # Check if message is from source channel
                if event.chat_id not in [int(ch.channel_id) for ch in sources]:
                    return
                
                await self.process_message(event)
                
            except Exception as e:
                logger.error(f"Error processing message: {e}")
        
        logger.info(f"Listening to {len(sources)} source channels")

    async def process_message(self, event) -> None:
        """Process incoming message
        
        Args:
            event: Telethon event object
        """
        try:
            message = event.message
            
            # Extract caption
            caption = message.text or ""
            
            # Check for duplicate
            if self.config.duplicate_check['enabled']:
                if self.db.is_duplicate(caption):
                    logger.info(f"Duplicate message detected: {caption[:50]}")
                    return
            
            # Process caption
            processed_caption = await self.caption_processor.process(caption)
            
            # Download media if present
            media_path = None
            if message.media:
                media_path = await self.media_downloader.download_from_telegram(
                    message, 
                    f"downloads/{datetime.now().strftime('%Y%m%d')}"
                )
            
            # Store in database
            post = Post(
                source_channel_id=event.chat_id,
                original_caption=caption,
                processed_caption=processed_caption,
                media_path=media_path,
                status='pending',
                created_at=datetime.now()
            )
            self.db.add_post(post)
            
            logger.info(f"Message processed and stored: {caption[:50]}")
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    async def post_init(self, application: Application) -> None:
        """Post initialization tasks
        
        Args:
            application: Telegram Application
        """
        await self.setup_telethon()
        await self.start_listening()
        
        # Start scheduler
        self.scheduler = Scheduler(self.db, self.app)
        await self.scheduler.start()

    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Log the error and send a telegram message to notify the developer
        
        Args:
            update: Update from Telegram
            context: Context object
        """
        logger.error(msg="Exception while handling an update:", exc_info=context.error)

    async def start(self) -> None:
        """Start the bot"""
        try:
            await self.setup()
            await self.app.initialize()
            await self.app.start()
            logger.info("Bot started successfully")
        except Exception as e:
            logger.error(f"Failed to start bot: {e}")
            raise

    async def stop(self) -> None:
        """Stop the bot"""
        try:
            if self.scheduler:
                await self.scheduler.stop()
            if self.app:
                await self.app.stop()
            if self.telethon_client:
                await self.telethon_client.disconnect()
            logger.info("Bot stopped")
        except Exception as e:
            logger.error(f"Error stopping bot: {e}")

    async def run(self) -> None:
        """Run the bot indefinitely"""
        await self.start()
        await self.app.updater.start_polling()
        try:
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            await self.stop()
