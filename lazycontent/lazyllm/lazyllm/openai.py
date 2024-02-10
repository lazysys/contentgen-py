from io import BufferedReader
from dataclasses import dataclass
from typing import List

import base64

import openai
from openai import OpenAI

@dataclass
class BaseOpenAILLM(LLM):
	_api: OpenAIChat
	model: str = "gpt-3.5-turbo"
	
	@classmethod
	def models(_):
		return OpenAIChat.models

	def generate(self, prompt: str, *images: BufferedReader) -> str:
		return self._api.generate(prompt)

# TODO: find a way to query models for capabilities, will burn in supported models for now...
class VisionOpenAILLM(BaseOpenAILLM, VisionLLM):
	def __init__(self, api: OpenAIChat, model: str = "gpt-4-vision-preview"):
		super().__init__(api, model)

	@classmethod
	def models(_):
		return ["gpt-4-vision-preview"]

	def generate(self, prompt: str, *images: BufferedReader) -> str:
		return self._api.generate(prompt, images)

# TODO: find a way to query models for capabilities, will burn in supported models for now...
class JSONOpenAILLM(BaseOpenAILLM, JSONLLM):
	def __init__(self, api: OpenAIChat, model: str = "gpt-3.5-turbo"):
		super().__init__(api, model)

	@classmethod
	def models(_):
		return ["gpt-3.5-turbo-1106", "gpt-3.5-turbo-0125", "gpt-3.5-turbo", "gpt-4-1106-preview", "gpt-4-0125-preview", "gpt-4-turbo-preview"]

	def generate(self, prompt: str, *images: BufferedReader) -> str:
		return self._api.generate(prompt, json = True, system = "Use JSON in your responses.")

@dataclass
class OpenAIChat:
	_key: str
	model: str = "gpt-3.5-turbo"
	seed: int = 0
	
	frequency_penalty: int = None
	presence_penalty: int = None
	logit_bias = None
	logprobs: bool = None
	top_logprobs: int = None
	max_tokens: int = None
	n: int = None
	stop: List[str] = None
	temperature: int = None
	top_p: int = None
	tools: List = None
	tool_choice = None
	user = None
	
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
	
	def _prompt_to_content(self, prompt: str) -> List:
		return [{"type": "text", "text": prompt}]

	def _image_to_base64(self, image: BufferedReader) -> str:
		return base64.b64encode(image.read())
	def _image_to_content(self, image: BufferedReader) -> List:
		return [{"type": , "image_url": {"url": f"data:image/jpeg;base64,{self._image_to_base64(image)}"}}]

	def generate(self, prompt: str, *images: BufferedReader, **kwargs) -> str:
		texts = self._prompt_to_content(prompt)
		images = [self._image_to_content(image) for image in images]
		user = { "role": "user", "content": texts + images }
			
		system = { "role": "system", "content": kwargs["system"] } if kwargs.get("system", False) else None

		response_format = None
		if kwargs["json"]:
			response_format = {"type": "json_object"}
				
		messages = [
			system,
			user
		]

		return self._api.chat.completions.create(
			messages = messages, 
			response_format = response_format, 

			model = self.model,
			seed = self.seed,
			stop = self.stop,
			frequency_penalty = self.frequency_penalty,
			presence_penalty = self.presence_penalty,
			logit_bias = self.logit_bias,
			logprobs = self.logprobs,
			top_logprobs = self.top_logprobs,
			max_tokens = self.max_tokens,
			n = self.n,
			temperature = self.temperature,
			top_p = self.top_p,
			tools = self.tools,
			tool_choice = self.tool_choice,
			user = self.user
		).choices[0].message.content
