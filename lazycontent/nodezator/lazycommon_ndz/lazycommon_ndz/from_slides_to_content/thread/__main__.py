from lazycommon.slide import Slide
from lazycommon.content.types import Thread

from typing import List

def from_slides_to_thread(slides: List[Slide]) -> [{"name": "content", "type": Thread}]:
	return Thread.from_slides(slides)

main_callable = from_slides_to_thread
