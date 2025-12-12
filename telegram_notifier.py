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
from telegram.helpers import escape_markdown

from wiki import get_guest_info

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

    def message_template(self, channel_name: str, video_url: str, summary: str) -> str:
        smr = escape_markdown(summary.replace('"', ''), version=2).split("\n")
        url = escape_markdown(video_url, version=2)


        smry = "\n".join([f"{x.strip().strip('\n')}" for x in smr[1:]])
        if ":" in smr[0]:
            guest_name = smr[0].replace("Гость:", "").replace("Гість:", "").strip()
            gs = ""   #get_guest_info(guest_name)
            gs = escape_markdown(gs, version=2)
        else:
            gs = ""

        out = (
                f"*{escape_markdown(channel_name, version=2)}*\n"
                f"{smr[0]}{gs}\n\n"
                f"{smry}\n\n"
                f"{url}"
            )

        print(out)
        return out
    
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