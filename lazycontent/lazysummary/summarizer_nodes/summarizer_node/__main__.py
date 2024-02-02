from ...summarizer import Summarizer

from lazycommon.content_type import Content
from lazycommon.entry import Entry
from lazycommon.slide import Slide

from typing import Type, List

def summarize(summarizer: Summarizer, type: Type[Content], entries: List[Entry]) -> [{ "name": "slides" , "type": List[Slide] }]:
	return summarizer.summarize(entries, type)

main_callable = summarize
