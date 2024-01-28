from ...content_type import LongVideo

main_callable = LongVideo

def _LongVideo(content: {"widget_name": "text_display", "type": str} = "", video: bytes = b'') -> [{"name": "content", "type": LongVideo}]:
	pass

signature_callable = _LongVideo
