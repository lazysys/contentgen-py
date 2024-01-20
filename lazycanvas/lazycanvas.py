from PIL import Image
from img_editor import ImageEditor

from abc import ABC, abstractmethod
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
class LazyCanvas:
	template: CanvasTemplate
	branding: str
	
	def _branding(self, img: Image) -> Image:
		editor = ImageEditor(img)
		editor.write_text(self.branding, color = self.template.color, center = editor.points.bottom_text, size = 75)
		return editor.image

	def master_slide(self, headline: str) -> Image:
		editor = ImageEditor(self.template.backgrounds[0])
		editor.write_text(headline, color = self.template.color, size = 275, constraints = editor.points.body_constraints)
		return self._branding(editor.image)
	
	def carousel_slide(self, text: str, index: int = None) -> Image:
		editor = ImageEditor(self.template.backgrounds[1 if (index or 0) % 2 == 0 else 2])
		if not index == None:
			editor.write_text(str(index + 1), color = self.template.color, center = editor.points.top_text, size = 75)
		editor.write_text(text, color = self.template.color, size = 150, constraints = editor.points.body_constraints)
		return self._branding(editor.image)


lazycanvas = LazyCanvas(CustomTemplate(("background0.png", "background1.png", "background2.png"), (0, 255, 255)), "@gregismotion")

#lazycanvas.master_slide("HOW AI WILL TAKE OVER THE WORLD").show()
#lazycanvas.carousel_slide("AI is literally going to replace you. There's no escape.").show()
#lazycanvas.carousel_slide("AI is literally going to replace you. There's no escape.", 0).show()
#lazycanvas.carousel_slide("Lorem ipsum dolor sit amet?", 1).show()
lazycanvas.carousel_slide("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", 2).show()

