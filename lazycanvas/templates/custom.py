from PIL import Image
from typing import Tuple
from dataclasses import dataclass

from templates import CanvasTemplate

# NOTE: this wasn't updated for a very long time, surely DEPRECATED AND NOT WORKING
@dataclass
class CustomTemplate(CanvasTemplate):
	_backgrounds: Tuple[str, str, str]
	_colors: (Tuple[int, int, int], Tuple[int, int, int])

	@property
	def backgrounds(self):
		return tuple(map(Image.open, self._backgrounds)) 

	@property
	def colors(self):
		return self._color
