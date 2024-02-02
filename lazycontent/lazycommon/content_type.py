from typing import List
from dataclasses import dataclass

from io import BufferedReader

@dataclass
class Content:
	content: str

@dataclass
class Microblog(Content):
	images: List[BufferedReader] = None
# NOTE: don't you dare inherit Microblog from Thread, that might feel cool now but imagine the implications...
@dataclass
class Thread(Content):
	microblogs: List[Microblog] = None
	images: List[BufferedReader] = None

@dataclass
class Article(Content):
	title: str

@dataclass
class Video(Content):
	video: bytes
@dataclass
class ShortVideo(Video):
	pass
@dataclass
class LongVideo(Video):
	pass

@dataclass
class Image(Content):
	image: BufferedReader
@dataclass
class Carousel(Content):
	images: List[Image]
