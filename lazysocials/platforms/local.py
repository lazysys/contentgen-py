from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

import os
import datetime
import shutil

from lazycommon.content_type import *

from lazysocials.platforms.platform import Platform

@dataclass
class Local(Platform):
	_root: str
	
	@property
	def root(self):
		return _root
	@root.setter
	def root(self, new):
		_root = new
		self.__post_init__()

	def __post_init__(self):
		if not os.path.exists(_root):
			os.makedirs(_root)

	def _publish(self, content: str, medias: List[str] = []):
		cwd = os.path.join(root, datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))

		with open(os.path.join(cwd, "content.txt"), "w") as file:
			file.write(content)
		
		for i, media in enumerate(medias):
			shutil.move(media, os.path.join(cwd, f"{i}.{os.path.splitext(media)[1]}"))
		
		return True

	def publish(self, content: Content) -> bool:
		if super().publish(content):
			if isinstance(content, Microblog):
				return bool(self._publish(content.content, medias = content.images))
			elif isinstance(content, Thread):
				return bool(self._publish(
						"\n---\n".join([content.content] + 
						[microblog.content for microblog in content.microblogs]), 
						medias = content.images + [image for image in [microblog.images for microblog in content.microblogs]]
					)
				)
			elif isinstance(content, Article):
				return bool(self._publish(content.content))
			elif isinstance(content, Image):
				return bool(self._publish(content.content, medias = [content.image]))
			elif isinstance(content, Carousel):
				return bool(self._publish(content.content, medias = [img.image for img in content.images]))
			elif isinstance(content, Video):
				return bool(self._publish(content.content, medias = [content.video]))
			else:
				return False
