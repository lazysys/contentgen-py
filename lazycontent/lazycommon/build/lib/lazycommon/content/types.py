from typing import List
from dataclasses import dataclass

from io import BufferedReader

from ..slide import Slide

@dataclass
class Content:
	content: str

@dataclass
class Microblog(Content):
	images: List[BufferedReader] = None
	
	@classmethod
	def from_slide(cls, slide: Slide):
		return cls(content = slide.caption, images = slide.images)

@dataclass
class Thread(Content):
	microblogs: List[Microblog] = None
	images: List[BufferedReader] = None

	@classmethod
	def from_slides(cls, slides: List[Slide]):
		return cls(content = slides[0].caption, microblogs = [Microblog.from_slide(slide) for slide in slides[1:]], images = slides[0].images)

@dataclass
class Article(Content):
	title: str
	# TODO: slides

# TODO: video slides
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

	@classmethod
	def from_slide(cls, slide: Slide):
		return cls(content = slide.caption, image = slide.images[0])

@dataclass
class Carousel(Content):
	images: List[Image]

	@classmethod
	def from_slides(cls, slides: List[Slide]):
		# NOTE: do we need more in the caption?
		return cls(content = slides[0].caption, images = [Image.from_slide(slide) for slide in slides])
