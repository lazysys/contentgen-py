from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

import tweepy
from lazycommon.content_type import *

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
	max_images: int = 4
		
	@property
	def twitter_auth(self):
		return self._twitter_auth
	@twitter_auth.setter
	def twitter_auth(self, auth):
		self._twitter_auth = auth
		self.__post_init__()
	
	def __init__(self, _twitter_auth, types):
		super().__init__(types)
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
	
	def _medias_to_media_ids(self, medias: List[str]) -> List[str]:
		ids = []
		for media in medias:
			if media:
				ids.append(self._old_client.media_upload(media).media_id_string)
		if len(ids) < 1:
			ids = None
		return ids

	def _publish(self, content: str, medias: List[str] = [], in_reply_to: str = None) -> str:
		while True:
			try:
				response = self._client.create_tweet(text = content, media_ids = self._medias_to_media_ids(medias), in_reply_to_tweet_id = in_reply_to)
				return len(response.errors) < 1
			except tweepy.errors.HTTPException as e:
				if "Payload too large" in str(e): # TODO: compress images
					print("Twitter: CRITICAL FAILURE: Payload too large! TODO: IMPLEMENT IMAGE/VIDEO COMPRESSION")
				elif f"maximum of {str(self.max_images)} items" in str(e):
					print(f"Twitter: WARNING: will cut down media count to {str(self.max_images)} (max.)!")
					medias = medias[:self.max_images]
					continue
				else:
					print(str(e))
				return None
		

	def publish(self, content: Content) -> bool:
		if super().publish(content):
			if isinstance(content, Microblog):
				return bool(self._publish(content.content, medias = content.images))
			elif isinstance(content, Thread):
				images = content.images
				last_tweet = self._publish(content.content, medias = [images.pop() for _ in range(min(len(images), self.max_images))])
				for microblog in content.microblogs:
					current_images = microblog.images
					last_tweet = self._publish(
							microblog.content, 
							medias = [current_images.pop() for _ in range(min(len(current_images), self.max_images))] + 
							[images.pop() for _ in range(max(0, self.max_images - len(current_images)))], 
							in_reply_to = last_tweet
					)
					images += current_images
				if len(images) > 0:
					print("Twitter: WARNING: Left-over images from thread, dropping them!")
				return bool(last_tweet)
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
