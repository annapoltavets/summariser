"""
YouTube Channel Monitor and Video Summarizer

This module handles fetching recent videos from YouTube channels
and retrieving their transcripts.
"""

import os
from typing import List, Dict, Optional
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import logging

logger = logging.getLogger(__name__)


class YouTubeMonitor:
    """Monitors YouTube channels and extracts video transcripts."""
    
    def __init__(self, api_key: str):
        """
        Initialize the YouTube monitor.
        
        Args:
            api_key: YouTube Data API key
        """
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=api_key)
    
    def get_recent_videos(self, channel_id: str, max_results: int = 3) -> List[Dict]:
        """
        Get recent videos from a YouTube channel.
        
        Args:
            channel_id: YouTube channel ID
            max_results: Maximum number of videos to retrieve
            
        Returns:
            List of video information dictionaries
        """
        try:
            # Get the uploads playlist ID for the channel
            channel_response = self.youtube.channels().list(
                part='contentDetails',
                id=channel_id
            ).execute()
            
            if not channel_response.get('items'):
                logger.warning(f"Channel {channel_id} not found")
                return []
            
            uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            
            # Get recent videos from the uploads playlist
            playlist_response = self.youtube.playlistItems().list(
                part='snippet,contentDetails',
                playlistId=uploads_playlist_id,
                maxResults=max_results
            ).execute()
            
            videos = []
            for item in playlist_response.get('items', []):
                video_id = item['contentDetails']['videoId']
                video_title = item['snippet']['title']
                published_at = item['snippet']['publishedAt']
                
                videos.append({
                    'video_id': video_id,
                    'title': video_title,
                    'published_at': published_at,
                    'channel_id': channel_id
                })
            
            logger.info(f"Found {len(videos)} videos for channel {channel_id}")
            return videos
            
        except Exception as e:
            logger.error(f"Error fetching videos for channel {channel_id}: {e}")
            return []
    
    def get_video_transcript(self, video_id: str) -> Optional[str]:
        """
        Get the transcript of a YouTube video.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Video transcript as a single string, or None if unavailable
        """
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            transcript = ' '.join([entry['text'] for entry in transcript_list])
            logger.info(f"Retrieved transcript for video {video_id} ({len(transcript)} chars)")
            return transcript
        except Exception as e:
            logger.warning(f"Could not retrieve transcript for video {video_id}: {e}")
            return None
    
    def get_videos_with_transcripts(self, channel_ids: List[str], max_videos_per_channel: int = 3) -> List[Dict]:
        """
        Get recent videos with transcripts from multiple channels.
        
        Args:
            channel_ids: List of YouTube channel IDs
            max_videos_per_channel: Maximum number of videos per channel
            
        Returns:
            List of videos with transcripts
        """
        all_videos = []
        
        for channel_id in channel_ids:
            videos = self.get_recent_videos(channel_id, max_videos_per_channel)
            
            for video in videos:
                transcript = self.get_video_transcript(video['video_id'])
                if transcript:
                    video['transcript'] = transcript
                    all_videos.append(video)
        
        logger.info(f"Total videos with transcripts: {len(all_videos)}")
        return all_videos
