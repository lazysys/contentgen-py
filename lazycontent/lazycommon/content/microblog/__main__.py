from ...content_type import Microblog

from typing import List

main_callable = Microblog

def _Microblog(content: {"widget_name": "text_display", "type": str} = "", bytes_images: List[bytes] = []) -> [{"name": "content", "type": Microblog}]:
	pass

signature_callable = _Microblog
