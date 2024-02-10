from lazyllm import LLM
from lazysummary.llm import LLMSummarizer
from lazycommon.content.types import Content

from typing import Type

main_callable = LLMSummarizer

def _LLMSummarizer(llm: LLM, *types: Type[Content]) -> [{"name": "summarizer", "type": LLMSummarizer}]:
	pass

signature_callable = _LLMSummarizer
