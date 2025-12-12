import datetime


def out_of_date(item, days) -> bool:
    dt = item["snippet"]["publishedAt"].replace("Z", "+00:00")
    cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)
    published_at = datetime.datetime.fromisoformat(dt)

    if published_at < cutoff:
        return True
    else:
        return False

def item_to_video(item):
    vidsnippet = item.get("snippet", {})

    video_id = item.get("id", {}).get("videoId")
    url = f"https://www.youtube.com/watch?v={video_id}" if video_id else None

    video = {
        "video_id": video_id,
        "channel": vidsnippet.get("channelTitle"),
        "channel_id": vidsnippet.get("channelId"),
        "title": vidsnippet.get("title"),
        "published_at": vidsnippet.get("publishedAt"),
        "url": url,
        "transcript": None,
        "summary": None
    }
    return video

import re  # Add this import at the top

def escape_markdown(text: str) -> str:
    # Escape special Markdown characters
    escape_chars = r'[\*\_\[\]\(\)\~\`\>\#\+\-\=\|\{\}\.\!]'
    return re.sub(escape_chars, r'\\\g<0>', text)
