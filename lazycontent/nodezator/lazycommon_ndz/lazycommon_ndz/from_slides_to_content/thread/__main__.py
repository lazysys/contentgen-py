from lazycommon.slide import Slide
from lazycommon.content.types import Thread

from typing import List

def _Thread(slides: List[Slide]) -> [{"name": "content", "type": Thread}]:
	return Thread.from_slides(slides)

main_callable = _Thread
