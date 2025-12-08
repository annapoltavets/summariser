"""
YouTube Channel Monitor and Video Summarizer

This module handles fetching recent videos from YouTube channels
and retrieving their transcripts.
"""
import asyncio
import datetime
import time
from typing import List, Dict, Optional

from dotenv import load_dotenv
import logging

from ai_summarizer import AISummarizer
from telegram_notifier import TelegramNotifier
from youtube_monitor import YouTubeFetcher

logger = logging.getLogger(__name__)
load_dotenv()


class Agent:
    videos = []

    def __init__(self):

        self.fetcher = YouTubeFetcher()
        self.summarizer = AISummarizer()
        self.notifier = TelegramNotifier()

    def search_channel_videos(self, channel_name: str, max_results: int = 1, days: int = 2, lang: str = 'ru') -> None:
        items = self.fetcher.search_channel_videos(channel_name, max_results)

        for item in items:
            vidsnippet = item.get("snippet", {})
            cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)
            published_at = datetime.datetime.fromisoformat(vidsnippet.get("publishedAt").replace("Z", "+00:00"))
            if published_at < cutoff:
                continue

            video_id = item.get("id", {}).get("videoId")
            print("Found video:", vidsnippet.get("channelTitle"), video_id, vidsnippet.get("title"))

            transcript = self.fetcher.get_video_transcript(video_id, lang)
            if transcript is None:
                continue
            else:
                prompt = f"""Просуммируй мнение(не пиши фразу Ведущие обсуждали...), аргументы и выводы ведущих по вопросу обсуждения в 2-3 тезиса. Поставь смайлик после тезисов
                Обязательно добавь интересные детали обсуждения.
                Стиль изложения должен быть живым, интересным, с элементами юмора. В стиле юмористической репортажной статьи. Можно использовать эмодзи и грубую лексику.
                Затем перечислить Какие события обсуждали в виде списка. 
                События опиши следующим образом:
                Если предметом обсуждения является документ или статья или книга и тп, то приведи краткое содержание документа и укажи авторов. 
                Если предметом обсуждения является встреча, то опиши кто и где встречался, и зачем.
                Если предметом обсуждения является событие, то опиши что случилось, где, когда, и с кем. 
                Текст: {transcript}"""

                summary = self.summarizer.summarize(prompt)
                print(summary)
                print('--' * 20)

                url = f"https://www.youtube.com/watch?v={video_id}"

                self.videos.append({
                    "channel_id": vidsnippet.get("channelId"),
                    "channel_title": vidsnippet.get("channelTitle"),
                    "video_id": video_id,
                    "title": vidsnippet.get("title"),
                    "published_at": vidsnippet.get("publishedAt"),
                    "transcript": transcript,
                    "summary": summary,
                    "url": url
                })

                asyncio.run(self.notifier.send_message(f"{summary}\n{url}"))
                time.sleep(10)

    def summary_of_summaries(self) -> Optional[str]:
        summaries = "\n".join([v['channel_title'] + ": " + v['summary'] for v in self.videos if v.get('summary')])

        total_prompt = f"""Сделай сводный список обсуждений в эфире за прошлый день. 
        Вначале 2-3 предложения о главных темах обсуждений и общие выводы.
        Затем приведи список интересных деталей из обсуждений.
        Обязательно укажи канал, на котором это обсуждалось.
        Добавь смайлик в конце каждого пункта списка.
        Текст:
            {summaries}
            """
        ss = self.summarizer.summarize(total_prompt)
        print('==' * 20)
        print('Summary of summaries:')
        print(ss)
        print('==' * 20)

        asyncio.run(self.notifier.send_message(ss))


if __name__ == '__main__':
    y = Agent()

    # y.search_channel_videos(channel_name='AnnaVanDensky', max_results=2, days=1, lang='ru')
    # y.search_channel_videos(channel_name='PolitekaOnline', max_results=5, days=1, lang='ru')
    # y.search_channel_videos(channel_name='Global_Capital', max_results=5, days=1, lang='ru')
    # y.search_channel_videos(channel_name='YuriyRomanenko_Ukraine', max_results=5, days=1, lang='ru')
    # y.search_channel_videos(channel_name='Dikiylive', max_results=5, days=1, lang='ru')
    # y.search_channel_videos(channel_name='HUGSFUND', max_results=5, days=1, lang='ru')
    # y.search_channel_videos(channel_name='katarsis_ua', max_results=5, days=1, lang='ru')
    # y.search_channel_videos(channel_name='LEHIST_UA', max_results=5, days=1, lang='ru')
    # y.search_channel_videos(channel_name='SLubarsky', max_results=5, days=1, lang='ru')
    y.search_channel_videos(channel_name='vvlashchenko', max_results=5, days=2, lang='ru')
    # y.search_channel_videos(channel_name='nemyrialive', max_results=5, days=2, lang='ru')

    # y.summary_of_summaries()
