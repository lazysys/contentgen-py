from lazycanvas import LazyCanvas
from lazycommon.slide import Slide

from typing import List

def slides_to_slides(lazycanvas: LazyCanvas, *slides: Slide) -> [{"name": "slides", "type": List[Slide]}]:
	return lazycanvas.slides_to_slides(*slides)

main_callable = slides_to_slides
