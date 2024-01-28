from ...content_type import Microblog, Thread

from PIL import Image

from typing import List

main_callable = Thread

def _Thread(content: {"widget_name": "text_display", "type": str} = "", microblogs: List[Microblog] = [], images: List[type(Image)] = []) -> [{"name": "content", "type": Thread}]:
	pass

signature_callable = _Thread
