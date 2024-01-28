from typing import List
from dataclasses import dataclass

@dataclass
class Content:
	content: str

@dataclass
class Microblog(Content):
	images: List[bytes] = None
# NOTE: don't you dare inherit Microblog from Thread, that might feel cool now but imagine the implications...
@dataclass
class Thread(Content):
	microblogs: List[Microblog] = None
	images: List[bytes] = None

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
	image: bytes
@dataclass
class Carousel(Content):
	images: List[Image]
