"""
Telegram Notifier Module

This module handles sending messages to Telegram.
"""
import asyncio
import logging
import os

from dotenv import load_dotenv
from telegram import Bot
from telegram.constants import ParseMode
from typing import Optional

logger = logging.getLogger(__name__)
load_dotenv()


class TelegramNotifier:
    """Sends notifications to Telegram."""
    
    def __init__(self):
        """
        Initialize the Telegram notifier.
        
        Args:
            bot_token: Telegram bot token
            chat_id: Telegram chat ID to send messages to
        """
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = '-1003320222030'
        self.bot = Bot(token=self.bot_token)
    
    async def send_message(self, text: str, parse_mode: str = ParseMode.MARKDOWN) -> bool:
        try:
            await self.bot.send_message(chat_id=self.chat_id, text=text, parse_mode=parse_mode)
            logger.info(f"Message sent to Telegram chat {self.chat_id}")
            return True
        except Exception as e:
            logger.error(f"Error sending message to Telegram: {e}")
            return False


if __name__ =='__main__':
    notifier = TelegramNotifier()
    asyncio.run(notifier.send_message("""### Сводный список главных тем и выводов из обсуждений HUGS.FUND"""))