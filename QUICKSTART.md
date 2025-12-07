# Quick Start Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Setup (5 minutes)

### 1. Clone and Install

```bash
git clone https://github.com/annapoltavets/summariser.git
cd summariser
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Get API Keys

#### YouTube API Key
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable "YouTube Data API v3"
4. Create credentials → API Key
5. Copy the API key

#### OpenAI API Key
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create new secret key
5. Copy the API key

#### Telegram Bot
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot`
3. Follow prompts to create your bot
4. Copy the bot token

#### Telegram Chat ID
1. Message [@userinfobot](https://t.me/userinfobot)
2. Copy your chat ID

### 3. Configure

```bash
cp .env.example .env
nano .env  # or use any text editor
```

Fill in your API keys and channel IDs:

```bash
YOUTUBE_API_KEY=your_youtube_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here
YOUTUBE_CHANNEL_IDS=UC_x5XG1OV2P6uZZ5FSM9Ttw,UCBJycsmduvYEL83R_U4JriQ
MAX_VIDEOS_PER_CHANNEL=3
```

### 4. Run

```bash
python agent.py
```

## What Happens

1. ✅ Agent validates configuration
2. 🔍 Fetches recent videos from your channels
3. 📝 Gets transcripts for available videos
4. 🤖 Generates AI summaries
5. 💬 Sends summaries to Telegram

## Troubleshooting

### "No module named 'googleapiclient'"
```bash
pip install -r requirements.txt
```

### "Missing required environment variables"
Check your `.env` file has all required values

### "No videos with transcripts found"
Some videos don't have transcripts. Try different channels or wait for new videos

### Telegram messages not arriving
1. Verify bot token is correct
2. Verify chat ID is correct
3. Make sure you've started a chat with your bot

## Next Steps

- Schedule with cron (see README.md)
- Customize summary length in `ai_summarizer.py`
- Add more channels to monitor
- Check logs in `summarizer.log`

## Need Help?

Check the full documentation:
- [README.md](README.md) - Complete documentation
- [ARCHITECTURE.md](ARCHITECTURE.md) - Technical details
- [example_usage.py](example_usage.py) - Code examples
