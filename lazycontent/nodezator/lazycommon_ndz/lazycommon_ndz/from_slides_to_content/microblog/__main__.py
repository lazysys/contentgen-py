from lazycommon.slide import Slide
from lazycommon.content.types import Microblog

from typing import List

def from_slides_to_microblog(slides: List[Slide]) -> [{"name": "content", "type": Microblog}]:
	return Microblog.from_slide(slides[0])

main_callable = from_slides_to_microblog
