from typing import List, Dict, Tuple
from abc import ABC, abstractmethod
from dataclasses import dataclass

import lazycommon.content_type as content

from lazysocials.platforms.platform import Platform

@dataclass
class LazySocials:
	platforms: List[Platform]
	
	def publish(self, content: content.Content):
		for platform in self.platforms:
			platform.publish(content)
