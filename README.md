# YouTube Video Summariser Agent

An AI-powered agent that monitors YouTube channels, extracts video transcripts, generates summaries using OpenAI's GPT, and sends notifications via Telegram.

## Features

- 📺 **YouTube Channel Monitoring**: Automatically checks multiple YouTube channels for recent videos
- 📝 **Transcript Extraction**: Retrieves video transcripts using YouTube's transcript API
- 🤖 **AI Summarization**: Generates concise summaries using OpenAI's GPT models
- 💬 **Telegram Notifications**: Sends formatted summaries directly to your Telegram chat

## Requirements

- Python 3.8 or higher
- YouTube Data API v3 key
- OpenAI API key
- Telegram Bot token and chat ID

## Installation

1. Clone the repository:
```bash
git clone https://github.com/annapoltavets/summariser.git
cd summariser
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy the example environment file and configure it:
```bash
cp .env.example .env
```

5. Edit `.env` and add your API keys and configuration:
   - **YOUTUBE_API_KEY**: Get from [Google Cloud Console](https://console.cloud.google.com/)
   - **OPENAI_API_KEY**: Get from [OpenAI Platform](https://platform.openai.com/)
   - **TELEGRAM_BOT_TOKEN**: Create a bot via [@BotFather](https://t.me/botfather)
   - **TELEGRAM_CHAT_ID**: Your Telegram chat ID (use [@userinfobot](https://t.me/userinfobot))
   - **YOUTUBE_CHANNEL_IDS**: Comma-separated list of YouTube channel IDs

## Configuration

### Getting YouTube Channel IDs

1. Go to a YouTube channel
2. Click on the channel name
3. The channel ID is in the URL: `https://www.youtube.com/channel/CHANNEL_ID_HERE`

### Setting up Telegram Bot

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot` and follow the instructions
3. Copy the bot token provided
4. Get your chat ID by messaging [@userinfobot](https://t.me/userinfobot)

## Usage

Run the agent:
```bash
python agent.py
```

The agent will:
1. Fetch recent videos from configured YouTube channels
2. Extract transcripts from available videos
3. Generate AI summaries for each video
4. Send formatted summaries to your Telegram chat

## Project Structure

```
summariser/
├── agent.py                 # Main agent script
├── youtube_monitor.py       # YouTube API integration
├── ai_summarizer.py         # OpenAI summarization
├── telegram_notifier.py     # Telegram bot integration
├── requirements.txt         # Python dependencies
├── .env.example            # Example environment configuration
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Example Output

The agent sends messages to Telegram in the following format:

```
📹 *Video Title Here*

This is a concise summary of the video content, highlighting 
the main points and key takeaways from the transcript.

🔗 [Watch Video](https://www.youtube.com/watch?v=VIDEO_ID)
```

## Logging

The agent logs all activities to:
- Console (stdout)
- `summariser.log` file

## Troubleshooting

### No transcripts available
Some videos don't have transcripts available. The agent will skip these videos automatically.

### API Rate Limits
- YouTube Data API: 10,000 quota units per day
- OpenAI API: Depends on your plan
- Telegram Bot API: 30 messages per second

### Configuration Issues
Make sure all required environment variables are set in your `.env` file. The agent will exit with an error message if any are missing.

## Scheduling

To run the agent periodically, you can use:

### Linux/Mac (cron)
```bash
# Run every day at 9 AM
0 9 * * * cd /path/to/summariser && /path/to/venv/bin/python agent.py
```

### Windows (Task Scheduler)
Create a scheduled task that runs `python agent.py` at your desired interval.

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.