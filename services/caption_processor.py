"""Caption Processing Service"""
import re
import logging
from typing import Optional

from utils.logger import setup_logger
from utils.config import Config

logger = setup_logger(__name__)


class CaptionProcessor:
    """Processes and transforms captions"""

    def __init__(self, config: Config):
        """Initialize caption processor
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.processing = config.processing

    async def process(self, caption: str) -> str:
        """Process caption with all enabled transformations
        
        Args:
            caption: Original caption text
            
        Returns:
            Processed caption
        """
        try:
            result = caption
            
            # Remove hashtags
            if self.processing.get('remove_hashtags', False):
                result = self._remove_hashtags(result)
            
            # Remove mentions
            if self.processing.get('remove_mentions', False):
                result = self._remove_mentions(result)
            
            # Remove links
            if self.processing.get('remove_links', False):
                result = self._remove_links(result)
            
            # Clean extra whitespace
            result = self._clean_whitespace(result)
            
            logger.info(f"Caption processed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error processing caption: {e}")
            return caption

    def _remove_hashtags(self, text: str) -> str:
        """Remove hashtags from text
        
        Args:
            text: Text content
            
        Returns:
            Text without hashtags
        """
        return re.sub(r'#\w+', '', text)

    def _remove_mentions(self, text: str) -> str:
        """Remove mentions from text
        
        Args:
            text: Text content
            
        Returns:
            Text without mentions
        """
        return re.sub(r'@\w+', '', text)

    def _remove_links(self, text: str) -> str:
        """Remove URLs from text
        
        Args:
            text: Text content
            
        Returns:
            Text without URLs
        """
        return re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)

    def _clean_whitespace(self, text: str) -> str:
        """Clean extra whitespace
        
        Args:
            text: Text content
            
        Returns:
            Text with cleaned whitespace
        """
        return re.sub(r'\s+', ' ', text).strip()

    async def translate_to_persian(self, text: str) -> str:
        """Translate text to Persian (placeholder)
        
        Args:
            text: Text to translate
            
        Returns:
            Translated text
        """
        # This would use a translation API
        logger.info(f"Translation requested for: {text[:50]}")
        return text

    async def summarize(self, text: str, max_length: int = 500) -> str:
        """Summarize text
        
        Args:
            text: Text to summarize
            max_length: Maximum length of summary
            
        Returns:
            Summarized text
        """
        if len(text) <= max_length:
            return text
        return text[:max_length] + "..."

    async def add_emoji(self, text: str) -> str:
        """Add relevant emojis to text
        
        Args:
            text: Text content
            
        Returns:
            Text with emojis
        """
        # Add emojis based on keywords
        emoji_map = {
            'موسیقی': '🎵',
            'ویدیو': '🎬',
            'عکس': '📸',
            'خبر': '📰',
            'ورزش': '⚽',
            'کمدی': '😂',
            'درام': '🎭',
        }
        
        for keyword, emoji in emoji_map.items():
            if keyword in text.lower():
                text = f"{emoji} {text}"
                break
        
        return text
