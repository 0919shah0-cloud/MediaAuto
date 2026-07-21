#!/usr/bin/env python3
"""Main entry point for MediaAuto"""
import asyncio
import logging
import sys
from pathlib import Path

from core.bot import MediaAutoBot
from utils.logger import setup_logger
from utils.config import Config

logger = setup_logger(
    __name__,
    log_file="logs/mediaauto.log"
)


async def main():
    """Main function"""
    try:
        logger.info("Starting MediaAuto...")
        
        # Check if config exists
        if not Path("config.json").exists():
            logger.error("config.json not found. Please run install.sh first.")
            sys.exit(1)
        
        # Initialize bot
        bot = MediaAutoBot("config.json")
        
        # Setup bot
        await bot.setup()
        
        # Run bot
        await bot.app.initialize()
        await bot.app.start()
        await bot.app.updater.start_polling()
        
        logger.info("MediaAuto started successfully")
        
        # Keep running
        try:
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            logger.info("Shutting down...")
            await bot.stop()
        
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        sys.exit(0)
