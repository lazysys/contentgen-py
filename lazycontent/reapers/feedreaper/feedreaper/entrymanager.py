from dataclasses import dataclass
import random
import requests
import tempfile
import opengraph_py3

from .feed import Feed
from .storage import Storage
from typing import *

from lazycommon.entry import Entry

@dataclass
class EntryManager:
	"""
	Iterator to get a random entry from the stored feeds.
	Doesn't allow a single entry to be returned more than once according to the used storage and the entry's ID.
	
	:param used_path: The file that holds the used entries' ID.
	:param storage: A generic interface to handle loading wanted feed URLs.
	"""

	used_path: str
	storage: Storage

	def __iter__(self):
		return self	
	def __next__(self) -> Entry:
		return self._pick_random_unused_entry()

	@property
	def _entries(self) -> List[Entry]:
		"""
		Aggregate all target entries into a list.

		:return: A list composed of the target entries.
		"""
		entries = []
		for url in self.storage.urls:
			entries += Feed(url).entries
		return entries

	def _pick_random_unused_entry(self) -> Entry:
		entries = self._entries
		entry = None
		count = 0
		while True:
			entry = random.choice(entries)
			if self._is_entry_used(entry) or not(entry.get("title", False) and entry.get("content", False)):
				count += 1
				entry = None
				if count == len(entries):
					break
				else:
					continue
			self._set_entry_used(entry)
			break
		return entry
	def _is_entry_used(self, entry: Entry) -> bool: # TODO: abstract used entry storage
		 try:
			 with open(self.used_path, "r") as file:
				 return entry.id in file.read().splitlines()
		 except FileNotFoundError:
			 return False
	def _set_entry_used(self, entry: Entry):
		 with open(self.used_path, "a") as file:
			 file.write(f"{entry.id}\n")
