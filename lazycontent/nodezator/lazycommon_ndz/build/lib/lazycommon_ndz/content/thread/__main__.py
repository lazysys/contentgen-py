from lazycommon.content.types import Microblog, Thread

from typing import List

from io import BufferedReader

main_callable = Thread

def _Thread(content: {"widget_name": "text_display", "type": str} = "", microblogs: List[Microblog] = [], images: List[BufferedReader] = []) -> [{"name": "content", "type": Thread}]:
	pass

signature_callable = _Thread
