from ...content_type import Microblog

from PIL import Image

from typing import List

main_callable = Microblog

def _Microblog(content: {"widget_name": "text_display", "type": str} = "", images: List[type(Image)] = []) -> [{"name": "content", "type": Microblog}]:
	pass

signature_callable = _Microblog
