from typing import List, Dict, Tuple
from abc import ABC, abstractmethod
from dataclasses import dataclass

from lazycommon.content_type import Content

from lazysocials.platforms.platform import Platform

@dataclass
class LazySocials:
	platforms: List[Platform]
	
	def publish(self, content: Content):
		for platform in self.platforms:
			if any(isinstance(content, x) for x in platform.types):
				platform.publish(content)
