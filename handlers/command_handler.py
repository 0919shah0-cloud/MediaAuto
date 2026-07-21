"""Command Handlers for Telegram Bot"""
import logging
from telegram import Update
from telegram.ext import ContextTypes

from utils.logger import setup_logger

logger = setup_logger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command
    
    Args:
        update: Update object from Telegram
        context: Context object
    """
    await update.message.reply_text(
        "سلام! من یک ربات خودکار برای مدیریت محتوای تلگرام هستم.\n"
        "برای اطلاعات بیشتر /help را بزن."
    )
    logger.info(f"Start command from user {update.effective_user.id}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command
    
    Args:
        update: Update object from Telegram
        context: Context object
    """
    help_text = """📚 راهنمای دستورات:
    
/start - شروع ربات
/help - نمایش این پیام
/status - وضعیت ربات
/settings - تنظیمات
/channels - مدیریت کانال‌ها

🌐 برای دسترسی به پنل:
http://localhost:8080
    """
    await update.message.reply_text(help_text)
    logger.info(f"Help command from user {update.effective_user.id}")


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /status command
    
    Args:
        update: Update object from Telegram
        context: Context object
    """
    status_text = """✅ وضعیت ربات:
    
🟢 ربات فعال است
📊 پست‌های معلق: 0
✉️ پست‌های ارسال‌شده: 0
❌ پست‌های ناموفق: 0
    """
    await update.message.reply_text(status_text)
    logger.info(f"Status command from user {update.effective_user.id}")
