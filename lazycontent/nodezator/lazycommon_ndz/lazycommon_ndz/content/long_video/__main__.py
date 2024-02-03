from lazycommon.content.types import LongVideo

from io import BufferedReader

main_callable = LongVideo

def _LongVideo(content: {"widget_name": "text_display", "type": str} = "", video: BufferedReader = None) -> [{"name": "content", "type": LongVideo}]:
	pass

signature_callable = _LongVideo
