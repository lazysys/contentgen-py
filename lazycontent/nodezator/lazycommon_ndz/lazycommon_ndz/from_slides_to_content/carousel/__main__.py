from lazycommon.slide import Slide
from lazycommon.content.types import Carousel

from typing import List

def from_slides_to_carousel(slides: List[Slide]) -> [{"name": "content", "type": Carousel}]:
	return Carousel.from_slides(slides)

main_callable = from_slides_to_carousel
