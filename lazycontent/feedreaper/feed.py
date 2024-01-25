from dataclasses import dataclass
import feedparser
from datetime import datetime, timedelta
from time import mktime
from typing import List

from lazycontent.lazycommon.entry import Entry

@dataclass
class Feed:
	"""
	Interface to handle a feed.
	
	:param url: The URL to the feed.
	"""

	url: str

	@property
	def entries(self) -> List[Entry]:
		"""
		Collects every target entry.
		Currently a one-week range is hard-coded, will make it so you can set other filters.


		:return: A list with every entry that matches the given filter.
		"""

		entries = []
		feed = feedparser.parse(self.url)
		for entry in feed.entries:
			if datetime.fromtimestamp(mktime(entry.updated_parsed)) > datetime.now() - timedelta(weeks=1): # TODO: custom filters
				entries.append(Entry(entry))
		return entries
