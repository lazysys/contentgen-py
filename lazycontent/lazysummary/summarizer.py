from abc import ABC, abstractmethod
from typing import List

from ..lazycommon.content_type import Content
from ..lazycommon.entry import Entry

class Summarizer(ABC):
	"""
	A generic interface for a summarizer.
	"""
	@abstractmethod
	def summarize(self, entries: List[Entry], into: Content) -> List[str]:
		"""
		This function takes list of entries, which will be converted into the specified content type's needed text.

		:return: A list of text segments.
		"""

		pass

