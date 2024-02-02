from ...content_type import Microblog

from typing import List

from io import BufferedReader

main_callable = Microblog

def _Microblog(content: {"widget_name": "text_display", "type": str} = "", images: List[BufferedReader] = []) -> [{"name": "content", "type": Microblog}]:
	pass

signature_callable = _Microblog
