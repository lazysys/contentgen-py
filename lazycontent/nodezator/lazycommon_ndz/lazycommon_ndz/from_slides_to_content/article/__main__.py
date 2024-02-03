from lazycommon.slide import Slide
from lazycommon.content.types import Article

from typing import List

def from_slides_to_Article(slides: List[Slide]) -> [{"name": "content", "type": Article}]:
	return Article.from_slides(slides)

main_callable = from_slides_to_Article
