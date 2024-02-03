from typing import List, Type

from lazycommon.content.types import Content
from lazycommon.entry import Entry
from lazycommon.slide import Slide
from lazycommon.runner import Runner

class Summarizer(Runner[Content, List[Slide]]):
	def summarize(self, entries: List[Entry], into: Content) -> List[Slide]:
		self.run(into, entries)

