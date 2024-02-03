from lazycommon.slide import Slide
from lazycommon.content.types import Image

from typing import List

def _Image(slides: List[Slide]) -> [{"name": "content", "type": Image}]:
	return Image.from_slide(slides[0])

main_callable = _Image
