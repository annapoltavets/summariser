"""
Telegram Notifier Module

This module handles sending messages to Telegram.
"""

import logging
from telegram import Bot
from telegram.constants import ParseMode
from typing import Optional

logger = logging.getLogger(__name__)


class TelegramNotifier:
    """Sends notifications to Telegram."""
    
    def __init__(self, bot_token: str, chat_id: str):
        """
        Initialize the Telegram notifier.
        
        Args:
            bot_token: Telegram bot token
            chat_id: Telegram chat ID to send messages to
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.bot = Bot(token=bot_token)
    
    async def send_message(self, text: str, parse_mode: str = ParseMode.MARKDOWN) -> bool:
        """
        Send a message to Telegram.
        
        Args:
            text: Message text to send
            parse_mode: Parse mode for formatting (MARKDOWN or HTML)
            
        Returns:
            True if message was sent successfully, False otherwise
        """
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=text,
                parse_mode=parse_mode
            )
            logger.info(f"Message sent to Telegram chat {self.chat_id}")
            return True
        except Exception as e:
            logger.error(f"Error sending message to Telegram: {e}")
            return False
    
    async def send_summary(self, summary: str) -> bool:
        """
        Send a video summary to Telegram.
        
        Args:
            summary: Formatted video summary
            
        Returns:
            True if message was sent successfully, False otherwise
        """
        return await self.send_message(summary)
    
    async def send_batch_summaries(self, summaries: list) -> int:
        """
        Send multiple summaries to Telegram.
        
        Args:
            summaries: List of formatted summaries
            
        Returns:
            Number of successfully sent messages
        """
        success_count = 0
        
        for summary in summaries:
            if await self.send_summary(summary):
                success_count += 1
        
        logger.info(f"Sent {success_count}/{len(summaries)} summaries to Telegram")
        return success_count
