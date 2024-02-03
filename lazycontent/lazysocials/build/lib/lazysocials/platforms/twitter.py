from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Type

import tweepy
import lazycommon.content.types as types

from lazysocials.platforms.platform import Platform

from io import BufferedReader

@dataclass(frozen=True)
class TwitterAuth:
	"""
	Class holding Twitter authentication information.
	"""

	consumer_key: str
	consumer_secret: str
	access_token: str
	access_token_secret: str

class Twitter(Platform):
	def __init__(auth: TwitterAuth, *types: Type[types.Content], max_images: int = 4):
		self._twitter_auth = auth
		self.max_images = max_images
		super().__init__(types)
		
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
	
	def _medias_to_media_ids(self, medias: List[BufferedReader]) -> List[str]:
		ids = []
		for media in medias:
			if media:
				ids.append(self._old_client.media_upload(file=media.raw).media_id_string)
		if len(ids) < 1:
			ids = None
		return ids

	def _publish(self, content: str, medias: List[BufferedReader] = [], in_reply_to: str = None) -> str:
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

	def Microblog(self, content: types.Microblog) -> bool:
		return bool(self._publish(content.content, medias = content.images))
	def Thread(self, content: types.Thread) -> bool:
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
	
	# FIXME: probably too long without X Premium Pro 420 ElonMusk orwhat
	def Article(self, content: types.Article) -> bool:
		return bool(self._publish(content.content))

	def Image(self, content: types.Image) -> bool:
		return bool(self._publish(content.content, medias = [content.image]))
	def Carousel(self, content: types.Carousel) -> bool:
		return bool(self._publish(content.content, medias = [img.image for img in content.images]))

	def Video(self, content: types.Video) -> bool:
		return bool(self._publish(content.content, medias = [content.video]))
