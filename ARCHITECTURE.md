# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    YouTubeSummarizerAgent                    │
│                      (agent.py)                              │
└─────────────┬─────────────────┬─────────────────┬───────────┘
              │                 │                 │
              │                 │                 │
              ▼                 ▼                 ▼
    ┌─────────────────┐ ┌─────────────┐ ┌──────────────────┐
    │ YouTubeMonitor  │ │AISummarizer │ │TelegramNotifier  │
    │youtube_monitor.py│ │ai_summarizer│ │telegram_notifier │
    └────────┬─────────┘ └──────┬──────┘ └────────┬─────────┘
             │                  │                  │
             │                  │                  │
             ▼                  ▼                  ▼
    ┌─────────────────┐ ┌──────────────┐ ┌──────────────┐
    │  YouTube API    │ │  OpenAI API  │ │Telegram API  │
    │  - Get videos   │ │  - GPT model │ │ - Send msg   │
    │  - Transcripts  │ │  - Summarize │ │ - Format     │
    └─────────────────┘ └──────────────┘ └──────────────┘
```

## Data Flow

1. **Initialization**
   - Load configuration from .env file
   - Validate all required API keys and settings
   - Initialize all service clients

2. **Fetch Videos**
   - Query YouTube Data API for recent videos from configured channels
   - Retrieve video metadata (title, ID, publish date)
   - Extract transcripts using youtube-transcript-api

3. **Generate Summaries**
   - Send each transcript to OpenAI GPT
   - Generate concise summaries (max 500 words)
   - Format output with video title and link

4. **Send Notifications**
   - Deliver formatted summaries to Telegram
   - Use Markdown formatting for rich display
   - Track success/failure for each message

## Configuration

All configuration is managed through environment variables:

| Variable | Purpose | Required |
|----------|---------|----------|
| YOUTUBE_API_KEY | YouTube Data API access | Yes |
| OPENAI_API_KEY | OpenAI API access | Yes |
| TELEGRAM_BOT_TOKEN | Telegram bot authentication | Yes |
| TELEGRAM_CHAT_ID | Target chat for messages | Yes |
| YOUTUBE_CHANNEL_IDS | Channels to monitor (comma-separated) | Yes |
| MAX_VIDEOS_PER_CHANNEL | Limit videos per channel | No (default: 3) |

## Error Handling

Each module includes comprehensive error handling:

- **YouTube errors**: Logged and skipped (continues with other videos)
- **Transcript errors**: Logged and skipped (video without transcript ignored)
- **OpenAI errors**: Logged and skipped (continues with other videos)
- **Telegram errors**: Logged and counted (tracks delivery success rate)
- **Configuration errors**: Agent exits immediately with clear error message

## Logging

All operations are logged to:
- Console (stdout) - Real-time monitoring
- `summarizer.log` file - Persistent record

Log levels used:
- INFO: Normal operations and progress
- WARNING: Non-critical issues (e.g., missing transcripts)
- ERROR: Critical failures requiring attention

## Extension Points

The modular design allows easy extension:

1. **Add new video sources**: Create new monitor modules
2. **Add new summarization engines**: Swap AISummarizer implementation
3. **Add new notification channels**: Create new notifier modules
4. **Add storage**: Insert database layer before/after summarization
5. **Add scheduling**: Wrap agent in cron job or scheduler service
