from PIL import Image
from img_editor import ImageEditor
from dataclasses import dataclass

from templates.templates import CanvasTemplate

from font import FontType

@dataclass
class LazyCanvas:
	template: CanvasTemplate
	branding: str
	
	def _branding(self, img: Image) -> Image:
		editor = ImageEditor(img)
		editor.write_text(
				self.branding, 
				font = self.template.fonts[1], 
				color = self.template.colors[1], 
				center = editor.points.bottom_text, 
				size = self.template.sizes["secondary"])
		return editor.image

	def master_slide(self, headline: str) -> Image:
		editor = ImageEditor(self.template.backgrounds[0])
		editor.write_text(
				headline, 
				font = self.template.fonts[0], 
				font_type = FontType.BOLD,
				color = self.template.colors[0], 
				size = self.template.sizes["headline"],
				constraints = editor.points.body_constraints
		)
		return self._branding(editor.image)
	
	def carousel_slide(self, text: str, index: int = None) -> Image:
		editor = ImageEditor(self.template.backgrounds[1 if (index or 0) % 2 == 0 else 2])
		if not index == None:
			editor.write_text(
					str(index + 1), 
					font = self.template.fonts[1], 
					color = self.template.colors[1], 
					center = editor.points.top_text, 
					size = self.template.sizes["secondary"]
			)
		editor.write_text(text, font = self.template.fonts[0], color = self.template.colors[0], size = self.template.sizes["body"], constraints = editor.points.body_constraints)
		return self._branding(editor.image)
