from dataclasses import dataclass
from openai import OpenAI
from typing import List, Type

from lazycommon.content_type import Content
import lazycommon.content_type as ContentType
from lazycommon.entry import Entry

from lazysummary.summarizer import Summarizer

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
	
	def _convert_answer_to_std(self, answer: str) -> List[str]:
		lines = answer.split("\n")
		title = lines[0].replace("Title: ")
		content = "\n".join(lines[1:]).replace("Content: ", "")
		return [title, content]
	def _convert_carousel_to_std(self, answer: str) -> List[str]:
		lines = answer.split("\n")
		return [item.split(': ', 1)[1].strip() for item in lines if item.strip()]

	def summarize(self, entries: List[Entry], into: Type[Content]) -> List[str]:
		"""
		Summarizes a list of [Entry]s into the specified [Content] using [OpenAIChat].
		As these models can't conform to an exact character count, we reiterate many times offending answers, which can be a few iterations.
		Keep that in mind for billing.
		"""

		articles = ""
		for entry in entries:
			articles += f"\nTitle: {entry.title}\n"
			articles += f"Content: {entry.content}\n"
		
		if issubclass(into, ContentType.Microblog):
				answer = self.api.generate(f"DO NOT MENTION THE CHARACTER COUNT, NOR SHOW THAT YOU ARE A BOT! BE A HUMAN WRITING NORMALLY A CONCISE POST! DON'T INTRODUCE YOURSELF! You're a highly qualified tech-journalist. Make a summary of the following articles combined, at max 280 characters:" + articles)
				while True:
					if len(answer) > 280:
						answer = self.api.generate(f"DO NOT MENTION THE CHARACTER COUNT, NOR SHOW THAT YOU ARE A BOT! BE A HUMAN WRITING NORMALLY A CONCISE POST! DON'T INTRODUCE YOURSELF! You're a highly qualified tech-journalist. Make a short (at max 200 characters) summary of the following snippet, and focus on the newsworthiness of it:\n" + answer)
					else:
						return [answer]
		elif issubclass(into, ContentType.Thread):
			answer = self.api.generate(f"You're a highly qualified tech journalist.\n\ndon't prefix the tweets\ndon't use hashtags\n\nCreate a Twitter thread with tweet blocks seperated by --- from the following article(s) (combine them into one summary thread):" + articles)
			return answer.split("\n---\n")
		elif issubclass(into, ContentType.Article):
			answer = self.api.generate(f"You're a highly qualified tech-journalist. You write articles in this format:\nTitle: <title of the article>\nContent: <contents of the article>\n\nMake ONE SUMMARY article out of the following article(s):" + articles)
			return self._convert_answer_to_std(answer)
		elif issubclass(into, ContentType.ShortVideo):
			answer = self.api.generate(f"You're a highly qualified tech-journalist. You write short (15s) video scripts in this format:\nTitle: <caption of video>\nContent: <your lines to be said in the video>\n\nYou follow the 3 point structure: hook, some talking points, call to action (the goal is to get engagement) => but all woven into one text to be read out loud (and put all these under Content:)\n\ndont use emojis\nbe concise, don't introduce yourself\n\nMake ONE SHORT SUMMARY VIDEO out of the following article(s):" + articles)
			return self._convert_answer_to_std(answer)
		elif issubclass(into, ContentType.LongVideo):
			answer = self.api.generate(f"You're a highly qualified tech-journalist. You write long (5min) video scripts in this format:\nTitle: <caption of video>\nContent: <your lines to be said in the video, NO FORMATTING, ONLY WHAT WOULD BE SPOKEN OUT>\n\nYou follow the 3 point structure: hook, many talking points, call to action (the goal is to get engagement) => but all woven into one text to be read out loud (and put all these under Content:)\n\ndont use emojis\nbe concise, don't introduce yourself\n\nMake ONE LONG SUMMARY VIDEO out of the following article(s):" + articles)
			return self._convert_answer_to_std(answer)
		elif issubclass(into, ContentType.Image):
			return [self.api.generate(f"You're a highly qualified tech-journalist.\n\nUse the following format (NO FORMATTING, THIS IS GOING STRAIGHT TO THE IMAGE):\n<headline without quotes>\n\nMake ONE short and concise summary headline (one line) that can be put on an image from the following article(s) (handle these articles as one):" + articles)]
		elif issubclass(into, ContentType.Carousel):
			return self._convert_carousel_to_std(self.api.generate(f"You're a highly qualified tech journalist. Make an Instagram carousel slide by slide using this format (every slide is one line, one sentence, atomic short and concise) (only one caption which can be longer):\n\nCaption: <caption>\n\n1: <first slide>\n2: <second slide>\n<...as many as you need...>\n\nSummarize in this format the following article(s) (in your head combine these into one):" + articles))

