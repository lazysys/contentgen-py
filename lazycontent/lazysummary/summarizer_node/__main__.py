from ..summarizer import Summarizer
from ...lazycommon.content_type import Content

from typing import Type, List

def summarize(summarizer: Summarizer, typ: Type[Content], text: str) -> List[str]:
	return summarizer.summarize(text, typ)

main_callable = summarize
