from typing import List
from dataclasses import dataclass

@dataclass
class Content:
	content: str

@dataclass
class Microblog(Content):
	images: List[str]
@dataclass
class Thread(Content):
	microblogs: List[Microblog]

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
