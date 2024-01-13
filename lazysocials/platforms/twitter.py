from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

import tweepy
from lazycommon.content_type import Content, Microblog, Thread

from lazysocials.platforms.platform import Platform


@dataclass(frozen=True)
class TwitterAuth:
	"""
	Class holding Twitter authentication information.
	"""

	consumer_key: str
	consumer_secret: str
	access_token: str
	access_token_secret: str

@dataclass
class Twitter(Platform):
	_twitter_auth: TwitterAuth
		
	@property
	def twitter_auth(self):
		return self._twitter_auth
	@twitter_auth.setter
	def twitter_auth(self, auth):
		self._twitter_auth = auth
		self.__post_init__()
	
	def __init__(self, _twitter_auth, types = None):
		super().__init__(types or [Microblog])
		self._twitter_auth = _twitter_auth
		self.__post_init__()

	def __post_init__(self):
		self._client = tweepy.Client(
		    consumer_key = self._twitter_auth.consumer_key,
		    consumer_secret = self._twitter_auth.consumer_secret,
		    access_token = self._twitter_auth.access_token,
		    access_token_secret = self._twitter_auth.access_token_secret
		)
		self._old_client = tweepy.API(tweepy.OAuth1UserHandler(
		    consumer_key = self._twitter_auth.consumer_key,
		    consumer_secret = self._twitter_auth.consumer_secret,
		    access_token = self._twitter_auth.access_token,
		    access_token_secret = self._twitter_auth.access_token_secret
		))
	
	def _images_to_media_ids(self, images: List[str]) -> List[str]:
		ids = []
		for image in images:
			if image:
				ids.append(self._old_client.media_upload(image).media_id_string)
		if len(ids) < 1:
			ids = None
		return ids

	def _publish(self, content: str, images: List[str], in_reply_to: str = None) -> str:
		try:
			response = self._client.create_tweet(text = content, media_ids = self._images_to_media_ids(images), in_reply_to_tweet_id = in_reply_to)
			return len(response.errors) < 1
		except tweepy.errors.HTTPException as e:
			if "Payload too large" in str(e):
				pass # TODO: compress images
			return None
		

	def publish(self, content: Content) -> bool:
		if super().publish(content):
			if isinstance(content, Microblog):
				return bool(self._publish(content.content, content.images))
			elif isinstance(content, Thread):
				last_tweet = None
				for microblog in content.microblogs:
					last_tweet = self._publish(microblog.content, microblog.images, last_tweet)
				return bool(last_tweet)
			elif isinstance(content, Article):
				raise UnimplementedError
			elif isinstance(content, Image):
				return bool(self._publish(content.content, [content.image]))
			elif isinstance(content, Carousel):
				return bool(self._publish(content.content, [img.image for img in content.images]))
			else:
				return False
