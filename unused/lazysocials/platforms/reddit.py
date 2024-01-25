from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Type

import praw
from praw.models import InlineGif, InlineImage, InlineVideo, InlineMedia, Subreddit
from praw.exceptions import RedditAPIException

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
	def subreddits(self, subreddits: Dict[str, str]):
		self._subreddits = [(self._client.subreddit(key), val) for key, val in subreddits.items()]

	def __init__(self, _auth, subreddits: List[str], types: List[Type[Content]]):
		super().__init__(types)
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

	def _publish(self, content: str, title: str = None, images: List[str] = []) -> bool:
		for subreddit in self.subreddits:
			flair = [flair["flair_template_id"] for flair in subreddit[0].flair.link_templates.user_selectable() if flair["flair_text"] == subreddit[1]]
			subreddit = subreddit[0]

			requirements = subreddit.post_requirements()
			title = title or self._truncate_text(content, requirements["title_text_max_length"] or 300)
			selftext = self._truncate_text(content, requirements["body_text_max_length"] or 10000)

			# FIXME: as soon as PR rolls in to have text in image posts, we don't need this and it will look better everytime
			NO_IMAGES = False
			SUBMIT_VALIDATION_BODY_NOT_ALLOWED = False
			while True:
				try:
					if NO_IMAGES and not SUBMIT_VALIDATION_BODY_NOT_ALLOWED:
						subreddit.submit(title, selftext = selftext, flair_id = flair)
						break
					elif SUBMIT_VALIDATION_BODY_NOT_ALLOWED:
						subreddit.submit(title, selftext = "", flair_id = flair)
						break

					if title == content and len(images) > 0:
						if len(images) > 1:
							captioned_images = { str(i): value for i, value in enumerate(images) }
							subreddit.submit_gallery(title, captioned_images, flair_id = flair)
						else:
							subreddit.submit_image(title, images[0], flair_id = flair)
					else:
						inlines = self._images_to_inlines(images)
						image_text = self._inlines_to_selftext(inlines)
						subreddit.submit(title, inline_media = inlines, selftext = selftext + image_text, flair_id = flair)
					break
				except RedditAPIException as e:
					e = str(e)
					if "NO_IMAGES" in e:
						NO_IMAGES = True
					elif "SUBMIT_VALIDATION_BODY_NOT_ALLOWED" in e: # FIXME: but they might allow images? quite weird requirements ngl reddit
						SUBMIT_VALIDATION_BODY_NOT_ALLOWED = True
			return True
				
	
	def publish(self, content: Content) -> bool:
		if super().publish(content):
			if isinstance(content, Microblog):
				return bool(self._publish(content.content, content.images))
			elif isinstance(content, Thread):
				text = "\n".join([microblog.content for microblog in content.microblogs])
				images = [item for sublist in [microblog.images for microblog in content.images] for item in sublist]
				return self._publish(content = text, images = images)
			elif isinstance(content, Article):
				return self._publish(content = content.content, title = content.title)
			elif isinstance(content, Image):
				return self._publish(content = content.content, images = [content.image])
			elif isinstance(content, Carousel):
				return self._publish(content = content.content, images = [img.image for img in content.images])
			elif isinstance(content, Video): # TODO: reddit video posting
				raise UnimplementedError
			else:
				return False
