from dataclasses import dataclass
from typing import List, Dict, Tuple

from feedreaper.rssstorage import OPML, RSSFile
from feedreaper.rssfeed import Entry
from feedreaper.rssentry import RSSEntryManager
from feedreaper.summarizer import OpenAIChat, OpenAISummarizer, ContentType

@dataclass(frozen=True)
class StorageConfig:
	"""
	Holds the configuration for FeedReaper's RSS storage.
	Specifies in which files the feed URLs and the used entry IDs are located.
	
	:param feed_file: The file which stores the feed URLs.
	:param used_file: The file which stores the used entry IDs.
	"""
 	
	feed_file: str = "feeds.opml"
	used_file: str = "used.txt"

@dataclass
class FeedReaper:
	"""
	Main and user-facing class to use FeedReaper. 
	Can be used as an iterator.
	
	:param storage_conf: The configuration which points to the storage files.
	:param openai_key: Currently only OpenAI's chat API is supported for summarization, so this is the API key. In the future you'll have to provide a summarizer class that conforms to a generic interface.
	:param types: The types of Content to spit back. This will be generalized with LazyContent.
	"""

	_storage_conf: StorageConfig
	_openai_key: str # TODO: summarizer instance with generalized interface
	types: List[ContentType] = None # TODO: LazyContent
	
	def __iter__(self):
		return self
	def __next__(self) -> Tuple[Entry, Dict[ContentType, List[str]]]:
		types = self.types
		if not types:
			types = [el.value for el in ContentType]

		content = {}
		entry = next(self._manager)
		for typ in types:
			content[typ] = self._summarizer.summarize([entry], typ)
		return (entry, content)

	@property
	def storage_conf(self):
		return self._storage_conf
	@storage_conf.setter
	def storage_conf(self, conf):
		self._storage_conf = conf
		self._setup_storage()
	def _setup_storage(self):
		"""
		Update the storage configuration.
		"""
		feed_file = self._storage_conf.feed_file or "feeds.opml"
		used_file = self._storage_conf.used_file or "used.txt"
		storage = None
		if "opml" in feed_file:
			storage = OPML(feed_file)
		else:
			storage = RSSFile(feed_file)
		if storage:
			self._manager = RSSEntryManager(used_file, storage)

	@property
	def openai_key(self):
		return self._openai_key
	@storage_conf.setter
	def openai_key(self, key):
		self._openai_key = key
		self._setup_summarizer()
	def _setup_summarizer(self):
		"""
		Update the OpenAI API key.
		"""
		openai = OpenAIChat(self._openai_key)
		self._summarizer = OpenAISummarizer(openai)
	
	def __post_init__(self):
		self._setup_storage()
		self._setup_summarizer()
