from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Type

import lazycommon.content_type as content_type

@dataclass
class Platform:
	types: List[Type[content_type.Content]]

	def __getattr__(self, name):
		raise TypeNotSupported(self, name)
	
	def _is_type_in(self, typ: Type, target_list: List) -> bool:
		target_list = [target.__name__ for target in target_list]
		return any([mro.__name__ in target_list for mro in typ.mro()])
	def _is_type_enabled(self, typ: Type) -> bool:
		return self._is_type_in(typ, self.types)
	def _can_post(self, content: content_type.Content) -> bool:
		return self._is_type_enabled(type(content))
	
	def publish(self, content: content_type.Content) -> bool:
		if self._can_post(content):
			typ = type(content)
			while True:
				mro = typ.mro()
				try:
					return getattr(self, typ.__name__)(content)
				except TypeNotSupported:
					typ = mro[1]
				if len(mro) <= 2:
					raise TypeNotSupported(type(content).__name__)
		else:
			raise TypeDisabled(self, type(content))

class TypeNotSupported(Exception):
	def __init__(self, platform: Platform, name: str):
		super().__init__(f"Type {name} is not supported by the {type(platform).__name__} platform!")

class TypeDisabled(Exception):
	def __init__(self, platform: Platform, typ: Type[content_type.Content]):
		super().__init__(f"Type {typ.__name__} is disabled on {type(platform).__name__} platform!")
