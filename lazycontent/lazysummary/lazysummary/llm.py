from lazycommon.entry import Entry
from lazycommon.slide import Slide
from lazycommon.content.types import Content

from lazyllm import LLM, VisionLLM, JSONLLM

from .summarizer import Summarizer

import json

class LLMSummarizer(Summarizer):
	@property
	def prompts(self):
		rules = [
			"DO NOT MENTION THE CHARACTER COUNT!",
			"NEVER SHOW YOU'RE A BOT!",
			"BE A HUMAN WRITING NORMALLY!",
			"WRITE CONCISE POSTS!",
			"DO NOT INTRODUCE YOURSELF",
			"DO NOT REVEAL THE WEBSITES/SOURCES FROM WHICH THE ARTICLES COME FROM",
			"DO NOT USE QUOTES AROUND YOUR WHOLE RESPONSE",
			"DO NOT USE HASHTAGS",
			"DO NOT PREFIX TWEETS",
			"DO NOT USE EMOJIS"
		]
		persona = "You're a highly qualified tech-journalist."
		
		prefix = "\n".join(rules) + f"\n\n{persona}"

		if isinstance(self.llm, VisionLLM):
			prefix = f"You might get a few images as a bonus, take them into account in the following task.\n\n{prefix}"
		prompts = {
			"Microblog": "Make a microblog type of summary (and focus on it's newsworthiness) of the following articles combined, at max 280 characters:\n{articles}",
			"MicroblogRepeat": "Make a short (at max 200 characters) summary of the following snippet, and focus on the newsworthiness of it:\n{snippet}"
			"Thread": "Create a Twitter thread with tweet blocks seperated by --- from the following article(s) (combine them into one summary thread):\n{articles}",
			"Article": "You write articles in this format:\nTitle: <title of the article>\nContent: <contents of the article>\n\nMake ONE SUMMARY article out of the following article(s):\n{articles}",
			"ShortVideo": "You write short (15s) video scripts in this format:\nTitle: <caption of video>\nContent: <your lines to be said in the video>\n\nYou follow the 3 point structure: hook, some talking points, call to action (the goal is to get engagement) => but all woven into one text to be read out loud (and put all these under Content:)\nMake ONE SHORT SUMMARY VIDEO out of the following article(s):\n{articles}",
			"LongVideo": "You write long (5min) video scripts in this format:\nTitle: <caption of video>\nContent: <your lines to be said in the video, NO FORMATTING, ONLY WHAT WOULD BE SPOKEN OUT>\n\nYou follow the 3 point structure: hook, many talking points, call to action (the goal is to get engagement) => but all woven into one text to be read out loud (and put all these under Content:)\nMake ONE LONG SUMMARY VIDEO out of the following article(s):\n{articles}",
			"Image": "Use the following format (NO FORMATTING, THIS IS GOING STRAIGHT TO THE IMAGE):\n<headline without quotes>\n\nMake ONE short and concise summary headline (one line) that can be put on an image from the following article(s) (handle these articles as one):\n{articles}",
			"Carousel": "Make an Instagram carousel slide by slide using this format (every slide is one line, one sentence, atomic short and concise) (only one caption which can be longer):\n\nCaption: <caption>\n\n1: <first slide>\n2: <second slide>\n<...as many as you need, but aim for 6 slides...>\n\nSummarize in this format the following article(s) (in your head combine these into one):\n{articles}"
		}

		if isinstance(self.llm, JSONLLM):
			prompts = {
				"Microblog": "Make a microblog type of summary (and focus on it's newsworthiness) of the following articles combined, at max 280 characters (put it into the 'content' key in your json):\n{articles}",
				"MicroblogRepeat": "Make a short (at max 200 characters) summary of the following snippet, and focus on the newsworthiness of it (put it into the 'content' key in your json):\n{snippet}"
				"Thread": "Create a Twitter thread with tweet blocks from the following article(s) (combine them into one summary thread) (put these blocks into a JSON array, and all objects' text should be in the 'content' key):\n{articles}",
				"Article": "Put the article's title into the 'title' key, and the content into the 'content' key in your JSON.\nMake ONE SUMMARY article out of the following article(s):\n{articles}",
				"ShortVideo": "You write short (15s) video scripts (put the video's title into the 'title' key, and the content into the 'content' key in your JSON.)\nYou follow the 3 point structure: hook, some talking points, call to action (the goal is to get engagement) => but all woven into one text to be read out loud (and put all these under Content:)\nMake ONE SHORT SUMMARY VIDEO out of the following article(s):\n{articles}",
				"LongVideo": "You write long (5min) video scripts (put the video's title into the 'title' key, and the content into the 'content' key in your JSON.)\nYou follow the 3 point structure: hook, many talking points, call to action (the goal is to get engagement) => but all woven into one text to be read out loud (and put all these under Content:)\nMake ONE LONG SUMMARY VIDEO out of the following article(s):\n{articles}",
				"Image": "Use the following format (NO FORMATTING, THIS IS GOING STRAIGHT TO THE IMAGE, put the headline into the 'caption' key):\n<headline without quotes>\n\nMake ONE short and concise summary headline (one line) that can be put on an image from the following article(s) (handle these articles as one):\n{articles}",
				"Carousel": "Make an Instagram carousel slide by slide. (Put these slide objects into a JSON array, and each object has to have a 'caption' key.) \nSummarize in this format the following article(s) (in your head combine these into one):\n{articles}"
			}
			
	return { key: f"{prefix}\n{value}" for key, value in prompts.items() }
	
	def __init__(self, llm: LLM, *types: Type[Content]):
		self.llm = llm
		super().__init__(types)
	
	# FIXME: what if not correct structure?
	def _convert_answer_to_std(self, answer: str) -> List[str]:
		if isinstance(self.llm, JSONLLM):
			data = json.loads(answer)
			title = answer.get("title", None)
			content = answer.get("content", None)
		else:
			lines = answer.split("\n")
			title = lines[0].replace("Title: ", "")
			content = "\n".join(lines[1:]).replace("Content: ", "")
		return [title, content]
	def _convert_carousel_to_std(self, answer: str) -> List[str]:
		if isinstance(self.llm, JSONLLM):
			data = json.loads(answer)
			slides = [slide["caption"] for slide in data]
		else:
			lines = answer.split("\n")
			slides = [item.split(': ', 1)[1].strip() for item in lines if item.strip()]
		return slides
	
	def _combined_entries(self, entries: List[Entry]) -> str:
		articles = [{ "title": entry.title, "content": entry.content } for entry in entries] 
		return json.dumps(articles)
		
	def Microblog(self, entries: List[Entry]) -> List[Slide]:
		combined = self._combined_entries(entries)
		answer = self.llm.generate(prompts["Microblog"].format(articles = combined))
		while True:
			if isinstance(self.llm, JSONLLM):
				data = json.loads(answer)
				answer = data["content"]
			if len(answer) > 280:
				answer = self.llm.generate(prompts["MicroblogRepeat"].format(snippet = answer))
			else:
				return [Slide(caption = answer, headline = True, images = [entry.thumbnail for entry in entries])]

	def Thread(self, entries: List[Entry]) -> List[Slide]:
		combined = self._combined_entries(entries)
		answer = self.llm.generate(prompts["Thread"].format(articles = combined))
		if isinstance(self.llm, JSONLLM):
			data = json.loads(answer)
			answers = [slide["content"] for slide in data]
		else:
			answers = answer.split("\n---\n")
		headline = Slide(caption = answers[0], headline = True, images = [entry.thumbnail for entry in entries])
		return [headline] + [Slide(caption = ans) for ans in answers[1:]]	

	def Article(self, entries: List[Entry]) -> List[Slide]:
		combined = self._combined_entries(entries)
		answer = self.llm.generate(prompts["Article"].format(articles = combined))
		std = self._convert_answer_to_std(answer)
		return [Slide(caption = std[0], headline = True, images = [entry.thumbnail for entry in entries]), Slide(caption = std[1])]
	
	def ShortVideo(self, entries: List[Entry]) -> List[Slide]:
		combined = self._combined_entries(entries)
		answer = self.llm.generate(prompts["ShortVideo"].format(articles = combined))
		std = self._convert_answer_to_std(answer)
		return [Slide(caption = std[0], headline = True, images = [entry.thumbnail for entry in entries]), Slide(caption = std[1])]

	def LongVideo(self, entries: List[Entry]) -> List[Slide]:
		combined = self._combined_entries(entries)
		answer = self.llm.generate(prompts["LongVideo"].format(articles = combined))
		return [Slide(caption = std[0], headline = True, images = [entry.thumbnail for entry in entries]), Slide(caption = std[1])]

	def Image(self, entries: List[Entry]) -> List[Slide]:
		combined = self._combined_entries(entries)
		answer = self.llm.generate(prompts["Image"].format(articles = combined))
		return [Slide(caption = answer, headline = True, images = [entry.thumbnail for entry in entries])]

	def Carousel(self, entries: List[Entry]) -> List[Slide]:
		combined = self._combined_entries(entries)
		answer = self.llm.generate(prompts["Carousel"].format(articles = combined))
		std = self._convert_carousel_to_std(answer)
		headline = Slide(caption = std[0], headline = True, images = [entry.thumbnail for entry in entries])
		return [headline] + [Slide(caption = ans) for ans in std[1:]]
