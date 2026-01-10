# python
import asyncio
import json
import time
from pathlib import Path
import sys
from typing import Dict, Any, Optional, Callable, List

from dotenv import load_dotenv

from ai_summarizer import AISummarizer
from prompt import PromptRegistry
from subtitles import download_subtitles
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
            v["transcript"] = download_subtitles(v['video_id'], lang)

            if v["transcript"] is None:
                print("Cannot fetch transcript")
                self._save_video_to_file(channel_name, v)
                continue

            v["summary"] = self.summarizer.summarize(prompt_cfg.sys_prompt, v["transcript"])

            self.videos.append(v)
            self._save_video_to_file(channel_name, v)
            self._post(channel_name, v["video_id"])

    def _run_for_channel(self, channel_name: str, id: str, lang: List[str] = None):
        prompt_cfg = self.prompts.get(channel_name)
        videos = [self._load_video_from_file(channel_name, id)]
        if lang is None:
            lang = ['ru', 'uk']

        for v in videos:
            if v["transcript"] is None:
                v["transcript"] = download_subtitles(v['video_id'], lang)

            if v["transcript"] is None:
                print("Cannot fetch transcript")
                self._save_video_to_file(channel_name, v)
                continue

            v["summary"] = self.summarizer.summarize(prompt_cfg.sys_prompt, v["transcript"])

            self.videos.append(v)
            self._save_video_to_file(channel_name, v)
            self._post(channel_name, id)

    def _post(self, channel_name, id):
        v = self._load_video_from_file(channel_name, id)
        msg = self.notifier.message_template(channel_name, v["url"], v["summary"])
        sent = False
        retry = 5
        while not sent and retry > 0:
            retry -= 1
            sent = asyncio.run(self.notifier.send_message(msg, parse_mode="MarkdownV2"))
        time.sleep(10)

    def _load_video_from_file(self, channel_name:str, video_id: str) -> Dict[str, Any]:
        with open(f"data/{channel_name}_{video_id}.json", "r", encoding="utf-8") as f:
            return json.load(f)
    def _save_video_to_file(self, channel_name:str, v: Dict[str, Any]):
        with open(f"data/{channel_name}_{v["video_id"]}.json", "w", encoding="utf-8") as f:
            json.dump(v, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        channel_names = [
                            'AnnaVanDensky',
                            'SLubarsky',
                            'LEHIST_UA',
                            'Global_Capital',
                            'katarsis_ua',
                            'Dikiylive',
                            'ALPHAMEDIACHANNEL',
                            'vvlashchenko',
                            'OlegZhdanov',
                            'AlexGoncharenko',
                            'BelkovskiyS',
                            'FeyginLive',
                            'OLEG_STARIKOV'
                        ]
    else:
        channel_names = sys.argv[1].split(',')

    agent = LangAgent()
    for ch in channel_names:
         agent.run_for_channel(channel_name=ch, max_results=10, days=3, lang=['ru', 'uk'])
