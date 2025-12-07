"""
Unit tests for the YouTube Summarizer Agent modules.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from youtube_monitor import YouTubeMonitor
from ai_summarizer import AISummarizer
from telegram_notifier import TelegramNotifier


class TestYouTubeMonitor(unittest.TestCase):
    """Test cases for YouTubeMonitor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.api_key = "test_api_key"
        self.monitor = YouTubeMonitor(self.api_key)
    
    def test_initialization(self):
        """Test YouTubeMonitor initialization."""
        self.assertEqual(self.monitor.api_key, self.api_key)
        self.assertIsNotNone(self.monitor.youtube)
    
    @patch('youtube_monitor.YouTubeTranscriptApi')
    def test_get_video_transcript_success(self, mock_transcript_api):
        """Test successful transcript retrieval."""
        mock_transcript_api.get_transcript.return_value = [
            {'text': 'Hello', 'start': 0.0, 'duration': 1.0},
            {'text': 'World', 'start': 1.0, 'duration': 1.0}
        ]
        
        result = self.monitor.get_video_transcript('test_video_id')
        
        self.assertEqual(result, 'Hello World')
        mock_transcript_api.get_transcript.assert_called_once_with('test_video_id')
    
    @patch('youtube_monitor.YouTubeTranscriptApi')
    def test_get_video_transcript_failure(self, mock_transcript_api):
        """Test transcript retrieval failure."""
        mock_transcript_api.get_transcript.side_effect = Exception('API Error')
        
        result = self.monitor.get_video_transcript('test_video_id')
        
        self.assertIsNone(result)


class TestAISummarizer(unittest.TestCase):
    """Test cases for AISummarizer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.api_key = "test_openai_key"
        self.summarizer = AISummarizer(self.api_key)
    
    def test_initialization(self):
        """Test AISummarizer initialization."""
        self.assertEqual(self.summarizer.api_key, self.api_key)
        self.assertEqual(self.summarizer.model, "gpt-3.5-turbo")
    
    def test_text_truncation(self):
        """Test that long text is truncated."""
        long_text = "a" * 15000
        
        # The summarize method should handle truncation internally
        with patch.object(self.summarizer.client.chat.completions, 'create') as mock_create:
            mock_create.return_value = Mock(
                choices=[Mock(message=Mock(content="Test summary"))]
            )
            
            result = self.summarizer.summarize(long_text)
            
            # Verify the API was called
            self.assertTrue(mock_create.called)
            # Get the actual prompt that was sent
            call_args = mock_create.call_args[1]
            prompt = call_args['messages'][1]['content']
            # The prompt should contain truncated text
            self.assertIn("...", prompt)
    
    def test_summarize_video_without_transcript(self):
        """Test video summarization without transcript."""
        video_info = {
            'video_id': 'test_id',
            'title': 'Test Video'
        }
        
        result = self.summarizer.summarize_video(video_info)
        
        self.assertIsNone(result)
    
    def test_summarize_video_formats_output(self):
        """Test that video summary is properly formatted."""
        video_info = {
            'video_id': 'test_id',
            'title': 'Test Video',
            'transcript': 'This is a test transcript.'
        }
        
        with patch.object(self.summarizer.client.chat.completions, 'create') as mock_create:
            mock_create.return_value = Mock(
                choices=[Mock(message=Mock(content="This is a summary."))]
            )
            
            result = self.summarizer.summarize_video(video_info)
            
            self.assertIsNotNone(result)
            self.assertIn('Test Video', result)
            self.assertIn('This is a summary.', result)
            self.assertIn('https://www.youtube.com/watch?v=test_id', result)


class TestTelegramNotifier(unittest.TestCase):
    """Test cases for TelegramNotifier class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.bot_token = "test_bot_token"
        self.chat_id = "test_chat_id"
        self.notifier = TelegramNotifier(self.bot_token, self.chat_id)
    
    def test_initialization(self):
        """Test TelegramNotifier initialization."""
        self.assertEqual(self.notifier.bot_token, self.bot_token)
        self.assertEqual(self.notifier.chat_id, self.chat_id)
        self.assertIsNotNone(self.notifier.bot)


class TestEnvironmentValidation(unittest.TestCase):
    """Test cases for environment configuration validation."""
    
    @patch.dict(os.environ, {}, clear=True)
    def test_missing_environment_variables(self):
        """Test that missing environment variables are detected."""
        from agent import YouTubeSummarizerAgent
        
        with self.assertRaises(SystemExit):
            YouTubeSummarizerAgent()
    
    @patch.dict(os.environ, {
        'YOUTUBE_API_KEY': 'test_yt_key',
        'OPENAI_API_KEY': 'test_openai_key',
        'TELEGRAM_BOT_TOKEN': 'test_bot_token',
        'TELEGRAM_CHAT_ID': 'test_chat_id',
        'YOUTUBE_CHANNEL_IDS': 'channel1,channel2'
    })
    def test_valid_environment_variables(self):
        """Test that valid environment variables are accepted."""
        from agent import YouTubeSummarizerAgent
        
        # Should not raise an exception
        agent = YouTubeSummarizerAgent()
        self.assertIsNotNone(agent)
        self.assertEqual(len(agent.channel_ids), 2)


if __name__ == '__main__':
    unittest.main()
