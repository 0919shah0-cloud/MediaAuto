"""Message Handlers for Telegram Bot"""
import logging
from telegram import Update
from telegram.ext import ContextTypes

from utils.logger import setup_logger

logger = setup_logger(__name__)


async def process_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process incoming messages
    
    Args:
        update: Update object from Telegram
        context: Context object
    """
    try:
        message = update.message
        if not message:
            return
        
        logger.info(f"Message from {update.effective_user.id}: {message.text[:50] if message.text else 'media'}")
        
        # Log message for debugging
        if message.text:
            logger.debug(f"Text: {message.text}")
        
        if message.photo:
            logger.debug(f"Photo received")
        
        if message.video:
            logger.debug(f"Video received")
            
    except Exception as e:
        logger.error(f"Error processing message: {e}")
