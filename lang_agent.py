# python
import asyncio
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional, Callable, List

from dotenv import load_dotenv

from ai_summarizer import AISummarizer
from prompt import PromptRegistry
from telegram_notifier import TelegramNotifier
from utils import item_to_video, out_of_date
from y_fetcher import FetcherInterface, YoutubeFetcher

load_dotenv()

class LangAgent:

    videos = []

    def __init__(self):
        self.prompts: PromptRegistry = PromptRegistry('configs/prompts.yml')
        self.fetcher: FetcherInterface = YoutubeFetcher()
        self.summarizer = AISummarizer()
        self.notifier = TelegramNotifier()

    def run_for_channel(self, channel_name: str, max_results: int = 3, days: int = 1, lang=None):
        if lang is None:
            lang = ['ru']
        prompt_cfg = self.prompts.get(channel_name)

        items = self.fetcher.fetch_videos(channel_name, max_results=max_results)
        seen_titles = set()
        videos = [
            item_to_video(i)
            for i in items
            if len(i['snippet']['description']) > 0 and not out_of_date(i, days)
               and (video_id := i['snippet']['title']) not in seen_titles and not seen_titles.add(video_id)
        ]

        for v in videos:
            print(f"{channel_name}: Processing video {v['video_id']} - {v['title']}")
            v["transcript"] = self.fetcher.get_video_transcript(v['video_id'], lang)

            if v["transcript"] is None:
                print("Cannot fetch transcript")
                self._save_video_to_file(channel_name, v)
                continue

            v["summary"] = self.summarizer.summarize(prompt_cfg.sys_prompt, v["transcript"])

            self.videos.append(v)
            self._save_video_to_file(channel_name, v)

            msg = self.notifier.message_template(channel_name, v["url"], v["summary"])
            asyncio.run(self.notifier.send_message(msg, parse_mode="MarkdownV2"))
            time.sleep(10)

    def _run_for_channel(self, channel_name: str, id: str, lang: List[str] = None):
        prompt_cfg = self.prompts.get(channel_name)
        videos = [self._load_video_from_file(channel_name, id)]
        if lang is None:
            lang = ['ru', 'uk']

        for v in videos:
            v["transcript"] = self.fetcher.get_video_transcript(v['video_id'], lang)

            if v["transcript"] is None:
                print("Cannot fetch transcript")
                self._save_video_to_file(channel_name, v)
                continue

            v["summary"] = self.summarizer.summarize(prompt_cfg.sys_prompt, v["transcript"])

            self.videos.append(v)
            self._save_video_to_file(channel_name, v)

            msg = self.notifier.message_template(channel_name, v["url"], v["summary"])
            loop = asyncio.get_event_loop()
            loop.run_until_complete(
                self.notifier.send_message(msg, parse_mode="MarkdownV2")
            )
            time.sleep(10)


    def _load_video_from_file(self, channel_name:str, video_id: str) -> Dict[str, Any]:
        with open(f"data/{channel_name}_{video_id}.json", "r", encoding="utf-8") as f:
            return json.load(f)
    def _save_video_to_file(self, channel_name:str, v: Dict[str, Any]):
        with open(f"data/{channel_name}_{v["video_id"]}.json", "w", encoding="utf-8") as f:
            json.dump(v, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':

    agent = LangAgent()
    agent.run_for_channel(channel_name='AnnaVanDensky', max_results=7, days=1)
    # agent.run_for_channel(channel_name='SLubarsky', max_results=7, days=1)
    # agent.run_for_channel(channel_name='LEHIST_UA', max_results=2, days=1)
    # agent.run_for_channel(channel_name='Global_Capital', max_results=10, days=1)
    # agent.run_for_channel(channel_name='HUGSFUND', max_results=10, days=1)
    # agent.run_for_channel(channel_name='katarsis_ua', max_results=10, days=1)
    # agent.run_for_channel(channel_name='Dikiylive', max_results=10, days=1, lang=['ru', 'uk'])
    # agent.run_for_channel(channel_name='vvlashchenko', max_results=10, days=1)
    # agent.run_for_channel(channel_name='OlegZhdanov', max_results=10, days=1)
    # agent.run_for_channel(channel_name='AlexGoncharenko', max_results=10, days=1, lang=['uk'])

    # agent.run_for_channel(channel_name='PolitekaOnline', max_results=10, days=1)
    # agent.run_for_channel(channel_name='nemyrialive', max_results=10, days=1, lang=['ru', 'uk'])
    # agent.run_for_channel(channel_name='YuriyRomanenko_Ukraine', max_results=10, days=1, lang=['ru', 'uk'])
