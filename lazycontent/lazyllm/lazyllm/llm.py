from abc import ABC, abstractmethod
from io import BufferedReader

from dataclasses import dataclass

class LLM(ABC):
	
	@abstractmethod
	def generate(self, prompt: str, *images: BufferedReader) -> str:
		pass

class VisionLLM(LLM):
	pass
class JSONLLM(LLM):
	pass
