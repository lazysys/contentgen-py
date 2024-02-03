from lazysummary.openai import OpenAIChat, OpenAISummarizer
from lazycommon.content.types import Content

from typing import Type

main_callable = OpenAISummarizer

def _OpenAISummarizer(api: OpenAIChat, *types: Type[Content]) -> [{"name": "summarizer", "type": OpenAISummarizer}]:
	pass

signature_callable = _OpenAISummarizer
