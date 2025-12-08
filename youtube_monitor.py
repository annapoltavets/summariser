"""
YouTube Channel Monitor and Video Summarizer

This module handles fetching recent videos from YouTube channels
and retrieving their transcripts.
"""
import asyncio
import datetime
import os
import time
from typing import List, Dict, Optional

from dotenv import load_dotenv
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig
import logging

from ai_summarizer import AISummarizer
from telegram_notifier import TelegramNotifier

logger = logging.getLogger(__name__)
load_dotenv()

class YouTubeFetcher:
    
    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
    
    def resolve_channel_id(self, identifier: str) -> Optional[str]:
        try:
            resp = self.youtube.search().list(part='id', q=identifier, type='channel', maxResults=1).execute()
            items = resp.get('items', [])
            if items:
                channel_id = items[0].get('id', {}).get('channelId')
                if channel_id:
                    return channel_id
        except Exception as e:
            logger.debug(f"search().list(...) failed for '{identifier}': {e}")

        # Could not resolve
        logger.warning(f"Could not resolve channel identifier '{identifier}' to a channel ID")
        return None

    def get_video_transcript(self, video_id: str, lang = 'ru') -> Optional[str]:
        try:
            ytt_api = YouTubeTranscriptApi(
                proxy_config=WebshareProxyConfig(
                    proxy_username=os.getenv("PROXY_USR"),
                    proxy_password=os.getenv("PROXY_PWD"),
                )
            )

            # all requests done by ytt_api will now be proxied through Webshare
            t = ytt_api.fetch(video_id=video_id, languages=[lang])

            return "\n".join([x.text for x in t.snippets])

        except Exception as e:
            logger.warning(f"Could not retrieve transcript for video {video_id}: {e}")
            return None

    def search_channel_videos(self, channel_name: str, max_results: int = 1) -> list[Dict]:
        channel_id = self.resolve_channel_id(channel_name)

        resp = self.youtube.search().list(
            part="snippet",
            channelId=channel_id,
            order="date",
            maxResults=max_results,
            type="video"
        ).execute()

        return resp.get("items", [])
