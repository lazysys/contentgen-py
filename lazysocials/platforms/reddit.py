from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Type

import praw
from praw.models import InlineGif, InlineImage, InlineVideo, InlineMedia, Subreddit

from lazycommon.content_type import Content, Microblog

from lazysocials.platforms.platform import Platform

@dataclass(frozen=True)
class RedditAuth:
	"""
	Class holding Reddit authentication information.
	"""

	client_id: str
	client_secret: str
	username: str
	password: str
	user_agent: str = "Unknown LazySocials application (by u/gregismotion)"

# TODO: ability to cross-post
@dataclass
class Reddit(Platform):
	_auth: RedditAuth
		
	@property
	def auth(self):
		return self._auth
	@auth.setter
	def auth(self, auth):
		self._auth = auth
		self.__post_init__()
	
	@property
	def subreddits(self) -> List[str]:
		return [x.name for x in self._subreddits]
	@subreddits.setter
	def subreddits(self, subreddits: List[str]):
		self._subreddits = [self._client.subreddit(x) for x in subreddits]

	def __init__(self, _auth, subreddits: List[str], types: List[Type[Content]] = None):
		super().__init__(types or [Microblog])
		self._auth = _auth
		self.__post_init__()
		self._subreddits = []
		self.subreddits = subreddits

	def __post_init__(self):
		self._client = praw.Reddit(
			client_id = self._auth.client_id,
			client_secret = self._auth.client_secret,
			password = self._auth.password,
			username = self._auth.username,
			user_agent = self._auth.user_agent
		)
	
	# TODO: captions per image
	def _images_to_inlines(self, images: List[str]) -> Dict[str, InlineImage]:
		inlines = {}
		count = 0
		for image in images:
			inlines[f"img{count}"] = InlineImage(path = image)
			count += 1
		return inlines
	
	def _truncate_text(self, text, max_chars):
		if len(text) <= max_chars:
			return text
		last_space = text.rfind(' ', 0, max_chars)
		if last_space == -1:
			return text[:max_chars] + '...'
		return text[:last_space] + '...'

	def _inlines_to_selftext(self, inlines: Dict[str, InlineImage]) -> str:
		result = ""
		for key in inlines.keys():
			result += f" {{{key}}}"
		return result

	def _publish(self, content: str, images: List[str]) -> bool:
		title = self._truncate_text(content, 300)
				
		for subreddit in self._subreddits:
			# FIXME: as soon as PR rolls in to have text in image posts, we don't need this and it will look better everytime
			if title == content and len(images) > 0:
				if len(images) > 1:
					captioned_images = { str(i): value for i, value in enumerate(images) }
					subreddit.submit_gallery(content, captioned_images)
				else:
					subreddit.submit_image(content, images[0])
			else:
				inlines = self._images_to_inlines(images)
				image_text = self._inlines_to_selftext(inlines)
				subreddit.submit(content, inline_media = inlines, selftext = content + image_text)
	
	def publish(self, content: Content) -> bool:
		if super().publish(content):
			text = ""
			images = []
			if isinstance(content, Microblog):
				text = content.content
				images = content.images
			if not len(text) == 0:
				return self._publish(text, images)
			else:
				return False
