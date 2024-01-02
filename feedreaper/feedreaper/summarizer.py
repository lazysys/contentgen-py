from abc import ABC, abstractmethod
from dataclasses import dataclass
from openai import OpenAI
from feedreaper.rssfeed import Entry
from typing import List

from lazycommon.content_type import ContentType

class Summarizer(ABC):
	"""
	A generic interface for a summarizer.
	"""
	@abstractmethod
	def summarize(self, entries: List[Entry], into: ContentType) -> List[str]:
		"""
		This function takes list of entries, which will be converted into the specified content type. (TEXT!)

		:return: A list of text segments.
		"""

		pass

@dataclass
class OpenAIChat:
	"""
	A class to abstract away OpenAI's chat API.

	:param key: The key for OpenAI's API.
	:param model: The model to be used at OpenAI.
	"""

	_key: str
	model: str = "gpt-3.5-turbo"

	@property
	def key(self):
		return _key
	@key.setter
	def key(self, new):
		self._key = new
		self.__post_init__()

	def __post_init__(self):
		self._api = OpenAI(api_key = self._key)

	def generate(self, prompt) -> str:
		"""
		Generates a response to the given prompt.
		
		:return: The answer from OpenAI's chat API.
		"""

		return self._api.chat.completions.create(messages = [
		{ 
			"role": "user",
			"content": prompt
		}
		], model=self.model).choices[0].message.content

@dataclass
class OpenAISummarizer(Summarizer):
	"""
	Glues the [Summarizer] interface and the [OpenAIChat] API.
	
	:param api: An instance of the [OpenAIChat] class.
	"""

	api: OpenAIChat

	def summarize(self, entries: List[Entry], into: ContentType) -> List[str]:
		"""
		Summarizes a list of [Entry]s into the specified [ContentType] using [OpenAIChat].
		As these models can't conform to an exact character count, we reiterate many times offending answers, which can be a few iterations.
		Keep that in mind for billing.
		"""

		articles = ""
		for entry in entries:
			articles += f"\nTitle: {entry.title}\n"
			articles += f"Content: {entry.content}\n"
		if into == ContentType.MICROBLOG:
				answer = self.api.generate(f"DO NOT MENTION THE CHARACTER COUNT! You're a highly qualified tech-journalist. Make a summary of the following articles combined, at max 280 characters:" + articles)
				while True:
					if len(answer) > 280:
						answer = self.api.generate(f"DO NOT MENTION THE CHARACTER COUNT! You're a highly qualified tech-journalist. Make a short (at max 200 characters) summary of the following snippet, and focus on the newsworthiness of it:\n" + answer)
					else:
						return [answer]
		elif into == ContentType.THREAD:
			raise UnimplementedError
		elif into == ContentType.ARTICLE:
			return [self.api.generate(f"You're a highly qualified tech-journalist. You write articles in this format:\nTitle: <title of the article>\nContent: <contents of the article>\n\nMake an article out of the following article(s):" + articles)]
		elif into == ContentType.SHORT_VIDEO:
			return [self.api.generate(f"You're a highly qualified tech-journalist. You write video scripts in this format:\nTitle: <caption of video>\nContent: <your lines to be said in the video>\n\nMake this out of the following article(s):" + articles)]
		elif into == ContentType.LONG_VIDEO:
			raise UnimplementedError
		elif into == ContentType.SINGLE_IMAGE:
			raise UnimplementedError
		elif into == ContentType.CAROUSEL:
			raise UnimplementedError
