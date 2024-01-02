from typing import List, Dict, Tuple
from abc import ABC, abstractmethod
from dataclasses import dataclass

from lazycommon.content_type import ContentType
from feedreaper.rssfeed import Entry

class Microblog(ABC):
	@abstractmethod
	def publish_microblog(self, content: str, images: List[str]):
		pass

class Thread(ABC):
	@abstractmethod
	def publish_thread(self, content: [str], images: List[List[str]]):
		pass

@dataclass
class LazySocials:
	platforms: List
	
	def publish(self, content: Tuple[Entry, Dict[ContentType, List[str]]]):
		for typ in content[1].keys():
			if typ == ContentType.MICROBLOG:
				for platform in self.platforms:
					if isinstance(platform, Microblog):
						platform.publish_microblog("\n".join(content[1][typ]), [content[0].thumbnail])
