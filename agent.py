#!/usr/bin/env python3
"""
YouTube Video Summarizer Agent

This agent monitors YouTube channels, extracts video transcripts,
generates AI summaries, and sends them via Telegram.
"""

import os
import sys
import asyncio
import logging
from typing import List
from dotenv import load_dotenv

from youtube_monitor import YouTubeMonitor
from ai_summarizer import AISummarizer
from telegram_notifier import TelegramNotifier


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('summariser.log')
    ]
)

logger = logging.getLogger(__name__)


class YouTubeSummarizerAgent:
    """Main agent that coordinates the summarization workflow."""
    
    def __init__(self):
        """Initialize the agent with configuration from environment variables."""
        load_dotenv()
        
        # Load configuration
        self.youtube_api_key = os.getenv('YOUTUBE_API_KEY')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.channel_ids = os.getenv('YOUTUBE_CHANNEL_IDS', '').split(',')
        self.max_videos = int(os.getenv('MAX_VIDEOS_PER_CHANNEL', '3'))
        
        # Validate configuration
        self._validate_config()
        
        # Initialize components
        self.youtube_monitor = YouTubeMonitor(self.youtube_api_key)
        self.ai_summarizer = AISummarizer(self.openai_api_key)
        self.telegram_notifier = TelegramNotifier(self.telegram_bot_token, self.telegram_chat_id)
        
        logger.info("YouTubeSummarizerAgent initialized successfully")
    
    def _validate_config(self):
        """Validate that all required configuration is present."""
        missing = []
        
        if not self.youtube_api_key:
            missing.append('YOUTUBE_API_KEY')
        if not self.openai_api_key:
            missing.append('OPENAI_API_KEY')
        if not self.telegram_bot_token:
            missing.append('TELEGRAM_BOT_TOKEN')
        if not self.telegram_chat_id:
            missing.append('TELEGRAM_CHAT_ID')
        if not self.channel_ids or self.channel_ids == ['']:
            missing.append('YOUTUBE_CHANNEL_IDS')
        
        if missing:
            logger.error(f"Missing required environment variables: {', '.join(missing)}")
            logger.error("Please check your .env file and ensure all required variables are set.")
            sys.exit(1)
    
    async def run(self):
        """Execute the main agent workflow."""
        logger.info("Starting YouTube Summarizer Agent")
        logger.info(f"Monitoring {len(self.channel_ids)} channels")
        
        try:
            # Step 1: Fetch videos with transcripts
            logger.info("Fetching recent videos from YouTube channels...")
            videos = self.youtube_monitor.get_videos_with_transcripts(
                self.channel_ids,
                self.max_videos
            )
            
            if not videos:
                logger.warning("No videos with transcripts found")
                return
            
            logger.info(f"Found {len(videos)} videos with transcripts")
            
            # Step 2: Generate summaries
            logger.info("Generating AI summaries...")
            summaries = []
            
            for video in videos:
                logger.info(f"Summarizing: {video['title']}")
                summary = self.ai_summarizer.summarize_video(video)
                
                if summary:
                    summaries.append(summary)
            
            logger.info(f"Generated {len(summaries)} summaries")
            
            if not summaries:
                logger.warning("No summaries generated")
                return
            
            # Step 3: Send summaries to Telegram
            logger.info("Sending summaries to Telegram...")
            success_count = await self.telegram_notifier.send_batch_summaries(summaries)
            
            logger.info(f"Agent completed successfully. Sent {success_count}/{len(summaries)} summaries")
            
        except Exception as e:
            logger.error(f"Error in agent workflow: {e}", exc_info=True)
            raise


async def main():
    """Main entry point for the agent."""
    try:
        agent = YouTubeSummarizerAgent()
        await agent.run()
    except KeyboardInterrupt:
        logger.info("Agent interrupted by user")
    except Exception as e:
        logger.error(f"Agent failed with error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
