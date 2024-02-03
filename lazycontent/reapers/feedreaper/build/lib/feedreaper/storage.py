from dataclasses import dataclass
from typing import *
from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET

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

class Storage(ABC):
	"""
	Interface to handle the storage of feeds.
	"""

	@property
	@abstractmethod
	def urls(self) -> List[str]:
		"""
		Collects all feed URLs.

		:return: A list of feed URLS.
		"""

		pass

@dataclass
class OPML(Storage):
	"""
	Class that implements the [Storage] interface and uses an OPML file.
	Many readers export into this format, so it's convenient to use.
	
	:param path: Path to the OPML file.
	"""

	path: str

	@property
	def urls(self) -> List[str]:
		tree = ET.parse(self.path)
		root = tree.getroot()
		feed_urls = []
		for outline in root.iter('outline'):
			if 'xmlUrl' in outline.attrib:
				feed_urls.append(outline.attrib['xmlUrl'])
		return feed_urls

@dataclass
class File(Storage):
	"""
	Class that implements the [Storage] interface and uses a normal text file.
	As every line contains a feed URL, it's quite easy to write/parse.
	
	:param path: Path to the text file.
	"""

	path: str

	@property
	def urls(self) -> List[str]:
		 with open(self.path, 'r') as file:
			 feed_urls = [line.strip() for line in file]
			 return feed_urls
