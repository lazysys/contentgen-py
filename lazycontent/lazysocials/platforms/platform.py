from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Type

from lazycommon.content_type import Content

@dataclass
class Platform:
	# TODO: make this a dict [Type -> Function] and what has None is unsupported
	types: List[Type[Content]]
	
	def _raise_can_post(self, content: Content) -> bool:
		typ = type(content)
		if typ in self.types:
			return True
		else:
			raise TypeNotSupported(self, typ)
	
	def publish(self, content: Content) -> bool:
		return self._raise_can_post(content)

class TypeNotSupported(Exception):
	def __init__(self, platform: Platform, typ: Type[Content]):
		super().__init__(f"Type {content.__name__} is not supported by the {platform.__name__} platform!")
