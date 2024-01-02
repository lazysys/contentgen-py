from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

import tweepy

from lazysocials.lazysocials import Microblog, Thread

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
class Twitter(Microblog, Thread):
	_twitter_auth: TwitterAuth
	
	@property
	def twitter_auth(self):
		return self._twitter_auth
	@twitter_auth.setter
	def twitter_auth(self, auth):
		self._twitter_auth = auth
		__post_init__()

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

	def _publish(self, content: str, images: List[str]):
		try:
			self._client.create_tweet(text=content, media_ids=self._images_to_media_ids(images))
		except tweepy.errors.HTTPException as e:
			if "Payload too large" in str(e):
				pass # TODO: compress images
		

	def publish_microblog(self, content: List[str], images: List[str]):
		self._publish(content, images)

	def publish_thread(self, content: List[str], images: List[str]):
		raise UnimplementedError
