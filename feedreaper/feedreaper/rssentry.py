from dataclasses import dataclass
import random
import requests
import tempfile
import opengraph_py3
from feedreaper.rssfeed import Entry, RSSFeed
from feedreaper.rssstorage import RSSStorage
from typing import *

@dataclass
class RSSEntryManager:
	"""
	Iterator to get a random RSS entry from the stored feed URLs.
	Doesn't allow a single entry to be returned more than once according to the used storage and the entry's ID.
	
	:param used_path: The file that holds the used entries' ID.
	:param storage: A generic interface to handle loading wanted feed URLs.
	"""

	used_path: str
	storage: RSSStorage

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
			entries += RSSFeed(url).entries
		return entries

	def _pick_random_unused_entry(self) -> Entry:
		entries = self._entries
		entry = None
		count = 0
		while True:
			entry = random.choice(entries)
			if count == len(entries):
				break
			elif self._is_entry_used(entry) or not entry.content:
				count += 1
				continue
			self._set_entry_used(entry)
			break
		return entry
	def _is_entry_used(self, entry: Entry) -> bool:
		 try:
			 with open(self.used_path, "r") as file:
				 return entry.id in file.read().splitlines()
		 except FileNotFoundError:
			 return False
	def _set_entry_used(self, entry: Entry):
		 with open(self.used_path, "a") as file:
			 file.write(f"{entry.id}\n")
