from dataclasses import dataclass
from typing import *
from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET

class RSSStorage(ABC):
	"""
	Interface to handle the storage of feed URLS.
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
class OPML(RSSStorage):
	"""
	Class that implements the [RSSStorage] interface and uses an OPML file.
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
class RSSFile(RSSStorage):
	"""
	Class that implements the [RSSStorage] interface and uses a normal text file.
	As every line contains a feed URL, it's quite easy to write/parse.
	
	:param path: Path to the text file.
	"""

	path: str

	@property
	def urls(self) -> List[str]:
		 with open(self.path, 'r') as file:
			 feed_urls = [line.strip() for line in file]
			 return feed_urls
