from dataclasses import dataclass
import openai
from openai import OpenAI
from typing import List, Type, get_type_hints, get_args

from lazycommon.entry import Entry
from lazycommon.slide import Slide
from lazycommon.content.types import Content

from .summarizer import Summarizer

@dataclass
class OpenAIChat:
	"""
	A class to abstract away OpenAI's chat API.

	:param key: The key for OpenAI's API.
	:param model: The model to be used at OpenAI.
	"""

	_key: str
	model: str = "gpt-3.5-turbo"
	
	# TODO: as soon as these enums roll out switch, this already broke over versions...
	@classmethod
	def models(_) -> List[str]:
		model_type = get_type_hints(openai.types.chat.completion_create_params.CompletionCreateParamsBase)['model']
		args = get_args(model_type)
		result = list(get_args(args[1]))
		return result

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

class OpenAISummarizer(Summarizer):
	def __init__(self, api: OpenAIChat, *types: Type[Content]):
		self.api = api
		super().__init__(types)

	def _convert_answer_to_std(self, answer: str) -> List[str]:
		lines = answer.split("\n")
		title = lines[0].replace("Title: ", "")
		content = "\n".join(lines[1:]).replace("Content: ", "")
		return [title, content]
	def _convert_carousel_to_std(self, answer: str) -> List[str]:
		lines = answer.split("\n")
		return [item.split(': ', 1)[1].strip() for item in lines if item.strip()]
	
	def _combined_entries(self, entries: List[Entry]) -> str:
		articles = ""
		for entry in entries:
			articles += f"\nTitle: {entry.title}\n"
			articles += f"Content: {entry.content}\n"
		return articles
		
	def Microblog(self, entries: List[Entry]) -> List[Slide]:
		combined = self._combined_entries(entries)
		answer = self.api.generate(f"DO NOT MENTION THE CHARACTER COUNT, NOR SHOW THAT YOU ARE A BOT! BE A HUMAN WRITING NORMALLY A CONCISE POST! DON'T INTRODUCE YOURSELF! You're a highly qualified tech-journalist. Make a summary of the following articles combined, at max 280 characters:" + combined)
		while True:
			if len(answer) > 280:
				answer = self.api.generate(f"DO NOT MENTION THE CHARACTER COUNT, NOR SHOW THAT YOU ARE A BOT! BE A HUMAN WRITING NORMALLY A CONCISE POST! DON'T INTRODUCE YOURSELF! You're a highly qualified tech-journalist. Make a short (at max 200 characters) summary of the following snippet, and focus on the newsworthiness of it:\n" + answer)
			else:
				return [Slide(caption = answer, headline = True, images = [entry.thumbnail for entry in entries])]

	def Thread(self, entries: List[Entry]) -> List[Slide]:
		combined = self._combined_entries(entries)
		answer = self.api.generate(f"You're a highly qualified tech journalist.\n\ndon't prefix the tweets\ndon't use hashtags\n\nCreate a Twitter thread with tweet blocks seperated by --- from the following article(s) (combine them into one summary thread):" + combined)
		answers = answer.split("\n---\n")
		headline = Slide(caption = answer[0], headline = True, images = [entry.thumbnail for entry in entries])
		return headline + [Slide(caption = answer) for answer in answers[1:]]

	def Article(self, entries: List[Entry]) -> List[Slide]:
		combined = self._combined_entries(entries)
		answer = self.api.generate(f"You're a highly qualified tech-journalist. You write articles in this format:\nTitle: <title of the article>\nContent: <contents of the article>\n\nMake ONE SUMMARY article out of the following article(s):" + combined)
		std = self._convert_answer_to_std(answer)
		return [Slide(caption = std[0], headline = True, images = [entry.thumbnail for entry in entries]), Slide(caption = std[1])]
	
	def ShortVideo(self, entries: List[Entry]) -> List[Slide]:
		combined = self._combined_entries(entries)
		answer = self.api.generate(f"You're a highly qualified tech-journalist. You write short (15s) video scripts in this format:\nTitle: <caption of video>\nContent: <your lines to be said in the video>\n\nYou follow the 3 point structure: hook, some talking points, call to action (the goal is to get engagement) => but all woven into one text to be read out loud (and put all these under Content:)\n\ndont use emojis\nbe concise, don't introduce yourself\n\nMake ONE SHORT SUMMARY VIDEO out of the following article(s):" + combined)
		std = self._convert_answer_to_std(answer)
		return [Slide(caption = std[0], headline = True, images = [entry.thumbnail for entry in entries]), Slide(caption = std[1])]

	def LongVideo(self, entries: List[Entry]) -> List[Slide]:
		combined = self._combined_entries(entries)
		answer = self.api.generate(f"You're a highly qualified tech-journalist. You write long (5min) video scripts in this format:\nTitle: <caption of video>\nContent: <your lines to be said in the video, NO FORMATTING, ONLY WHAT WOULD BE SPOKEN OUT>\n\nYou follow the 3 point structure: hook, many talking points, call to action (the goal is to get engagement) => but all woven into one text to be read out loud (and put all these under Content:)\n\ndont use emojis\nbe concise, don't introduce yourself\n\nMake ONE LONG SUMMARY VIDEO out of the following article(s):" + combined)
		return [Slide(caption = std[0], headline = True, images = [entry.thumbnail for entry in entries]), Slide(caption = std[1])]

	def Image(self, entries: List[Entry]) -> List[Slide]:
		combined = self._combined_entries(entries)
		answer = self.api.generate(f"You're a highly qualified tech-journalist.\n\nUse the following format (NO FORMATTING, THIS IS GOING STRAIGHT TO THE IMAGE):\n<headline without quotes>\n\nMake ONE short and concise summary headline (one line) that can be put on an image from the following article(s) (handle these articles as one):" + combined)
		return [Slide(caption = answer, headline = True, images = [entry.thumbnail for entry in entries])]

	def Carousel(self, entries: List[Entry]) -> List[Slide]:
		combined = self._combined_entries(entries)
		std = self._convert_carousel_to_std(self.api.generate(f"You're a highly qualified tech journalist. Make an Instagram carousel slide by slide using this format (every slide is one line, one sentence, atomic short and concise) (only one caption which can be longer):\n\nCaption: <caption>\n\n1: <first slide>\n2: <second slide>\n<...as many as you need...>\n\nSummarize in this format the following article(s) (in your head combine these into one):" + combined))
		headline = Slide(caption = std[0], headline = True, images = [entry.thumbnail for entry in entries])
		return headline + [Slide(caption = answer) for answer in std[1:]]
