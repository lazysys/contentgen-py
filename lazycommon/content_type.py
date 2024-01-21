from typing import List
from dataclasses import dataclass

@dataclass
class Content:
	content: str

@dataclass
class Microblog(Content):
	images: List[str]
# NOTE: don't you dare inherit Microblog from Thread, that might feel cool now but imagine the implications...
@dataclass
class Thread(Content):
	microblogs: List[Microblog]
	images: List[str]

@dataclass
class Article(Content):
	title: str

@dataclass
class Video(Content):
	video: str
@dataclass
class ShortVideo(Video):
	pass
@dataclass
class LongVideo(Video):
	pass

@dataclass
class Image(Content):
	image: str
@dataclass
class Carousel(Content):
	images: List[Image]
