# Docker Deployment Guide

This guide explains how to run the YouTube Summariser application using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose (optional, but recommended)
- API keys configured (YouTube, OpenAI, Telegram)

## Quick Start with Docker Compose

1. **Create environment file**

   Copy the example environment file and configure your API keys:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your credentials:
   ```
   YOUTUBE_API_KEY=your_youtube_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   TELEGRAM_CHAT_ID=your_telegram_chat_id_here
   ```

2. **Build and run the container**

   ```bash
   docker-compose up -d
   ```

   This will:
   - Build the Docker image
   - Create a container named `youtube-summariser`
   - Mount the `data/` directory to persist video information
   - Run the application

3. **View logs**

   ```bash
   docker-compose logs -f
   ```

4. **Stop the container**

   ```bash
   docker-compose down
   ```

## Manual Docker Commands

If you prefer not to use Docker Compose:

1. **Build the image**

   ```bash
   docker build -t youtube-summariser .
   ```

2. **Run the container**

   ```bash
   docker run -d \
     --name youtube-summariser \
     --env-file .env \
     -v $(pwd)/data:/app/data \
     youtube-summariser
   ```

3. **View logs**

   ```bash
   docker logs -f youtube-summariser
   ```

4. **Stop and remove the container**

   ```bash
   docker stop youtube-summariser
   docker rm youtube-summariser
   ```

## Running on a Schedule

### Option 1: GitHub Actions (Recommended)

The repository includes a GitHub Actions workflow that runs the summariser daily at 9:00 AM UTC.

**Setup:**

1. Go to your repository Settings → Secrets and variables → Actions
2. Add the following secrets:
   - `YOUTUBE_API_KEY`
   - `OPENAI_API_KEY`
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`

3. The workflow will run automatically every day at 9:00 AM UTC
4. You can also trigger it manually from the Actions tab

**Workflow file:** `.github/workflows/daily-summariser.yml`

### Option 2: Docker with Cron (Linux/Mac)

To run the Docker container on a schedule using cron:

1. Create a shell script `run-summariser.sh`:

   ```bash
   #!/bin/bash
   cd /path/to/summariser
   docker-compose run --rm summariser
   ```

2. Make it executable:

   ```bash
   chmod +x run-summariser.sh
   ```

3. Add to crontab:

   ```bash
   crontab -e
   ```

   Add this line to run daily at 9 AM:
   ```
   0 9 * * * /path/to/run-summariser.sh >> /var/log/summariser.log 2>&1
   ```

### Option 3: Windows Task Scheduler

1. Create a batch file `run-summariser.bat`:

   ```batch
   @echo off
   cd C:\path\to\summariser
   docker-compose run --rm summariser
   ```

2. Open Task Scheduler and create a new task:
   - Trigger: Daily at 9:00 AM
   - Action: Start a program → `run-summariser.bat`

## Data Persistence

The `data/` directory is mounted as a volume to persist video information across container restarts. This directory contains JSON files with:
- Video metadata
- Transcripts
- Generated summaries

## Troubleshooting

### Container fails to start
- Check if all environment variables are set in `.env`
- Verify API keys are valid
- Check logs: `docker-compose logs`

### Permission issues with data directory
```bash
mkdir -p data
chmod 777 data
```

### Container runs but no output
- The application may take time to process videos
- Check if there are new videos from the configured channels
- View logs for detailed output

## Configuration

To customize which channels are processed:

1. Edit `lang_agent.py` (main block at the bottom)
2. Uncomment/add channels you want to monitor
3. Rebuild the Docker image: `docker-compose build`

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
