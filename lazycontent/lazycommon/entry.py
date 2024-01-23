from typing import List, Dict, Any
from dataclasses import dataclass

import opengraph_py3
import requests
import tempfile

@dataclass
class Entry:
	"""
	Feed entry with convenience features to be used for content creation.
	
	:param entry: FeedParser's entry that is used as a base.
	"""
	entry: Dict
	
	@property
	def thumbnail(self) -> str:
		"""
		Download the thumbnail from the OpenGraph metadata.
		
		:return: The local file path to the thumbnail.
		"""
		
		try:
			return self._download_image(opengraph_py3.OpenGraph(url=self.entry.link).image)
		except AttributeError:
			return None

	@property
	def images(self) -> List[str]: # TODO: implement scraping all images from an entry
		"""
		Download all images that appear in this entry.

		:return: A list of local file paths to the images.
		"""

		return []

	@property
	def related_images(self) -> List[str]: # TODO: implement searching for related images
		"""
		Download all images that appear in this entry PLUS anything that is related to the topic of the given entry.

		:return: A list of local file paths to the images.
		"""

		return self.images

	def __getattr__(self, attr) -> Any:
		"""
		Every unknown attribute is redirected to the base FeedParser entry.

		:param attr: The attribute to be redirected.
		:return: The specified attribute on the base FeedParser entry.
		"""
		try:
			return getattr(self.entry, attr)
		except AttributeError:
			return self.__getattribute__(attr)

	def _download_image(self, url: str) -> str:
		"""
		Download an image from the specified location into a temporary file.
		Move/copy/upload/... it as soon as you can, as it is a TEMPORARY file.

		:return: The path to the temporary image file.
		"""

		response = requests.get(url)
		if response.status_code == 200:
			_, temp_file_path = tempfile.mkstemp(suffix='.jpg', prefix='downloaded_image_', dir=tempfile.gettempdir())
			with open(temp_file_path, 'wb') as temp_file:
				temp_file.write(response.content)
			return temp_file_path
		else:
			return None
