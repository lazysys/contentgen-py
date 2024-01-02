from enum import Enum

class ContentType(Enum):
	"""
	Enum that specifies the types of posts that can exist.
	"""
	
	MICROBLOG = 0
	THREAD = 6
	ARTICLE = 1
	SHORT_VIDEO = 2
	LONG_VIDEO = 3
	SINGLE_IMAGE = 4
	CAROUSEL = 5
