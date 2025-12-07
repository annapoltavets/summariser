#!/usr/bin/env python3
"""
Example usage script for the YouTube Summarizer Agent.

This script demonstrates how to use the agent programmatically.
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Example: Direct usage of individual components
async def example_direct_usage():
    """Example of using individual components directly."""
    from youtube_monitor import YouTubeMonitor
    from ai_summarizer import AISummarizer
    from telegram_notifier import TelegramNotifier
    
    # Initialize components
    youtube = YouTubeMonitor(os.getenv('YOUTUBE_API_KEY'))
    summarizer = AISummarizer(os.getenv('OPENAI_API_KEY'))
    telegram = TelegramNotifier(
        os.getenv('TELEGRAM_BOT_TOKEN'),
        os.getenv('TELEGRAM_CHAT_ID')
    )
    
    # Get videos from a specific channel
    channel_id = "UC_x5XG1OV2P6uZZ5FSM9Ttw"  # Example channel ID
    videos = youtube.get_recent_videos(channel_id, max_results=1)
    
    # Process first video
    if videos:
        video = videos[0]
        print(f"Processing video: {video['title']}")
        
        # Get transcript
        transcript = youtube.get_video_transcript(video['video_id'])
        
        if transcript:
            video['transcript'] = transcript
            
            # Generate summary
            summary = summarizer.summarize_video(video)
            
            if summary:
                print(f"Summary generated:\n{summary}")
                
                # Send to Telegram
                success = await telegram.send_summary(summary)
                print(f"Telegram message sent: {success}")


# Example: Using the main agent
async def example_agent_usage():
    """Example of using the main agent."""
    from agent import YouTubeSummarizerAgent
    
    agent = YouTubeSummarizerAgent()
    await agent.run()


if __name__ == '__main__':
    # Uncomment the example you want to run:
    
    # Run the full agent
    asyncio.run(example_agent_usage())
    
    # Or run direct component usage
    # asyncio.run(example_direct_usage())
