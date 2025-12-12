# python
from dataclasses import dataclass
from typing import Dict
import yaml



@dataclass
class PromptConfig:
    channel: str
    sys_prompt: str



class PromptRegistry:
    def __init__(self, yaml_file: str):
        self._registry: Dict[str, PromptConfig] = {}
        with open(yaml_file, 'r') as f:
            data = yaml.safe_load(f)
        for channel, prompt in data.items():
            self._registry[channel.lower()] = PromptConfig(channel, prompt)

    def register(self, channel: str, template: str) -> None:
        self._registry[channel.lower()] = PromptConfig(channel=channel, sys_prompt=template)

    def get(self, channel: str) -> PromptConfig:
        return self._registry.get(channel.lower())
