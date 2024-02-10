from lazycommon.slide import Slide
from lazycommon.content.types import Image

from typing import List

def from_slides_to_image(slides: List[Slide]) -> [{"name": "content", "type": Image}]:
	return Image.from_slide(slides[0])

main_callable = from_slides_to_image
