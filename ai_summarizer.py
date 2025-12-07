"""
AI Summarizer Module

This module handles summarizing video transcripts using OpenAI's API.
"""

import os
from typing import Optional
import openai
import logging

logger = logging.getLogger(__name__)


class AISummarizer:
    """Summarizes text using OpenAI's GPT models."""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        """
        Initialize the AI summarizer.
        
        Args:
            api_key: OpenAI API key
            model: OpenAI model to use for summarization
        """
        self.api_key = api_key
        self.model = model
        self.client = openai.OpenAI(api_key=api_key)
    
    def summarize(self, text: str, max_length: int = 500) -> Optional[str]:
        """
        Summarize a text using OpenAI's API.
        
        Args:
            text: Text to summarize
            max_length: Maximum length of summary in words
            
        Returns:
            Summary of the text, or None if summarization fails
        """
        try:
            # Truncate text if it's too long (approximately 4 chars per token)
            max_chars = 12000  # Leave room for prompt and response
            if len(text) > max_chars:
                text = text[:max_chars] + "..."
                logger.info(f"Truncated text to {max_chars} characters")
            
            prompt = f"""Please provide a concise summary of the following video transcript. 
The summary should be no more than {max_length} words and should capture the main points and key takeaways.

Transcript:
{text}

Summary:"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that creates concise and informative summaries of video transcripts."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            summary = response.choices[0].message.content.strip()
            logger.info(f"Generated summary ({len(summary)} chars)")
            return summary
            
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return None
    
    def summarize_video(self, video_info: dict) -> Optional[str]:
        """
        Summarize a video and format the result with video details.
        
        Args:
            video_info: Dictionary containing video information and transcript
            
        Returns:
            Formatted summary with video details
        """
        if 'transcript' not in video_info:
            logger.warning(f"No transcript found for video {video_info.get('video_id')}")
            return None
        
        summary = self.summarize(video_info['transcript'])
        
        if summary:
            video_url = f"https://www.youtube.com/watch?v={video_info['video_id']}"
            formatted_summary = f"""📹 *{video_info['title']}*

{summary}

🔗 [Watch Video]({video_url})
"""
            return formatted_summary
        
        return None
