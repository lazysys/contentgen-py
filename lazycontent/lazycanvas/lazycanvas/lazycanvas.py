from PIL import Image
from .img_editor import ImageEditor
from dataclasses import dataclass

from .templates.templates import CanvasTemplate

from .font import FontType

import deprecation
import tempfile

from lazycommon.slide import Slide

from typing import List

from io import BufferedReader, BytesIO

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
	
	@deprecation.deprecated(details="We moved to BufferedReader images, no need for this.")
	def get_temp_file(self, img: Image) -> str:
		file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
		img.save(file.name)
		return file.name

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
		editor = ImageEditor(self.template.backgrounds[1 if ((index or 0) % 2 == 0) else 2])
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

	def _slides_to_images(self, *slides: Slide) -> List[Image]:
		master = []
		if slides[0].headline:
			master = [self.master_slide(slides[0].caption)]
			slides = slides[1:]
		return master + [self.carousel_slide(slide.caption, i+1) for i, slide in enumerate(slides)]
	
	def slides_to_slides(self, *slides: Slide) -> List[Slide]:
		return [Slide(caption = slides[i].caption, headline = i == 0, images = [self._image_to_buffered_reader(image)]) for i, image in enumerate(self._slides_to_images(*slides))]

	def _image_to_buffered_reader(self, image: Image) -> BufferedReader:
		buf = BytesIO()
		image.save(buf, format="PNG")
		buf.seek(0)
		return BufferedReader(buf)
