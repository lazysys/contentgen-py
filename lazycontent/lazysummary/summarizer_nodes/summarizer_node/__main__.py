from ...summarizer import Summarizer

from lazycommon.content.types import Content
from lazycommon.entry import Entry
from lazycommon.slide import Slide

from typing import Type, List

def summarize(summarizer: Summarizer, typ: Type[Content], entries: List[Entry]) -> [{ "name": "slides" , "type": List[Slide] }]:
	return summarizer.summarize(entries, typ)

main_callable = summarize
