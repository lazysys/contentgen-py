from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

import os
from datetime import datetime

import lazycommon.content_type as content

from lazysocials.platforms.platform import Platform

import magic
import mimetypes

from io import BufferedReader

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

	def _publish(self, content: str, medias: List[BufferedReader] = []):
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
		
		mag = magic.Magic()
		for i, media in enumerate(medias):
			if media:
				mime = mag.from_buffer(media)
				ext = mimetypes.guess_extension(mime)
				with open(os.path.join(cwd, f"{i}media.{ext}")) as f:
					chunk_size = 4096
					chunk = media.read(chunk_size)
					if not chunk:
						break
					f.write(chunk)
		mag.close()
		
		return True
	
	def Microblog(self, content: content.Microblog) -> bool:
		return bool(self._publish(content.content, medias = content.images))
	def Thread(self, content: content.Thread) -> bool:
		return bool(self._publish(
				"\n---\n".join([content.content] + 
				[microblog.content for microblog in content.microblogs]), 
				medias = content.images + [image for image in [microblog.images for microblog in content.microblogs]]
			)
		)

	def Article(self, content: content.Article) -> bool:
		return bool(self._publish(content.content))

	def Image(self, content: content.Image) -> bool:
		return bool(self._publish(content.content, medias = [content.image]))
	def Carousel(self, content: content.Carousel) -> bool:
		return bool(self._publish(content.content, medias = [img.image for img in content.images]))

	def Video(self, content: content.Video) -> bool:
		return bool(self._publish(content.content, medias = [content.video]))
