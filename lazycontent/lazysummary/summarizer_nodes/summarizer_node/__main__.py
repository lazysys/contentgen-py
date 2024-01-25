from ...summarizer import Summarizer

from lazycommon.content_type import Content
from lazycommon.entry import Entry

from typing import Type, List

def summarize(summarizer: Summarizer, type: Type[Content], entries: List[Entry]) -> [{ "name": "summarized_blocks" , "type": List[str] }]:
	return summarizer.summarize(entries, type)

main_callable = summarize
