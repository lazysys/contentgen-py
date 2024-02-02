from ...content_type import Image, Carousel

from typing import List

main_callable = Carousel

def _Carousel(content: {"widget_name": "text_display", "type": str} = "", content_images: List[Image] = []) -> [{"name": "content", "type": Carousel}]:
	pass

signature_callable = _Carousel
