from abc import ABC, abstractmethod
from PIL import Image
from typing import Tuple
from dataclasses import dataclass
class CanvasTemplate(ABC):
	@property
	@abstractmethod
	def backgrounds(self) -> Tuple[Image, Image, Image]:
		pass

	@property
	@abstractmethod
	def color(self) -> Tuple[int, int, int]:
		pass
@dataclass
class CustomTemplate(CanvasTemplate):
	_backgrounds: Tuple[str, str, str]
	_color: Tuple[int, int, int]

	@property
	def backgrounds(self):
		return tuple(map(Image.open, self._backgrounds)) 

	@property
	def color(self):
		return self._color

@dataclass
class FolderTemplate(CanvasTemplate)
	path: str

	@property
	def backgrounds()
