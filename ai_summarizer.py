"""
AI Summarizer Module

This module handles summarizing video transcripts using OpenAI's API.
"""

import os
from typing import Optional
import openai
import logging

from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()

class AISummarizer:
    """Summarizes text using OpenAI's GPT models."""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = model
        self.client = openai.OpenAI(api_key=self.api_key)
    
    def summarize(self, sys_pmt: str, prompt: str) -> Optional[str]:

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": sys_pmt},
                    {"role": "user", "content": prompt[:127000]}
                ],
                temperature=0
            )
            
            summary = response.choices[0].message.content.strip()
            logger.info(f"Generated summary ({len(summary)} chars)")
            return summary
            
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return None