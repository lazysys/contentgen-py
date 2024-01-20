from abc import ABC, abstractmethod
from PIL import Image
from typing import Tuple, Dict
from dataclasses import dataclass

from font import Font

class CanvasTemplate(ABC):
	@property
	@abstractmethod
	def backgrounds(self) -> Tuple[Image, Image, Image]:
		pass

	@property
	@abstractmethod
	def colors(self) -> (Tuple[int, int, int], Tuple[int, int, int]):
		pass

	@property
	@abstractmethod
	def fonts(self) -> (Font, Font):
		pass

	@property
	@abstractmethod
	def sizes(self) -> Dict[str, int]:
		pass
