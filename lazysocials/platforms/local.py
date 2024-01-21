from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

import os
from datetime import datetime
import shutil

from lazycommon.content_type import *

from lazysocials.platforms.platform import Platform

@dataclass
class Local(Platform):
	_root: str
	
	@property
	def root(self):
		return self._root
	@root.setter
	def root(self, new):
		self._root = new
		self.__post_init__()

	def __post_init__(self):
		if not os.path.exists(self._root):
			os.makedirs(self._root)

	def _publish(self, content: str, medias: List[str] = []):
		count = 0
		while True:
			cwd = os.path.join(self.root, f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}-{count}")
			if os.path.exists(cwd):
				continue
			else:
				os.makedirs(cwd)
				break

		with open(os.path.join(cwd, "content.txt"), "w") as file:
			file.write(content)
		
		for i, media in enumerate(medias):
			if media:
				shutil.copy(media, os.path.join(cwd, f"{i}{os.path.splitext(media)[1]}"))
		
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
