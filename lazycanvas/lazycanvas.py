from PIL import Image
from img_editor import ImageEditor
from dataclasses import dataclass

from templates import CanvasTemplate

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
