from dataclasses import dataclass
from typing import List, Dict, Tuple

from .storage import OPML, File, StorageConfig
from .entrymanager import EntryManager

from ..lazycommon.entry import Entry

@dataclass
class FeedReaper:
	"""
	Main and user-facing class to use FeedReaper. 
	Can be used as an iterator.
	
	:param storage_conf: The configuration which points to the storage files.
	"""

	_storage_conf: StorageConfig
	
	def __iter__(self):
		return self
	def __next__(self) -> Entry:
		return next(self._manager)

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
			storage = File(feed_file)
		if storage:
			self._manager = EntryManager(used_file, storage)

	def __post_init__(self):
		self._setup_storage()
